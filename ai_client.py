# ai_client.py
import os

# Option A: OpenAI API (if OPENAI_API_KEY env var present)
def get_tags_openai(snippet):
    try:
        import openai
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("OPENAI_API_KEY not set")
        openai.api_key = key
        prompt = (
            "You are a helpful assistant. Read the snippet and return up to 5 short category tags "
            "separated by commas. Use compact tags like: report, todo list, lecture notes, invoice, email, code, recipe, meeting notes.\n\n"
            f"SNIPPET:\n{snippet}\n\nTAGS:"
        )
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}],
            temperature=0.0,
            max_tokens=60
        )
        text = resp["choices"][0]["message"]["content"].strip()
        # Normalize into list
        parts = []
        for part in text.replace("\n", ",").split(","):
            p = part.strip().lower()
            if p:
                parts.append(p)
        return parts[:5]
    except Exception as e:
        print("[ai_client] OpenAI tagging error:", e)
        return None

# Option B: Simple offline fallback
def get_tags_fallback(snippet):
    s = (snippet or "").lower()
    tags = set()
    # a few heuristics
    if any(w in s for w in ["todo", "to-do", "task", "tasks", "checklist"]):
        tags.add("todo list")
    if any(w in s for w in ["lecture", "professor", "lecture notes", "slides", "syllabus", "exam"]):
        tags.add("lecture notes")
    if any(w in s for w in ["abstract", "introduction", "conclusion", "report", "analysis"]):
        tags.add("report")
    if any(w in s for w in ["invoice", "amount due", "bill", "invoice number"]):
        tags.add("invoice")
    if any(w in s for w in ["recipe", "ingredients", "cook", "bake"]):
        tags.add("recipe")
    if any(w in s for w in ["error:", "stack trace", "def ", "function", "class ", "import "]):
        tags.add("code")
    if any(w in s for w in ["meeting", "minutes", "attendees", "agenda"]):
        tags.add("meeting notes")
    if not tags:
        tags.add("misc")
    return list(tags)
