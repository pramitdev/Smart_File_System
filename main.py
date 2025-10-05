# main.py
import os
from watcher import start_watcher
from extractor import extract_snippet
from ai_client import get_tags_openai, get_tags_fallback
import db

WATCH_FOLDER = "watch_folder"
USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))

def process_new_file(path):
    print("[Main] New file detected:", path)
    snippet = extract_snippet(path, max_chars=1200)
    if not snippet:
        print("[Main] No extractable text from:", path, "— skipping AI tagging.")
        return
    # Try OpenAI if available
    tags = None
    if USE_OPENAI:
        tags = get_tags_openai(snippet)
    # fallback to local heuristics if OpenAI not available or failed
    if not tags:
        tags = get_tags_fallback(snippet)
    print("[Main] Tags for", os.path.basename(path), "->", tags)
    db.save_tags(path, tags)

if __name__ == "__main__":
    # ensure DB and watch folder exist
    db.init_db()
    if not os.path.exists(WATCH_FOLDER):
        os.makedirs(WATCH_FOLDER)
        print(f"[Main] Created watch folder: {WATCH_FOLDER}")
    print("[Main] Starting watcher. Drop .txt/.pdf/.docx files into the folder:", WATCH_FOLDER)
    start_watcher(WATCH_FOLDER, process_new_file)
