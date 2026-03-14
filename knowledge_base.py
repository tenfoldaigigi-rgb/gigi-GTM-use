"""
Loads GTM knowledge base documents from the repository for the Sales Buddy bot.
"""

import os
import glob


KNOWLEDGE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_knowledge_base() -> str:
    """Load all markdown files from the repo as the sales knowledge base."""
    documents = []
    md_files = sorted(glob.glob(os.path.join(KNOWLEDGE_DIR, "*.md")))

    for filepath in md_files:
        filename = os.path.basename(filepath)
        # Skip README since it's setup instructions, not sales content
        if filename.lower() == "readme.md":
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        documents.append(f"--- Document: {filename} ---\n{content}")

    return "\n\n".join(documents)
