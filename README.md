# ChatGPT JSON to Markdown Extractor

A lightweight Python script that converts your ChatGPT conversation history into clean Markdown files — perfect for migrating to Claude, importing into Obsidian/Notion, or building a personal knowledge base.

## Why Markdown?

Many guides suggest copying the raw HTML from ChatGPT's web interface into Claude or another tool. This works for short chats, but breaks down fast:

- **HTML is bloated** — a single conversation can be 10x larger than its actual content due to styling, scripts, and metadata
- **File size limits** — large HTML exports often exceed upload limits, forcing you to split or truncate
- **Noisy context** — HTML boilerplate wastes tokens and dilutes the signal for any AI reading it

Markdown strips all of that away. You get just the conversation — clean, structured, and small enough to transfer even massive chat histories.

## Migrating to Claude

This tool pairs perfectly with [Claude's memory import](https://claude.com/import-memory) feature. Two approaches:

### Approach 1: Import conversation history as project knowledge

1. Export and convert your ChatGPT chats using this script (see [How to Use](#-how-to-use) below)
2. Upload the resulting `.md` files to a [Claude Project](https://support.anthropic.com/en/articles/9517075-what-are-projects) as project knowledge
3. Claude can now reference your full conversation history

### Approach 2: Migrate your AI memory/preferences directly

Claude provides a migration prompt you can paste into ChatGPT (or any AI with memory) to export everything it knows about you:

> I'm moving to another AI service and need to export my data. List every memory you have stored about me, as well as any context you've learned about me from our past conversations. Output everything in a single block so I can easily copy it. Format each entry as: \[date saved, if available\] - memory content. Make sure to cover all of the following — preserve my words verbatim where possible:
>
> 1. Instructions I've given you about how to respond (tone, format, style, "always do X," "never do Y")
> 2. Personal and professional context (job, company, location, goals)
> 3. Projects or topics I frequently work on
> 4. Communication preferences (formal/informal, long/short, etc.)
> 5. Technical preferences (tools, frameworks, languages I use)
> 6. Recurring tasks or workflows
> 7. Any other context that would help a new AI assistant understand how I work

Then paste the output into [claude.com/import-memory](https://claude.com/import-memory) to transfer your preferences in under a minute.

You can combine both approaches — import your preferences via memory, and upload your full conversation history as project knowledge for deeper context.

## Features

- **Perfect Chronology** — rebuilds conversations from ChatGPT's node-mapping structure using timestamp metadata
- **Table of Contents** — combined output includes auto-generated TOC with anchor links
- **Interactive Mode** — when no `targets.txt` is found, choose to export all, pick interactively via a curses-based checklist, or exit
- **Flexible Output** — single combined file or individual `.md` per conversation (`--separate-files`)
- **Configurable Paths** — `--input-dir`, `--output-dir`, and `config.json` support
- **Privacy First** — only extracts the chats you specify; no data leaves your machine
- **Media Safe** — skips DALL-E/image generation metadata to prevent crashes
- **Zero Dependencies** — Python 3 standard library only

## How to Use

1. **Export your data** from ChatGPT: Settings → Data Controls → Export Data. Extract the `.zip`.

2. **Place your files.** Put the `conversations-00X.json` files in the same folder as `extract_chats.py` (or use `--input-dir`).

3. **Choose your targets** (optional):
   - Create a `targets.txt` with exact chat titles, one per line (see `targets.txt.example`)
   - Or skip it — the script will prompt you to export all or select interactively
   - Or use `--all` to export everything without prompts

4. **Run the script:**

   ```bash
   python3 extract_chats.py
   ```

5. **Read your chats.** Open the generated Markdown in your favorite viewer, upload to Claude, or import into Obsidian/Notion.

## CLI Options

| Flag | Description |
|------|-------------|
| `--all` | Export all conversations without prompting |
| `--separate-files` | Export each chat as its own `.md` file |
| `--input-dir DIR` | Directory containing `conversations-00*.json` files |
| `--output-dir DIR` | Directory for output files |
| `--config FILE` | Path to `config.json` (default: `config.json`) |

## Requirements

- Python 3.x
- No external dependencies
