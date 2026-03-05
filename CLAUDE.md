# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Single-file Python script (`extract_chats.py`) that converts ChatGPT JSON data exports into Markdown. Designed for migrating conversation history to Claude, Obsidian, Notion, or vector databases. No external dependencies — uses only Python 3 stdlib (`json`, `os`, `glob`, `datetime`, `re`, `argparse`, `curses`).

## Running

```bash
python3 extract_chats.py            # interactive prompt if no targets.txt
python3 extract_chats.py --all      # export everything, no prompts
python3 extract_chats.py --separate-files --output-dir out/
```

Expects `conversations-00X.json` files in the working directory (or `--input-dir`). Targets come from `targets.txt` (one title per line), interactive selection, or `--all`.

## Architecture

The script has one main flow in `extract_conversations()`:
1. Globs all `conversations-00*.json` files from `input_dir`
2. Resolves target titles: `load_targets()` returns a set (from file), `None` (file missing), or is overridden by `--all`
3. When targets is `None` and `--all` not set: `prompt_no_targets()` offers export-all, curses-based interactive picker (`interactive_select()`), or exit
4. For each matching conversation, walks the `mapping` node tree, collects user/assistant messages (skipping non-string parts like DALL-E dicts), sorts by `create_time`, formats to Markdown
5. Writes output as a single file with TOC or individual files per conversation (`--separate-files`)

## Key Functions

- `parse_args()` — CLI flags + `config.json` defaults, returns `(input_dir, output_dir, separate_files, export_all)`
- `load_targets()` — returns `set` of titles, or `None` if file missing
- `load_all_titles(input_dir)` — scans JSON files, returns sorted unique titles
- `interactive_select(titles)` — curses checklist (arrows, space, `a` for all, enter, `q`/esc)
- `prompt_no_targets(all_titles)` — 3-option menu when targets.txt absent
- `extract_messages(conv)` — walks node tree, returns sorted message list
- `format_messages(title, messages)` — produces Markdown lines

## Privacy

`conversations*.json`, `targets.txt`, and `Extracted_ChatGPT_Chats.md` are gitignored — never commit user data.

## Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `refactor:`, `perf:`, `test:`, `chore:`, etc.
