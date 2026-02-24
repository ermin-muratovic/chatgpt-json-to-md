# ChatGPT JSON to Markdown Extractor

A lightweight, robust Python script to extract specific ChatGPT conversations from your official JSON data export and convert them into a clean, chronologically ordered Markdown (`.md`) file. 

## 🚀 Features
- **Perfect Chronology:** Rebuilds conversations based on timestamp metadata, navigating ChatGPT's complex node-mapping structure.
- **Privacy First:** Only extracts the exact chats you specify. 
- **Markdown Ready:** Formats output beautifully for Obsidian, Notion, or vector databases (RAG).
- **Media Safe:** Bypasses image/DALL-E generation dictionaries to prevent script crashes.

## 📋 How to Use

1. **Export your data:** Request your data export from ChatGPT (Settings > Data Controls > Export Data) and extract the `.zip`.
2. **Setup the folder:** Place your `conversations-00X.json` files in the same folder as `extract_chats.py`.
3. **Set your targets:** Open `targets.txt` and paste the exact titles of the chats you want to extract, one per line.
4. **Run the script:**

    python3 extract_chats.py

5. **Read your chats:** Open the newly generated `Extracted_ChatGPT_Chats.md` in your favorite Markdown viewer!

## 🛠 Requirements
- Python 3.x
- No external dependencies required (uses built-in `json`, `os`, and `glob` libraries).
