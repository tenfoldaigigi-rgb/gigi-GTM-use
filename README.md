# Slack Sales Buddy — Tenfold AI

An AI-powered sales assistant that lives in your Slack workspace. Powered by Claude and grounded in Tenfold AI's GTM knowledge base.

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

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your tokens:
#   SLACK_BOT_TOKEN=xoxb-...
#   SLACK_APP_TOKEN=xapp-...
#   ANTHROPIC_API_KEY=sk-ant-...
```

### 4. Install & Run

```bash
pip install -r requirements.txt
python bot.py
```

The bot connects via Socket Mode (no public URL needed) and will log `⚡️ Bolt app is running!` when ready.

## Adding Knowledge

Drop any `.md` files into the repo root — the bot automatically loads all markdown files (except README.md) as its knowledge base at startup. Add sales playbooks, competitive analyses, or product docs to make the bot smarter.

## Architecture

```
Slack (mentions, DMs, /command)
    ↓
bot.py (Slack Bolt + Socket Mode)
    ↓
knowledge_base.py (loads .md files from repo)
    ↓
Claude API (Anthropic) with system prompt + knowledge context
    ↓
Response back to Slack thread
```
