"""
Slack Sales Buddy — A Claude-powered sales assistant for Tenfold AI.

Responds to:
  - Direct mentions (@SalesBuddy) in any channel
  - Direct messages
  - The /salesbuddy slash command

Grounded in Tenfold AI's GTM knowledge base (Microsoft AI Summit analysis,
competitive positioning, market data, and sales playbooks).
"""

import logging
import os

import anthropic
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from knowledge_base import load_knowledge_base

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sales-buddy")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")

app = App(token=SLACK_BOT_TOKEN)
claude = anthropic.Anthropic()

# Load knowledge base once at startup
KNOWLEDGE = load_knowledge_base()

SYSTEM_PROMPT = f"""You are **Sales Buddy**, an AI sales assistant for Tenfold AI — a legal-tech company that builds AI-powered agents for enterprise legal teams.

Your job is to help the Tenfold AI sales team by:
1. Answering questions about our GTM strategy, market positioning, and competitive landscape.
2. Providing talking points, objection handling, and pitch guidance for sales conversations.
3. Summarizing market data, Microsoft ecosystem details, and adoption best practices.
4. Helping craft emails, call scripts, and meeting prep based on our knowledge base.

## Personality
- Confident but not arrogant — you know the market and our positioning cold.
- Concise — sales reps are busy, give them what they need fast.
- Action-oriented — always end with a clear recommendation or next step.
- Use bullet points and short paragraphs for readability in Slack.

## Key Positioning (always keep in mind)
- Tenfold AI provides **legal-grade AI agents** that outperform generic tools like Microsoft Copilot on accuracy, citation quality, and regulatory awareness.
- We play in **Phase 2** of Microsoft's Frontier Firm framework — specialized legal agents for due diligence, compliance, and contract analysis.
- Microsoft's own legal team only achieved a **5% cost reduction** with generic Copilot — we can beat that significantly with domain-specific agents.
- We are **compatible with the Microsoft ecosystem** (MCP, OpenAPI, A2A standards) — we complement M365 E7, not compete with it.
- **M365 E7 ships May 1, 2026** — ride that wave.

## Knowledge Base
Use the following internal documents to ground your answers. Cite specific data points when relevant.

{KNOWLEDGE}

## Rules
- If asked about something outside your knowledge base, say so honestly and suggest who on the team might know.
- Never make up statistics or data points — only cite what's in the knowledge base.
- Keep responses under 300 words unless the user explicitly asks for more detail.
- Format for Slack: use *bold*, _italic_, bullet points, and short paragraphs.
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def ask_claude(question: str, thread_context: str = "") -> str:
    """Send a question to Claude with the sales knowledge base context."""
    messages = []
    if thread_context:
        messages.append({"role": "user", "content": thread_context})
        messages.append(
            {
                "role": "assistant",
                "content": "I have the thread context. What's your question?",
            }
        )
    messages.append({"role": "user", "content": question})

    response = claude.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    return response.content[0].text


def get_thread_context(client, channel: str, thread_ts: str) -> str:
    """Fetch previous messages in a thread for conversational context."""
    try:
        result = client.conversations_replies(channel=channel, ts=thread_ts, limit=10)
        messages = result.get("messages", [])
        parts = []
        for msg in messages[:-1]:  # exclude the latest (current) message
            role = "User" if msg.get("bot_id") is None else "Sales Buddy"
            parts.append(f"{role}: {msg.get('text', '')}")
        return "\n".join(parts)
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Event handlers
# ---------------------------------------------------------------------------


@app.event("app_mention")
def handle_mention(event, client, say):
    """Respond when @SalesBuddy is mentioned in a channel."""
    question = event.get("text", "")
    channel = event["channel"]
    thread_ts = event.get("thread_ts", event["ts"])

    # Get thread context if replying in a thread
    context = ""
    if event.get("thread_ts"):
        context = get_thread_context(client, channel, thread_ts)

    try:
        answer = ask_claude(question, context)
        say(text=answer, thread_ts=thread_ts)
    except Exception as e:
        logger.error("Error calling Claude: %s", e)
        say(
            text="Sorry, I hit a snag. Try again in a moment!",
            thread_ts=thread_ts,
        )


@app.event("message")
def handle_dm(event, client, say):
    """Respond to direct messages."""
    # Only handle DMs (channel type 'im'), skip bot messages and subtypes
    if event.get("channel_type") != "im":
        return
    if event.get("bot_id") or event.get("subtype"):
        return

    question = event.get("text", "")
    thread_ts = event.get("thread_ts", event["ts"])

    context = ""
    if event.get("thread_ts"):
        context = get_thread_context(client, event["channel"], thread_ts)

    try:
        answer = ask_claude(question, context)
        say(text=answer, thread_ts=thread_ts)
    except Exception as e:
        logger.error("Error calling Claude: %s", e)
        say(
            text="Sorry, I hit a snag. Try again in a moment!",
            thread_ts=thread_ts,
        )


@app.command("/salesbuddy")
def handle_slash_command(ack, command, say):
    """Handle the /salesbuddy slash command."""
    ack()
    question = command.get("text", "").strip()
    if not question:
        say("Usage: `/salesbuddy <your question>`\n\nExamples:\n"
            "• `/salesbuddy What's our pitch against generic Copilot?`\n"
            "• `/salesbuddy Give me 3 talking points for a legal ops meeting`\n"
            "• `/salesbuddy Summarize the M365 E7 opportunity`")
        return

    try:
        answer = ask_claude(question)
        say(text=answer)
    except Exception as e:
        logger.error("Error calling Claude: %s", e)
        say("Sorry, I hit a snag. Try again in a moment!")


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting Sales Buddy bot...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
