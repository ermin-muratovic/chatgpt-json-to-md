import json
import os
import glob
import re
from datetime import datetime

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
    """Convert text to GitHub-style URL slug."""
    # Convert to lowercase, replace spaces/special chars with hyphens
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)  # Remove special chars except spaces and hyphens
    text = re.sub(r'[-\s]+', '-', text)    # Replace spaces/multiple hyphens with single hyphen
    return text.strip('-')

def extract_conversations():
    target_titles = load_targets()
    if not target_titles:
        return

    file_paths = glob.glob("conversations-00*.json")
    if not file_paths:
        print("Error: No 'conversations-00X.json' files found.")
        return

    markdown_lines = []
    toc_lines = []
    processed_titles = []  # Track all processed titles for TOC
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
                processed_count += 1
                processed_titles.append(title)
                
                # Add to TOC
                slug = slugify(title)
                toc_lines.append(f"1. [{title}](#{slug})")
                
                markdown_lines.append(f"# {title}\n\n")
                
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
                
                # Chronological sort
                messages.sort(key=lambda x: x["time"])
                
                for m in messages:
                    readable_time = format_timestamp(m['time'])
                    if m["role"] == "user":
                        markdown_lines.append(f"### 👤 You asked ({readable_time}):\n{m['text']}\n\n")
                    else:
                        markdown_lines.append(f"### 🤖 ChatGPT replied ({readable_time}):\n{m['text']}\n\n")
                
                markdown_lines.append("---\n\n")

    if processed_count == 0:
        print("\nNo matching conversations found.")
        return

    # Generate output with TOC at the top
    output_lines = []
    
    # Add TOC header
    if toc_lines:
        output_lines.append("# Table of Contents\n\n")
        output_lines.append("\n".join(toc_lines))
        output_lines.append("\n\n---\n\n")
    
    # Add main content
    output_lines.extend(markdown_lines)

    output_filename = "Extracted_ChatGPT_Chats.md"
    with open(output_filename, "w", encoding="utf-8") as out_f:
        out_f.write("".join(output_lines))

    print(f"\n✅ Success! {processed_count} matching conversations extracted with timestamps.")
    print(f"Saved to: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    extract_conversations()
