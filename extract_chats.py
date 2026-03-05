import json
import os
import glob
import re
import argparse
import curses
from datetime import datetime

def load_config(config_path):
    """Loads configuration from a JSON file if it exists."""
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config file '{config_path}': {e}")
    return {}

def parse_args():
    """Parses CLI arguments with config file defaults."""
    parser = argparse.ArgumentParser(
        description="Extract specific ChatGPT conversations from JSON exports to Markdown."
    )
    parser.add_argument("--config", default="config.json",
                        help="path to config file (default: config.json)")
    parser.add_argument("--input-dir",
                        help="directory containing conversations-00*.json files (default: .)")
    parser.add_argument("--output-dir",
                        help="directory for output files (default: .)")
    parser.add_argument("--separate-files", action="store_true", default=None,
                        help="export each chat as a separate .md file")
    parser.add_argument("--all", action="store_true",
                        help="export all conversations without prompting")
    args = parser.parse_args()

    # Load config file defaults
    config = load_config(args.config)

    # Resolve: CLI args override config, config overrides hardcoded defaults
    input_dir = args.input_dir or config.get("input_dir", ".")
    output_dir = args.output_dir or config.get("output_dir", ".")
    separate_files = args.separate_files if args.separate_files is not None else config.get("separate_files", False)
    export_all = args.all

    return input_dir, output_dir, separate_files, export_all

