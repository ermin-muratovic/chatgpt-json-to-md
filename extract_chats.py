import json
import os
import glob
import re
import argparse
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
    args = parser.parse_args()

    # Load config file defaults
    config = load_config(args.config)

    # Resolve: CLI args override config, config overrides hardcoded defaults
    input_dir = args.input_dir or config.get("input_dir", ".")
    output_dir = args.output_dir or config.get("output_dir", ".")
    separate_files = args.separate_files if args.separate_files is not None else config.get("separate_files", False)

    return input_dir, output_dir, separate_files

def load_targets(filename="targets.txt"):
    """Loads target conversation titles from a text file."""
    if not os.path.exists(filename):
        print(f"Error: '{filename}' not found. Please create it and add your chat titles.")
        return set()

    with open(filename, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}

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

def extract_conversations(input_dir=".", output_dir=".", separate_files=False):
    target_titles = load_targets()
    if not target_titles:
        return

    pattern = os.path.join(input_dir, "conversations-00*.json")
    file_paths = glob.glob(pattern)
    if not file_paths:
        print(f"Error: No 'conversations-00X.json' files found in '{input_dir}'.")
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

            if title in target_titles:
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
    input_dir, output_dir, separate_files = parse_args()
    extract_conversations(input_dir, output_dir, separate_files)
