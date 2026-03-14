"""
Loads GTM knowledge base from Google Drive and/or local markdown files.

Supports:
- Google Docs (exported as plain text)
- Google Slides (exported as plain text)
- Google Sheets (exported as CSV)
- PDFs (text extracted via PyPDF2)
- Plain text / markdown files
- Microsoft Office files (.docx, .pptx, .xlsx exported via Google Drive)
"""

import glob
import io
import json
import logging
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

logger = logging.getLogger("sales-buddy.knowledge")

KNOWLEDGE_DIR = os.path.dirname(os.path.abspath(__file__))

# Google Drive MIME types and how to handle them
EXPORT_MIME_MAP = {
    "application/vnd.google-apps.document": {
        "export_mime": "text/plain",
        "label": "Google Doc",
    },
    "application/vnd.google-apps.spreadsheet": {
        "export_mime": "text/csv",
        "label": "Google Sheet",
    },
    "application/vnd.google-apps.presentation": {
        "export_mime": "text/plain",
        "label": "Google Slides",
    },
}

# Binary/text files we can download directly
DOWNLOADABLE_MIMES = {
    "application/pdf",
    "text/plain",
    "text/markdown",
    "text/csv",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def _get_drive_service():
    """Build an authenticated Google Drive service using a service account."""
    creds_path = os.environ.get(
        "GOOGLE_SERVICE_ACCOUNT_FILE",
        os.path.join(KNOWLEDGE_DIR, "service-account.json"),
    )

    # Support credentials as JSON string in env var (useful for deployment)
    creds_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if creds_json:
        info = json.loads(creds_json)
        creds = service_account.Credentials.from_service_account_info(
            info, scopes=SCOPES
        )
    elif os.path.exists(creds_path):
        creds = service_account.Credentials.from_service_account_file(
            creds_path, scopes=SCOPES
        )
    else:
        return None

    return build("drive", "v3", credentials=creds)


def _extract_pdf_text(content_bytes: bytes) -> str:
    """Extract text from a PDF file."""
    try:
        from PyPDF2 import PdfReader

        reader = PdfReader(io.BytesIO(content_bytes))
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append(f"[Page {i + 1}]\n{text}")
        return "\n\n".join(pages)
    except Exception as e:
        logger.warning("Failed to extract PDF text: %s", e)
        return "[PDF content could not be extracted]"


def _list_files_in_folder(service, folder_id: str) -> list:
    """List all files in a Google Drive folder (non-recursive by default)."""
    results = []
    page_token = None

    while True:
        response = (
            service.files()
            .list(
                q=f"'{folder_id}' in parents and trashed = false",
                fields="nextPageToken, files(id, name, mimeType)",
                pageSize=100,
                pageToken=page_token,
            )
            .execute()
        )
        results.extend(response.get("files", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return results


def _list_files_recursive(service, folder_id: str, path: str = "") -> list:
    """Recursively list all files in a Google Drive folder and subfolders."""
    all_files = []
    items = _list_files_in_folder(service, folder_id)

    for item in items:
        item_path = f"{path}/{item['name']}" if path else item["name"]

        if item["mimeType"] == "application/vnd.google-apps.folder":
            # Recurse into subfolders
            all_files.extend(
                _list_files_recursive(service, item["id"], item_path)
            )
        else:
            item["path"] = item_path
            all_files.append(item)

    return all_files


def _download_file(service, file_info: dict) -> str:
    """Download or export a file from Google Drive and return its text content."""
    file_id = file_info["id"]
    mime_type = file_info["mimeType"]
    name = file_info.get("path", file_info["name"])

    # Google Workspace files — export them
    if mime_type in EXPORT_MIME_MAP:
        export_info = EXPORT_MIME_MAP[mime_type]
        logger.info("Exporting %s (%s) as text", name, export_info["label"])
        request = service.files().export_media(
            fileId=file_id, mimeType=export_info["export_mime"]
        )
        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        return buffer.getvalue().decode("utf-8", errors="replace")

    # Downloadable binary/text files
    if mime_type in DOWNLOADABLE_MIMES:
        logger.info("Downloading %s (%s)", name, mime_type)
        request = service.files().get_media(fileId=file_id)
        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        content_bytes = buffer.getvalue()

        if mime_type == "application/pdf":
            return _extract_pdf_text(content_bytes)
        else:
            return content_bytes.decode("utf-8", errors="replace")

    logger.warning("Skipping unsupported file type: %s (%s)", name, mime_type)
    return ""


def load_from_google_drive(folder_id: str) -> str:
    """Load all documents from a Google Drive folder as a single knowledge string."""
    service = _get_drive_service()
    if not service:
        logger.warning(
            "Google Drive not configured — no service account credentials found. "
            "Set GOOGLE_SERVICE_ACCOUNT_FILE or GOOGLE_SERVICE_ACCOUNT_JSON."
        )
        return ""

    logger.info("Loading knowledge base from Google Drive folder: %s", folder_id)
    files = _list_files_recursive(service, folder_id)
    logger.info("Found %d files in Drive folder", len(files))

    documents = []
    for f in files:
        try:
            content = _download_file(service, f)
            if content.strip():
                doc_path = f.get("path", f["name"])
                documents.append(f"--- Document: {doc_path} ---\n{content}")
                logger.info("Loaded: %s (%d chars)", doc_path, len(content))
        except Exception as e:
            logger.error("Failed to load %s: %s", f["name"], e)

    return "\n\n".join(documents)


def load_from_local_files() -> str:
    """Load all markdown files from the repo as the sales knowledge base."""
    documents = []
    md_files = sorted(glob.glob(os.path.join(KNOWLEDGE_DIR, "*.md")))

    for filepath in md_files:
        filename = os.path.basename(filepath)
        if filename.lower() == "readme.md":
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        documents.append(f"--- Document: {filename} ---\n{content}")

    return "\n\n".join(documents)


def load_knowledge_base() -> str:
    """
    Load knowledge from all configured sources.

    Priority:
    1. Google Drive folder (if GOOGLE_DRIVE_FOLDER_ID is set)
    2. Local markdown files (always loaded as fallback/supplement)
    """
    parts = []

    # Google Drive
    folder_id = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")
    if folder_id:
        drive_content = load_from_google_drive(folder_id)
        if drive_content:
            parts.append(drive_content)
            logger.info("Loaded knowledge from Google Drive")
    else:
        logger.info("No GOOGLE_DRIVE_FOLDER_ID set — skipping Drive")

    # Local files
    local_content = load_from_local_files()
    if local_content:
        parts.append(local_content)
        logger.info("Loaded knowledge from local markdown files")

    combined = "\n\n".join(parts)
    if not combined:
        logger.warning("No knowledge base content loaded from any source!")
    return combined