def load_targets(filename="targets.txt"):
    """Loads target conversation titles from a text file. Returns None if file missing."""
    if not os.path.exists(filename):
        return None

    with open(filename, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def load_all_titles(input_dir):
    """Loads all conversation titles from JSON files in input_dir."""
    pattern = os.path.join(input_dir, "conversations-00*.json")
    file_paths = glob.glob(pattern)
    titles = []
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for conv in data:
                title = conv.get("title", "")
                if title:
                    titles.append(title)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    return sorted(set(titles))


def interactive_select(titles):
    """Curses-based checklist for selecting conversation titles."""
    selected = set()
    current = 0

    def draw(stdscr):
        nonlocal current, selected
        curses.curs_set(0)
        stdscr.clear()

        while True:
            stdscr.clear()
            max_y, max_x = stdscr.getmaxyx()
            header = "Select conversations (↑/↓: navigate, Space: toggle, a: all/none, Enter: confirm)"
            stdscr.addnstr(0, 0, header, max_x - 1, curses.A_BOLD)

            visible_rows = max_y - 3
            if visible_rows < 1:
                visible_rows = 1

            # Scrolling window
            if current < visible_rows:
                start = 0
            else:
                start = current - visible_rows + 1
            end = min(start + visible_rows, len(titles))

            for idx in range(start, end):
                row = 2 + (idx - start)
                marker = "[x]" if idx in selected else "[ ]"
                line = f" {marker} {titles[idx]}"
                attr = curses.A_REVERSE if idx == current else curses.A_NORMAL
                stdscr.addnstr(row, 0, line, max_x - 1, attr)

            status = f" {len(selected)} selected | {len(titles)} total"
            stdscr.addnstr(max_y - 1, 0, status, max_x - 1, curses.A_DIM)
            stdscr.refresh()

            key = stdscr.getch()
            if key == curses.KEY_UP and current > 0:
                current -= 1
            elif key == curses.KEY_DOWN and current < len(titles) - 1:
                current += 1
            elif key == ord(' '):
                if current in selected:
                    selected.discard(current)
                else:
                    selected.add(current)
            elif key == ord('a'):
                if len(selected) == len(titles):
                    selected.clear()
                else:
                    selected = set(range(len(titles)))
            elif key in (curses.KEY_ENTER, 10, 13):
                break
            elif key == ord('q') or key == 27:  # q or Escape
                selected.clear()
                break

    curses.wrapper(draw)
    return {titles[i] for i in selected}


def prompt_no_targets(all_titles):
    """Prompts the user to choose how to proceed when targets.txt is missing."""
    print("No targets.txt found. What would you like to do?\n")
    print("  [1] Export all conversations")
    print("  [2] Select interactively")
    print("  [3] Exit\n")

    while True:
        choice = input("Enter choice (1/2/3): ").strip()
        if choice == "1":
            return set(all_titles)
        elif choice == "2":
            if not all_titles:
                print("No conversations found to select from.")
                return set()
            return interactive_select(all_titles)
        elif choice == "3":
            return set()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def format_timestamp(unix_timestamp):
    """Converts unix timestamp to readable string."""
    if not unix_timestamp:
        return "Unknown Time"
    return datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')

def slugify(text):
    """Convert text to a safe slug for URLs and filenames."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def extract_messages(conv):
    """Extracts and returns sorted messages from a conversation."""
    messages = []
    mapping = conv.get("mapping", {})

    for node_id, node_data in mapping.items():
        msg = node_data.get("message")

        if msg and msg.get("author", {}).get("role") in ["user", "assistant"]:
            role = msg["author"]["role"]
            create_time = msg.get("create_time") or 0

            content_parts = msg.get("content", {}).get("parts", [])
            text = "".join([part for part in content_parts if isinstance(part, str)])

            if text.strip():
                messages.append({"role": role, "time": create_time, "text": text})

    messages.sort(key=lambda x: x["time"])
    return messages

def format_messages(title, messages):
    """Formats a conversation's messages as Markdown lines."""
    lines = [f"# {title}\n\n"]
    for m in messages:
        readable_time = format_timestamp(m['time'])
        if m["role"] == "user":
            lines.append(f"### 👤 You asked ({readable_time}):\n{m['text']}\n\n")
        else:
            lines.append(f"### 🤖 ChatGPT replied ({readable_time}):\n{m['text']}\n\n")
    lines.append("---\n\n")
    return lines

def extract_conversations(input_dir=".", output_dir=".", separate_files=False, export_all=False):
    pattern = os.path.join(input_dir, "conversations-00*.json")
    file_paths = glob.glob(pattern)
    if not file_paths:
        print(f"Error: No 'conversations-00X.json' files found in '{input_dir}'.")
        return

    target_titles = load_targets()

    if export_all:
        target_titles = None  # None means export everything

    if target_titles is not None and not target_titles:
        # targets.txt exists but is empty
        print("Error: 'targets.txt' is empty. Add chat titles or use --all.")
        return

    if target_titles is None and not export_all:
        # targets.txt is missing and --all not set: interactive prompt
        all_titles = load_all_titles(input_dir)
        if not all_titles:
            print("No conversations found in JSON files.")
            return
        target_titles = prompt_no_targets(all_titles)
        if not target_titles:
            return

    conversations = []  # List of (title, messages) tuples
    processed_count = 0

    for file_path in file_paths:
        print(f"Loading {file_path}...")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            continue

        for conv in data:
            title = conv.get("title", "")

            if target_titles is None or title in target_titles:
                messages = extract_messages(conv)
                if messages:
                    processed_count += 1
                    conversations.append((title, messages))

    if processed_count == 0:
        print("\nNo matching conversations found.")
        return

    os.makedirs(output_dir, exist_ok=True)

    if separate_files:
        for title, messages in conversations:
            filename = slugify(title) + ".md"
            filepath = os.path.join(output_dir, filename)
            content = "".join(format_messages(title, messages))
            with open(filepath, "w", encoding="utf-8") as out_f:
                out_f.write(content)
            print(f"  Wrote: {filepath}")
    else:
        # Combined file with TOC
        toc_lines = []
        markdown_lines = []
        for title, messages in conversations:
            slug = slugify(title)
            toc_lines.append(f"1. [{title}](#{slug})")
            markdown_lines.extend(format_messages(title, messages))

        output_lines = []
        if toc_lines:
            output_lines.append("# Table of Contents\n\n")
            output_lines.append("\n".join(toc_lines))
            output_lines.append("\n\n---\n\n")
        output_lines.extend(markdown_lines)

        output_filename = os.path.join(output_dir, "Extracted_ChatGPT_Chats.md")
        with open(output_filename, "w", encoding="utf-8") as out_f:
            out_f.write("".join(output_lines))

    print(f"\n✅ Success! {processed_count} matching conversations extracted with timestamps.")
    if separate_files:
        print(f"Saved to: {os.path.abspath(output_dir)}/")
    else:
        print(f"Saved to: {os.path.abspath(os.path.join(output_dir, 'Extracted_ChatGPT_Chats.md'))}")

if __name__ == "__main__":
    input_dir, output_dir, separate_files, export_all = parse_args()
    extract_conversations(input_dir, output_dir, separate_files, export_all)
