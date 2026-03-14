# Slack Sales Buddy — Tenfold AI

An AI-powered sales assistant that lives in your Slack workspace. Powered by Claude and grounded in Tenfold AI's GTM knowledge base — loaded directly from Google Drive.

## What It Does

- **@SalesBuddy** in any channel — ask questions about positioning, market data, competitive intel
- **DM the bot** — private conversations for meeting prep, email drafts, objection handling
- **/salesbuddy** slash command — quick lookups from anywhere in Slack

### Example Questions

```
@SalesBuddy What's our pitch against generic Microsoft Copilot for legal teams?
@SalesBuddy Give me 3 talking points for a legal ops VP meeting
@SalesBuddy How should we position around the M365 E7 launch?
@SalesBuddy What adoption success factors should I share with a prospect?
/salesbuddy Summarize the Taiwan market opportunity
```

## Setup

### 1. Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From scratch**
2. Name it `Sales Buddy` and select your workspace

**Enable Socket Mode:**
- Go to **Socket Mode** (left sidebar) → toggle it **ON**
- Generate an **App-Level Token** with `connections:write` scope → save as `SLACK_APP_TOKEN`

**Set Bot Permissions** (OAuth & Permissions → Scopes → Bot Token Scopes):
- `app_mentions:read` — respond to @mentions
- `chat:write` — send messages
- `im:history` — read DMs
- `im:read` — access DM channels
- `channels:history` — read channel messages (for thread context)
- `commands` — slash commands

**Enable Events** (Event Subscriptions → toggle ON → Subscribe to bot events):
- `app_mention`
- `message.im`

**Create Slash Command** (Slash Commands → Create New Command):
- Command: `/salesbuddy`
- Description: `Ask the Sales Buddy a question`
- Usage hint: `[your question]`

**Install the App:**
- Go to **Install App** → **Install to Workspace** → Authorize
- Copy the **Bot User OAuth Token** → save as `SLACK_BOT_TOKEN`

### 2. Get an Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Create an API key → save as `ANTHROPIC_API_KEY`

### 3. Connect Google Drive

The bot reads your sales knowledge base directly from a Google Drive folder — no need to download files.

**Create a Google Cloud Service Account:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use an existing one)
3. Enable the **Google Drive API**:
   - Go to **APIs & Services** → **Library**
   - Search "Google Drive API" → **Enable**
4. Create a **Service Account**:
   - Go to **APIs & Services** → **Credentials**
   - Click **Create Credentials** → **Service Account**
   - Name it `sales-buddy-drive` → **Create and Continue**
   - Skip role assignment → **Done**
5. Create a key for the service account:
   - Click the service account → **Keys** tab → **Add Key** → **Create new key**
   - Choose **JSON** → Download the file
   - Save it as `service-account.json` in the project root (it's already in `.gitignore`)

**Share your Drive folder with the service account:**

1. Copy the service account email (looks like `sales-buddy-drive@your-project.iam.gserviceaccount.com`)
2. Go to your Google Drive folder
3. Click **Share** → paste the service account email → set to **Viewer** → **Send**

**Get the folder ID:**

The folder ID is the last part of the Drive URL:
```
https://drive.google.com/drive/folders/1j-3uWjNXmhRc6tIaS9QH-eQQ73QQCMDB
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                        This is your GOOGLE_DRIVE_FOLDER_ID
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your tokens:
#   SLACK_BOT_TOKEN=xoxb-...
#   SLACK_APP_TOKEN=xapp-...
#   ANTHROPIC_API_KEY=sk-ant-...
#   GOOGLE_DRIVE_FOLDER_ID=1j-3uWjNXmhRc6tIaS9QH-eQQ73QQCMDB
#   GOOGLE_SERVICE_ACCOUNT_FILE=./service-account.json
```

### 5. Install & Run

```bash
pip install -r requirements.txt
python bot.py
```

The bot connects via Socket Mode (no public URL needed) and will log `Bolt app is running!` when ready.

## Supported File Types from Google Drive

| File Type | How It's Processed |
|-----------|-------------------|
| Google Docs | Exported as plain text |
| Google Slides | Exported as plain text |
| Google Sheets | Exported as CSV |
| PDFs | Text extracted via PyPDF2 |
| Markdown (.md) | Read as-is |
| Plain text (.txt) | Read as-is |
| Word (.docx) | Exported via Drive as text |
| PowerPoint (.pptx) | Exported via Drive as text |
| Excel (.xlsx) | Exported via Drive as CSV |

The bot also loads any `.md` files from the repo root as supplemental knowledge.

Subfolders in the Drive folder are scanned recursively.

## Architecture

```
Slack (mentions, DMs, /command)
    ↓
bot.py (Slack Bolt + Socket Mode)
    ↓
knowledge_base.py
    ├── Google Drive API (service account auth)
    │   └── Reads all docs/slides/PDFs from shared folder
    └── Local .md files (fallback/supplement)
    ↓
Claude API (Anthropic) with system prompt + knowledge context
    ↓
Response back to Slack thread
```

## Adding Knowledge

**Via Google Drive (recommended):** Just add files to the shared Drive folder. Restart the bot to pick up new content.

**Via local files:** Drop `.md` files into the repo root — they're loaded automatically alongside Drive content.
