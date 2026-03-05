# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Single-file Python script (`extract_chats.py`) that extracts specific ChatGPT conversations from official JSON data exports and converts them to Markdown. No external dependencies — uses only Python 3 stdlib (`json`, `os`, `glob`, `datetime`).

## Running

```bash
python3 extract_chats.py
```

Expects `conversations-00X.json` files and a `targets.txt` (one chat title per line) in the working directory. Outputs `Extracted_ChatGPT_Chats.md`.

## Architecture

The script has one main flow in `extract_conversations()`:
1. `load_targets()` reads chat titles from `targets.txt` into a set
2. Globs all `conversations-00*.json` files
3. For each conversation matching a target title, walks the `mapping` node tree, collects user/assistant messages (skipping non-string parts like DALL-E dicts), sorts by `create_time`, and formats to Markdown
4. Writes all matched conversations to a single output file

## Privacy

`conversations*.json`, `targets.txt`, and `Extracted_ChatGPT_Chats.md` are gitignored — never commit user data.

## Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `refactor:`, `perf:`, `test:`, `chore:`, etc.
