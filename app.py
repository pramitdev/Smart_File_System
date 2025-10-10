import os
import threading
import time
import pandas as pd
import streamlit as st

# Import your backend modules
import main
import extractor
import watcher
import db

st.set_page_config(page_title="Smart File System", page_icon="🧠", layout="wide")

# --- Utility functions ---
def refresh_data():
    """Fetch all tag data from the DB"""
    try:
        data = db.get_all_tags()  # You’ll need to define this in db.py
        return pd.DataFrame(data, columns=["File Path", "Tag", "Last Updated"])
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=["File Path", "Tag", "Last Updated"])


def start_watcher_thread(path):
    """Run file watcher in a background thread"""
    def watch_folder():
        st.session_state["watching"] = True
        watcher.start_monitoring(path)
    thread = threading.Thread(target=watch_folder, daemon=True)
    thread.start()


# --- Sidebar Navigation ---
st.sidebar.title("🗂 Smart File System")
menu = st.sidebar.radio("Navigate", ["Dashboard", "Scan Folder", "View Tags", "Add Tag", "Watcher", "About"])

# --- Dashboard ---
if menu == "Dashboard":
    st.title("🧠 Smart File System")
    st.markdown("A system that organizes and tags your files intelligently.")
    st.info("Use the sidebar to scan folders, view tags, or start the watcher.")

# --- Scan Folder ---
elif menu == "Scan Folder":
    st.header("📁 Scan a Folder for Files")
    folder = st.text_input("Enter the path of the folder you want to scan:")
    if st.button("Start Scan"):
        if os.path.exists(folder):
            with st.spinner("Scanning files..."):
                try:
                    results = extractor.extract_from_folder(folder)  # adjust per your code
                    main.process_files(results)
                    st.success("✅ Scan complete! Tags updated.")
                except Exception as e:
                    st.error(f"Error scanning folder: {e}")
        else:
            st.warning("That path doesn’t exist.")

# --- View Tags ---
elif menu == "View Tags":
    st.header("🏷 View File Tags")
    df = refresh_data()
    if df.empty:
        st.info("No data found. Try scanning a folder first.")
    else:
        search = st.text_input("Search files or tags:")
        if search:
            df = df[df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]
        st.dataframe(df, use_container_width=True)

# --- Add Tag ---
elif menu == "Add Tag":
    st.header("➕ Add or Update a Tag")
    file_path = st.text_input("File path:")
    tag = st.text_input("Tag:")
    if st.button("Save Tag"):
        try:
            db.add_or_update_tag(file_path, tag)  # define in db.py
            st.success(f"Tag '{tag}' added to {file_path}")
        except Exception as e:
            st.error(f"Error saving tag: {e}")

# --- Watcher ---
elif menu == "Watcher":
    st.header("👀 Real-Time Folder Watcher")
    path = st.text_input("Enter folder path to monitor:")
    if st.button("Start Watcher"):
        if os.path.exists(path):
            start_watcher_thread(path)
            st.success(f"Watcher started for: {path}")
        else:
            st.warning("Invalid path.")
    if st.button("Stop Watcher"):
        watcher.stop_monitoring()
        st.info("Watcher stopped.")

# --- About ---
elif menu == "About":
    st.header("📖 About This Project")
    st.markdown("""
    **Smart File System** helps you:
    - Automatically organize and tag files.  
    - Monitor directories for changes.  
    - Add and edit tags through a simple interface.  
    - Integrate AI for smarter insights (optional).  
    
    """)
