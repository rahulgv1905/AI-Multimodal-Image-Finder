
import os
import streamlit as st
import chromadb
import numpy as np
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from google.genai import Client, types
from dotenv import load_dotenv

# 1. INITIALIZATION
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = Client(api_key=GEMINI_API_KEY)

# Models from your Dashboard
EMBEDDING_MODEL = "gemini-embedding-2-preview" 
AGENT_MODEL = "gemini-1.5-flash" 

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="multimodal_rag")

# 2. CORE FUNCTIONS
def get_image_date(img_path):
    try:
        img = Image.open(img_path)
        exif = img._getexif()
        if exif:
            for tag, value in exif.items():
                if TAGS.get(tag) == 'DateTimeOriginal':
                    return str(value).split(" ")[0].replace(":", "-")
    except:
        return "Unknown"
    return "Unknown"

def get_multimodal_embedding(path: Path):
    """Generates vector and prints the first 10 dimensions to console."""
    data = path.read_bytes()
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=[types.Part.from_bytes(data=data, mime_type="image/jpeg")],
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
    )
    
    vector = result.embeddings[0].values
    
    # --- DEBUG PRINT FOR YOUR CHECK ---
    print(f"\n[API CHECK] Successfully embedded: {path.name}")
    print(f"[API CHECK] Vector Size: {len(vector)}")
    print(f"[API CHECK] First 10 dimensions: {vector[:10]}")
    print("-" * 30)
    
    return vector

def get_text_embedding(query: str):
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=[query],
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    return result.embeddings[0].values

def agent_date_filter(query):
    try:
        prompt = f"Identify if a month or year is mentioned in: '{query}'. Return ONLY YYYY-MM. If none, return NONE."
        response = client.models.generate_content(model=AGENT_MODEL, contents=prompt)
        text = response.text.strip().upper()
        if "NONE" in text or not text:
            return None
        return text.split()[0]
    except:
        return None

# 3. STREAMLIT UI
st.set_page_config(page_title="AI Image Finder", layout="wide")
st.title("📸 Multimodal Image Finder (Gemini Embedding 2)")

with st.sidebar:
    st.header("Admin")
    # Unique key added to prevent DuplicateId error
    if st.button("Index 'my_images' Folder", key="btn_index_images"):
        img_dir = Path("my_images")
        if img_dir.exists():
            image_files = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png")) + list(img_dir.glob("*.jpeg"))
            if not image_files:
                st.warning("Folder 'my_images' is empty!")
            else:
                prog = st.progress(0)
                for i, f in enumerate(image_files):
                    if not collection.get(ids=[str(f)])['ids']:
                        try:
                            # This will trigger the print to your terminal
                            vector = get_multimodal_embedding(f)
                            date_val = get_image_date(f)
                            collection.add(
                                ids=[str(f)],
                                embeddings=[vector],
                                metadatas=[{"file_path": str(f), "date": date_val}]
                            )
                        except Exception as e:
                            st.error(f"Quota error: {e}")
                            break
                    prog.progress((i + 1) / len(image_files))
                st.success("Indexing Finished!")
        else:
            st.error("Create a folder named 'my_images' first.")

user_query = st.text_input("Search for an image (e.g. 'volleyball at the beach'):")

if user_query:
    with st.spinner("Searching..."):
        try:
            query_vec = get_text_embedding(user_query)
            extracted_date = agent_date_filter(user_query)
            
            # Dynamic dictionary to avoid ChromaDB {} error
            search_params = {
                "query_embeddings": [query_vec],
                "n_results": 1
            }
            
            if extracted_date:
                search_params["where"] = {"date": {"$contains": extracted_date}}
                st.info(f"Filtering for date: {extracted_date}")

            results = collection.query(**search_params)

            if results['ids'] and len(results['ids'][0]) > 0:
                match_path = results['metadatas'][0][0]['file_path']
                st.subheader("Found Match!")
                st.image(match_path, use_container_width=True)
            else:
                st.warning("No matches found.")
        except Exception as e:
            st.error(f"Search failed: {e}")
