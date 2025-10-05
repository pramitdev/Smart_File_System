# cli.py
import argparse
import db

def cmd_search(tag):
    rows = db.search_by_tag(tag)
    if not rows:
        print("No files found with tag:", tag)
        return
    for path, tags in rows:
        print(path, "->", tags)

def cmd_show(file_path):
    tags = db.get_tags(file_path)
    if not tags:
        print("No tags for", file_path)
    else:
        print("Tags for", file_path, ":", tags)

def cmd_list_all():
    # helper: show entire DB (small)
    conn = __import__("sqlite3").connect(db.DB_PATH)
    c = conn.cursor()
    c.execute("SELECT file_path, tags FROM file_tags")
    rows = c.fetchall()
    conn.close()
    if not rows:
        print("No records in DB.")
        return
    for p, t in rows:
        print(p, "->", t)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart FS CLI")
    parser.add_argument("--search", "-s", help="search by tag")
    parser.add_argument("--show", "-f", help="show tags for file path")
    parser.add_argument("--list", action="store_true", help="list all indexed files")
    args = parser.parse_args()
    db.init_db()
    if args.search:
        cmd_search(args.search)
    elif args.show:
        cmd_show(args.show)
    elif args.list:
        cmd_list_all()
    else:
        parser.print_help()
