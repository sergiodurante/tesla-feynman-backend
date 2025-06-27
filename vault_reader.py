
import os
import json

VAULT_PATH = "shared_knowledge_base"
INDEX_FILE = os.path.join(VAULT_PATH, "index.json")

def query_vault(keyword, max_results=3):
    print(f"🔍 [Vault] Query received: '{keyword}'")
    results = []

    if not os.path.exists(INDEX_FILE):
        print("⚠️ [Vault] Index file not found.")
        return ""

    with open(INDEX_FILE, "r") as f:
        index = json.load(f)

    for filename, meta in index.items():
        searchable_text = (meta.get("title", "") + " " +
                           meta.get("summary", "") + " " +
                           " ".join(meta.get("tags", []))).lower()
        print(f"📁 [Vault] Searching in: {filename}")
        print(f"🔍 [Vault] Searchable text: {searchable_text}")

        if keyword.lower() in searchable_text:
            full_path = os.path.join(VAULT_PATH, filename)
            print(f"✅ [Vault] Match found in: {filename}")
            if os.path.exists(full_path):
                with open(full_path, "r", encoding="utf-8", errors="ignore") as doc:
                    snippet = doc.read(1000)
                results.append(f"📄 *{meta['title']}* ({filename})\n{snippet.strip()}\n")
            else:
                print(f"⚠️ [Vault] File {filename} not found.")

        if len(results) >= max_results:
            break

    if results:
        print(f"✅ [Vault] Returning {len(results)} result(s).")
        return "\n---\n".join(results)
    else:
        print("🤖 [Vault] No results found.")
        return ""
def lookup_call_status(query_term):
    status_file = os.path.join(VAULT_PATH, "calls_status.json")
    if not os.path.exists(status_file):
        return None

    try:
        with open(status_file, "r") as f:
            calls_data = json.load(f)

        for call_code, call_info in calls_data.items():
            if query_term.lower() in call_info["topic"].lower():
                return {
                    "code": call_code,
                    "topic_id": call_info["topic_id"],
                    "deadline": call_info["deadline"],
                    "status": call_info["status"]
                }
        return None
    except Exception as e:
        print(f"❌ Error reading calls_status.json: {e}")
        return None
