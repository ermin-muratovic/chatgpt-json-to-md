import json
import os
import glob

def load_targets(filename="targets.txt"):
    """Loads target conversation titles from a text file."""
    if not os.path.exists(filename):
        print(f"Error: '{filename}' not found. Please create it and add your chat titles.")
        return set()
    
    with open(filename, "r", encoding="utf-8") as f:
        # Strip whitespace and ignore empty lines
        return {line.strip() for line in f if line.strip()}

def extract_conversations():
    target_titles = load_targets()
    if not target_titles:
        return

    file_paths = glob.glob("conversations-00*.json")
    if not file_paths:
        print("Error: No 'conversations-00X.json' files found.")
        return

    markdown_lines = []
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
                
                messages.sort(key=lambda x: x["time"])
                
                for m in messages:
                    sender = "User" if m["role"] == "user" else "ChatGPT"
                    markdown_lines.append(f"**{sender}:**\n{m['text']}\n\n")
                
                markdown_lines.append("---\n\n")

    if processed_count == 0:
        print("\nNo matching conversations found. Check your targets.txt and JSON files.")
        return

    output_filename = "Extracted_ChatGPT_Chats.md"
    with open(output_filename, "w", encoding="utf-8") as out_f:
        out_f.write("".join(markdown_lines))

    print(f"\n✅ Success! {processed_count} matching conversations extracted.")
    print(f"Saved to: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    extract_conversations()
