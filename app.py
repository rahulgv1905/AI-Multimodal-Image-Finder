# # # # # import os
# # # # # import streamlit as st
# # # # # import numpy as np
# # # # # import chromadb
# # # # # from pathlib import Path
# # # # # from PIL import Image
# # # # # from PIL.ExifTags import TAGS
# # # # # from google.genai import Client, types
# # # # # from datetime import datetime
# # # # # from dotenv import load_dotenv

# # # # # # --- INITIALIZATION ---
# # # # # load_dotenv()
# # # # # # If you don't use a .env file, paste your key directly here:
# # # # # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyC03XkmFj9jhoWlaTW69zKnNvJcs1u0HVc")

# # # # # client = Client(api_key=GEMINI_API_KEY)
# # # # # EMBEDDING_MODEL = "gemini-embedding-2-preview"

# # # # # # Initialize ChromaDB
# # # # # chroma_client = chromadb.PersistentClient(path="./chroma_db")
# # # # # collection = chroma_client.get_or_create_collection(name="multimodal_rag")

# # # # # # --- CORE FUNCTIONS ---

# # # # # def get_image_date(img_path):
# # # # #     """Extracts date from image metadata."""
# # # # #     try:
# # # # #         img = Image.open(img_path)
# # # # #         exif = img._getexif()
# # # # #         if exif:
# # # # #             for tag, value in exif.items():
# # # # #                 if TAGS.get(tag) == 'DateTimeOriginal':
# # # # #                     # Returns YYYY-MM-DD
# # # # #                     return value.split(" ")[0].replace(":", "-")
# # # # #     except:
# # # # #         return "Unknown"
# # # # #     return "Unknown"

# # # # # def get_multimodal_embedding(path: Path):
# # # # #     """Latest Gemini 2 Embedding logic for images."""
# # # # #     data = path.read_bytes()
# # # # #     result = client.models.embed_content(
# # # # #         model=EMBEDDING_MODEL,
# # # # #         contents=[
# # # # #             types.Part.from_bytes(data=data, mime_type="image/jpeg")
# # # # #         ],
# # # # #         config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
# # # # #     )
# # # # #     return result.embeddings[0].values

# # # # # def get_text_embedding(query: str):
# # # # #     """Latest Gemini 2 Embedding logic for text queries."""
# # # # #     result = client.models.embed_content(
# # # # #         model=EMBEDDING_MODEL,
# # # # #         contents=[query],
# # # # #         config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
# # # # #     )
# # # # #     return result.embeddings[0].values

# # # # # def agent_date_filter(query):
# # # # #     """Uses Gemini to extract date logic from the user query."""
# # # # #     prompt = f"Extract year/month from: '{query}'. Format YYYY-MM. If none, return NONE."
# # # # #     # Use Gemini 1.5 Flash for the 'Agent' reasoning part
# # # # #     response = client.models.generate_content(
# # # # #         model="gemini-1.5-flash", 
# # # # #         contents=prompt
# # # # #     )
# # # # #     return None if "NONE" in response.text.upper() else response.text.strip()

# # # # # # --- STREAMLIT UI ---

# # # # # st.set_page_config(page_title="AI Image Finder")
# # # # # st.title("📸 Multimodal RAG Image Finder")
# # # # # st.write("Using Gemini Embedding 2 & ChromaDB")

# # # # # with st.sidebar:
# # # # #     st.header("Database Management")
# # # # #     if st.button("Index 'images' Folder"):
# # # # #         image_folder = Path("images") # Ensure this folder exists
# # # # #         if not image_folder.exists():
# # # # #             st.error("Folder 'images' not found!")
# # # # #         else:
# # # # #             files = list(image_folder.glob("*.jpg")) + list(image_folder.glob("*.png"))
# # # # #             for f in files:
# # # # #                 if not collection.get(ids=[str(f)])['ids']:
# # # # #                     st.write(f"Indexing {f.name}...")
# # # # #                     vector = get_multimodal_embedding(f)
# # # # #                     date_meta = get_image_date(f)
# # # # #                     collection.add(
# # # # #                         ids=[str(f)],
# # # # #                         embeddings=[vector],
# # # # #                         metadatas=[{"file_path": str(f), "date": date_meta}]
# # # # #                     )
# # # # #             st.success("Indexing Complete!")

# # # # # query_text = st.text_input("Describe your image (e.g., '10 people playing volleyball in March')")

# # # # # if query_text:
# # # # #     with st.spinner("Agent searching..."):
# # # # #         # 1. Get embedding for the text query
# # # # #         query_vector = get_text_embedding(query_text)
        
# # # # #         # 2. Agent extracts the date for filtering
# # # # #         extracted_date = agent_date_filter(query_text)
        
# # # # #         where_clause = {}
# # # # #         if extracted_date:
# # # # #             where_clause = {"date": {"$contains": extracted_date}}
# # # # #             st.info(f"Filtering results for: {extracted_date}")

# # # # #         # 3. Query ChromaDB
# # # # #         results = collection.query(
# # # # #             query_embeddings=[query_vector],
# # # # #             n_results=1,
# # # # #             where=where_clause
# # # # #         )

# # # # #         if results['ids'][0]:
# # # # #             img_path = results['metadatas'][0][0]['file_path']
# # # # #             img_date = results['metadatas'][0][0]['date']
# # # # #             st.write(f"**Found Match!** Captured on: {img_date}")
# # # # #             st.image(img_path)
# # # # #         else:
# # # # #             st.warning("No images matched your description.")

# # # # import os
# # # # import streamlit as st
# # # # import numpy as np
# # # # import chromadb
# # # # from pathlib import Path
# # # # from PIL import Image
# # # # from PIL.ExifTags import TAGS
# # # # from google.genai import Client, types
# # # # from datetime import datetime
# # # # from dotenv import load_dotenv

# # # # load_dotenv()
# # # # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY","AIzaSyC03XkmFj9jhoWlaTW69zKnNvJcs1u0HVc")

# # # # client = Client(api_key=GEMINI_API_KEY)
# # # # # We use the family of 2.0 models for consistency
# # # # EMBEDDING_MODEL = "gemini-embedding-2-preview"
# # # # AGENT_MODEL = "gemini-2.0-flash" 

# # # # chroma_client = chromadb.PersistentClient(path="./chroma_db")
# # # # collection = chroma_client.get_or_create_collection(name="multimodal_rag")

# # # # def get_image_date(img_path):
# # # #     try:
# # # #         img = Image.open(img_path)
# # # #         exif = img._getexif()
# # # #         if exif:
# # # #             for tag, value in exif.items():
# # # #                 if TAGS.get(tag) == 'DateTimeOriginal':
# # # #                     return value.split(" ")[0].replace(":", "-")
# # # #     except:
# # # #         return "Unknown"
# # # #     return "Unknown"

# # # # def get_multimodal_embedding(path: Path):
# # # #     data = path.read_bytes()
# # # #     result = client.models.embed_content(
# # # #         model=EMBEDDING_MODEL,
# # # #         contents=[types.Part.from_bytes(data=data, mime_type="image/jpeg")],
# # # #         config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
# # # #     )
# # # #     return result.embeddings[0].values

# # # # def get_text_embedding(query: str):
# # # #     result = client.models.embed_content(
# # # #         model=EMBEDDING_MODEL,
# # # #         contents=[query],
# # # #         config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
# # # #     )
# # # #     return result.embeddings[0].values

# # # # def agent_date_filter(query):
# # # #     try:
# # # #         prompt = f"Identify if a month or year is mentioned in: '{query}'. If yes, return in YYYY-MM format. If no, return NONE."
# # # #         response = client.models.generate_content(model=AGENT_MODEL, contents=prompt)
# # # #         text = response.text.strip().upper()
# # # #         return None if "NONE" in text else text
# # # #     except Exception as e:
# # # #         # If the AI Agent fails, we don't want the whole app to crash
# # # #         print(f"Agent logic skipped: {e}")
# # # #         return None

# # # # # --- STREAMLIT UI ---
# # # # st.set_page_config(page_title="Multimodal Image Finder", layout="wide")
# # # # st.title("📸 Image Finder (Gemini 2.0 + ChromaDB)")

# # # # with st.sidebar:
# # # #     st.header("Admin")
# # # #     if st.button("Index 'images' Folder"):
# # # #         img_dir = Path("images")
# # # #         if img_dir.exists():
# # # #             image_files = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png")) + list(img_dir.glob("*.jpeg"))
# # # #             progress_bar = st.progress(0)
# # # #             for i, f in enumerate(image_files):
# # # #                 if not collection.get(ids=[str(f)])['ids']:
# # # #                     vector = get_multimodal_embedding(f)
# # # #                     date_val = get_image_date(f)
# # # #                     collection.add(
# # # #                         ids=[str(f)],
# # # #                         embeddings=[vector],
# # # #                         metadatas=[{"file_path": str(f), "date": date_val}]
# # # #                     )
# # # #                 progress_bar.progress((i + 1) / len(image_files))
# # # #             st.success(f"Indexed {len(image_files)} images!")
# # # #         else:
# # # #             st.error("Create an 'images' folder first!")

# # # # query_text = st.text_input("What are you looking for?", placeholder="e.g. 10 people playing volleyball at the beach")

# # # # if query_text:
# # # #     with st.spinner("Searching..."):
# # # #         # 1. Text Embedding (Usually has a higher quota than Flash)
# # # #         try:
# # # #             query_vec = get_text_embedding(query_text)
# # # #         except Exception as e:
# # # #             st.error("Embedding API Rate Limit Hit. Please wait 60 seconds and try again.")
# # # #             st.stop()
        
# # # #         # 2. Extract Date (Agent) - We wrap this so a 429 doesn't break the app
# # # #         extracted_date = None
# # # #         try:
# # # #             extracted_date = agent_date_filter(query_text)
# # # #         except Exception as e:
# # # #             # If the Agent fails (429 error), we just log it and move on
# # # #             print(f"Agent Quota Hit: {e}") 
# # # #             st.warning("AI Agent is resting (Rate Limit). Searching without date filter...")

# # # #         # 3. FIX: Build the where_clause correctly
# # # #         # We start with None. If Agent found a date, we build the dict.
# # # #         where_clause = None 
        
# # # #         if extracted_date and extracted_date != "NONE":
# # # #             where_clause = {"date": {"$contains": str(extracted_date)}}
# # # #             st.info(f"Filtering by Date: {extracted_date}")

# # # #         # 4. Chroma Search
# # # #         # If where_clause is None, Chroma performs a global search.
# # # #         results = collection.query(
# # # #             query_embeddings=[query_vec],
# # # #             n_results=1,
# # # #             where=where_clause 
# # # #         )

# # # #         if results['ids'][0]:
# # # #             path = results['metadatas'][0][0]['file_path']
# # # #             st.image(path, caption=f"Result: {path}")
# # # #         else:
# # # #             st.warning("No matches found.")

# # # import os
# # # import streamlit as st
# # # import numpy as np
# # # import chromadb
# # # from pathlib import Path
# # # from PIL import Image
# # # from PIL.ExifTags import TAGS
# # # from google.genai import Client, types
# # # from dotenv import load_dotenv

# # # # 1. INITIALIZATION
# # # load_dotenv()
# # # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY","AIzaSyC03XkmFj9jhoWlaTW69zKnNvJcs1u0HVc")
# # # client = Client(api_key=GEMINI_API_KEY)

# # # # Use 1.5-flash for the agent because it has much higher free-tier limits than 2.0
# # # EMBEDDING_MODEL = "gemini-embedding-2-preview"
# # # AGENT_MODEL = "gemini-1.5-flash" 

# # # chroma_client = chromadb.PersistentClient(path="./chroma_db")
# # # collection = chroma_client.get_or_create_collection(name="multimodal_rag")

# # # # 2. HELPER FUNCTIONS
# # # def get_image_date(img_path):
# # #     try:
# # #         img = Image.open(img_path)
# # #         exif = img._getexif()
# # #         if exif:
# # #             for tag, value in exif.items():
# # #                 if TAGS.get(tag) == 'DateTimeOriginal':
# # #                     return value.split(" ")[0].replace(":", "-")
# # #     except:
# # #         return "Unknown"
# # #     return "Unknown"

# # # def get_multimodal_embedding(path: Path):
# # #     data = path.read_bytes()
# # #     result = client.models.embed_content(
# # #         model=EMBEDDING_MODEL,
# # #         contents=[types.Part.from_bytes(data=data, mime_type="image/jpeg")],
# # #         config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
# # #     )
# # #     return result.embeddings[0].values

# # # def get_text_embedding(query: str):
# # #     result = client.models.embed_content(
# # #         model=EMBEDDING_MODEL,
# # #         contents=[query],
# # #         config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
# # #     )
# # #     return result.embeddings[0].values

# # # def agent_date_filter(query):
# # #     """Safely extracts date using AI. Returns None if it fails or hits quota."""
# # #     try:
# # #         prompt = f"Does this query mention a month or year: '{query}'? If yes, return ONLY YYYY-MM. If no, return NONE."
# # #         response = client.models.generate_content(model=AGENT_MODEL, contents=prompt)
# # #         text = response.text.strip().upper()
# # #         if "NONE" in text or not text:
# # #             return None
# # #         return text
# # #     except Exception as e:
# # #         # This catches the 429 error and prevents a crash
# # #         print(f"Agent logic skipped due to rate limit: {e}")
# # #         return None

# # # # 3. STREAMLIT UI
# # # st.set_page_config(page_title="Multimodal Image Finder", layout="wide")
# # # st.title("📸 Image Finder (FYP Edition)")

# # # with st.sidebar:
# # #     st.header("Admin")
# # #     if st.button("Index 'my_images' Folder"):
# # #         img_dir = Path("my_images")
# # #         if img_dir.exists():
# # #             image_files = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png")) + list(img_dir.glob("*.jpeg"))
# # #             prog = st.progress(0)
# # #             for i, f in enumerate(image_files):
# # #                 if not collection.get(ids=[str(f)])['ids']:
# # #                     vector = get_multimodal_embedding(f)
# # #                     date_val = get_image_date(f)
# # #                     collection.add(
# # #                         ids=[str(f)],
# # #                         embeddings=[vector],
# # #                         metadatas=[{"file_path": str(f), "date": date_val}]
# # #                     )
# # #                 prog.progress((i + 1) / len(image_files))
# # #             st.success("Indexing Finished!")
# # #         else:
# # #             st.error("Please create an 'images' folder.")
# # # # ... (rest of imports remains the same)

# # # with st.sidebar:
# # #     st.header("Setup")
# # #     if st.button("Index 'my_images' Folder"):
# # #         # UPDATED FOLDER NAME HERE
# # #         img_dir = Path("my_images") 
        
# # #         if img_dir.exists():
# # #             # Support all common formats
# # #             image_files = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png")) + list(img_dir.glob("*.jpeg"))
            
# # #             if len(image_files) == 0:
# # #                 st.warning("Folder 'my_images' is empty!")
            
# # #             prog = st.progress(0)
# # #             for i, f in enumerate(image_files):
# # #                 # Check if file is already in ChromaDB
# # #                 if not collection.get(ids=[str(f)])['ids']:
# # #                     try:
# # #                         # Use Gemini Embedding 2
# # #                         vector = get_multimodal_embedding(f)
# # #                         # Extract EXIF date
# # #                         date_val = get_image_date(f)
                        
# # #                         collection.add(
# # #                             ids=[str(f)],
# # #                             embeddings=[vector],
# # #                             metadatas=[{"file_path": str(f), "date": date_val}]
# # #                         )
# # #                     except Exception as e:
# # #                         st.error(f"Failed to index {f.name}: {e}")
# # #                         # If we hit a rate limit (429) during indexing, stop and warn
# # #                         if "429" in str(e):
# # #                             st.error("Rate limit hit! Wait 60 seconds before continuing.")
# # #                             break
# # #                 prog.progress((i + 1) / len(image_files))
# # #             st.success(f"Indexed {len(image_files)} images.")
# # #         else:
# # #             st.error("Folder 'my_images' not found. Please create it on your laptop.")

# # # # ... (rest of search logic remains the same)
# # # query_text = st.text_input("Describe your photo:", placeholder="e.g. 10 people playing volleyball")

# # # if query_text:
# # #     with st.spinner("Searching..."):
# # #         # STEP 1: Get Embedding (High priority)
# # #         try:
# # #             query_vec = get_text_embedding(query_text)
# # #         except Exception as e:
# # #             st.error("API Error: Rate limit hit. Please wait a minute.")
# # #             st.stop()

# # #         # STEP 2: Get Date Filter (Optional Agent)
# # #         extracted_date = agent_date_filter(query_text)
        
# # #         # CRITICAL FIX: Ensure where_clause is either a valid dict OR None. 
# # #         # Never let it be {}.
# # #         where_clause = None 
        
# # #         if extracted_date:
# # #             # Note: We use the simplest filter format to avoid Chroma parsing errors
# # #             where_clause = {"date": {"$contains": extracted_date}}
# # #             st.info(f"AI Agent is filtering for date: {extracted_date}")

# # #         # STEP 3: Query Chroma
# # #         try:
# # #             # We explicitly handle the where_clause here
# # #             results = collection.query(
# # #                 query_embeddings=[query_vec],
# # #                 n_results=1,
# # #                 where=where_clause # If where_clause is None, it works!
# # #             )

# # #             if results['ids'] and len(results['ids'][0]) > 0:
# # #                 match_path = results['metadatas'][0][0]['file_path']
# # #                 st.image(match_path, caption=f"Found: {match_path}")
# # #             else:
# # #                 st.warning("No images found for that description.")
                
# # #         except Exception as e:
# # #             st.error(f"Search Error: {e}")

# # import os
# # import streamlit as st
# # import chromadb
# # from pathlib import Path
# # from PIL import Image
# # from PIL.ExifTags import TAGS
# # from google.genai import Client, types
# # from dotenv import load_dotenv

# # # 1. INITIALIZATION (Matches your Dashboard)
# # load_dotenv()
# # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyC03XkmFj9jhoWlaTW69zKnNvJcs1u0HVc")
# # client = Client(api_key=GEMINI_API_KEY)

# # # Using your specific project's available models
# # EMBEDDING_MODEL = "gemini-embedding-2-preview" 
# # AGENT_MODEL = "gemini-1.5-flash" 

# # chroma_client = chromadb.PersistentClient(path="./chroma_db")
# # collection = chroma_client.get_or_create_collection(name="multimodal_rag")

# # # 2. HELPER FUNCTIONS
# # def get_image_date(img_path):
# #     try:
# #         img = Image.open(img_path)
# #         exif = img._getexif()
# #         if exif:
# #             for tag, value in exif.items():
# #                 if TAGS.get(tag) == 'DateTimeOriginal':
# #                     return str(value).split(" ")[0].replace(":", "-")
# #     except:
# #         return "Unknown"
# #     return "Unknown"

# # def get_multimodal_embedding(path: Path):
# #     """Uses Embedding 2 (100 RPM Limit)"""
# #     data = path.read_bytes()
# #     result = client.models.embed_content(
# #         model=EMBEDDING_MODEL,
# #         contents=[types.Part.from_bytes(data=data, mime_type="image/jpeg")],
# #         config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
# #     )
# #     return result.embeddings[0].values

# # def get_text_embedding(query: str):
# #     result = client.models.embed_content(
# #         model=EMBEDDING_MODEL,
# #         contents=[query],
# #         config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
# #     )
# #     return result.embeddings[0].values

# # def agent_date_filter(query):
# #     """Uses 1.5 Flash (15 RPM Limit)"""
# #     try:
# #         prompt = f"Identify if a month or year is mentioned in: '{query}'. Return ONLY YYYY-MM. Else return NONE."
# #         response = client.models.generate_content(model=AGENT_MODEL, contents=prompt)
# #         text = response.text.strip().upper()
# #         if "NONE" in text or not text:
# #             return None
# #         return text.split()[0]
# #     except Exception as e:
# #         # If we hit the 15 RPM limit, we just skip the date filter
# #         return None

# # # 3. UI LOGIC
# # st.title("📸 Image Finder")

# # with st.sidebar:
# #     # UPDATED FOLDER NAME
# #     if st.button("Index 'my_images' Folder"):
# #         img_dir = Path("my_images")
# #         if img_dir.exists():
# #             image_files = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png")) + list(img_dir.glob("*.jpeg"))
# #             prog = st.progress(0)
# #             for i, f in enumerate(image_files):
# #                 if not collection.get(ids=[str(f)])['ids']:
# #                     try:
# #                         vector = get_multimodal_embedding(f)
# #                         date_val = get_image_date(f)
# #                         collection.add(
# #                             ids=[str(f)],
# #                             embeddings=[vector],
# #                             metadatas=[{"file_path": str(f), "date": date_val}]
# #                         )
# #                     except Exception as e:
# #                         st.error(f"Quota issue during indexing: {e}")
# #                         break # Stop if we hit 100 RPM
# #                 prog.progress((i + 1) / len(image_files))
# #             st.success("Indexing complete!")

# # query_text = st.text_input("Find an image:")

# # if query_text:
# #     # Generate vector (Embedding 2)
# #     query_vec = get_text_embedding(query_text)
    
# #     # Extract date (Agent 1.5 Flash)
# #     extracted_date = agent_date_filter(query_text)
    
# #     # DYNAMIC SEARCH LOGIC (Fixes the ValueError {})
# #     search_params = {"query_embeddings": [query_vec], "n_results": 1}
    
# #     if extracted_date:
# #         search_params["where"] = {"date": {"$contains": extracted_date}}
# #         st.info(f"Agent filtered by date: {extracted_date}")

# #     # Final Query
# #     results = collection.query(**search_params)

# #     if results['ids'] and len(results['ids'][0]) > 0:
# #         match_path = results['metadatas'][0][0]['file_path']
# #         st.image(match_path)
# #     else:
# #         st.warning("No matches found.")

# import os
# import streamlit as st
# import chromadb
# from pathlib import Path
# from PIL import Image
# from PIL.ExifTags import TAGS
# from google.genai import Client, types
# from dotenv import load_dotenv

# # 1. INITIALIZATION
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY","AIzaSyC03XkmFj9jhoWlaTW69zKnNvJcs1u0HVc")
# client = Client(api_key=GEMINI_API_KEY)

# # Using models confirmed by your dashboard
# EMBEDDING_MODEL = "gemini-embedding-2-preview" 
# AGENT_MODEL = "gemini-1.5-flash" 

# # Setup Database
# chroma_client = chromadb.PersistentClient(path="./chroma_db")
# collection = chroma_client.get_or_create_collection(name="multimodal_rag")

# # 2. CORE FUNCTIONS
# def get_image_date(img_path):
#     """Extracts date from image EXIF data."""
#     try:
#         img = Image.open(img_path)
#         exif = img._getexif()
#         if exif:
#             for tag, value in exif.items():
#                 if TAGS.get(tag) == 'DateTimeOriginal':
#                     # Format: 2026:03:14 02:04:16 -> 2026-03-14
#                     return str(value).split(" ")[0].replace(":", "-")
#     except:
#         return "Unknown"
#     return "Unknown"

# def get_multimodal_embedding(path: Path):
#     """Generates vector from image pixels."""
#     data = path.read_bytes()
#     result = client.models.embed_content(
#         model=EMBEDDING_MODEL,
#         contents=[types.Part.from_bytes(data=data, mime_type="image/jpeg")],
#         config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
#     )
#     return result.embeddings[0].values

# def get_text_embedding(query: str):
#     """Generates vector from search text."""
#     result = client.models.embed_content(
#         model=EMBEDDING_MODEL,
#         contents=[query],
#         config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
#     )
#     return result.embeddings[0].values

# def agent_date_filter(query):
#     """Uses AI to find a date in the query. Returns None if it fails."""
#     try:
#         prompt = f"Identify if a month or year is mentioned in: '{query}'. Return ONLY YYYY-MM. If none, return NONE."
#         response = client.models.generate_content(model=AGENT_MODEL, contents=prompt)
#         text = response.text.strip().upper()
#         if "NONE" in text or not text:
#             return None
#         return text.split()[0] # Take only the first word to be safe
#     except:
#         return None

# # 3. STREAMLIT UI
# st.set_page_config(page_title="AI Image Finder", layout="wide")
# st.title("📸 AI Multimodal Image Finder")

# # Sidebar for indexing
# with st.sidebar:
#     st.header("Admin Panel")
#     # Added unique 'key' to fix StreamlitDuplicateElementId
#     if st.button("Index 'my_images' Folder", key="index_button_unique"):
#         img_dir = Path("my_images")
#         if img_dir.exists():
#             image_files = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png")) + list(img_dir.glob("*.jpeg"))
#             if not image_files:
#                 st.warning("Folder 'my_images' is empty!")
#             else:
#                 prog = st.progress(0)
#                 for i, f in enumerate(image_files):
#                     # Only index if not already in DB
#                     if not collection.get(ids=[str(f)])['ids']:
#                         try:
#                             vector = get_multimodal_embedding(f)
#                             date_val = get_image_date(f)
#                             collection.add(
#                                 ids=[str(f)],
#                                 embeddings=[vector],
#                                 metadatas=[{"file_path": str(f), "date": date_val}]
#                             )
#                         except Exception as e:
#                             st.error(f"Quota error: Indexing stopped. {e}")
#                             break
#                     prog.progress((i + 1) / len(image_files))
#                 st.success("Indexing Finished!")
#         else:
#             st.error("Please create a folder named 'my_images' first.")

# # Main Search Area
# user_query = st.text_input("Describe your photo:", placeholder="e.g. 10 people playing volleyball at the beach in March")

# if user_query:
#     with st.spinner("Searching database..."):
#         try:
#             # Step 1: Text Embedding (Gemini 2)
#             query_vec = get_text_embedding(user_query)
            
#             # Step 2: Date Extraction (Agent 1.5 Flash)
#             extracted_date = agent_date_filter(user_query)
            
#             # Step 3: BUILD THE SEARCH DICTIONARY
#             # We ONLY add "where" if extracted_date is found.
#             # This is the ONLY way to prevent ChromaDB from getting {}
#             search_params = {
#                 "query_embeddings": [query_vec],
#                 "n_results": 1
#             }
            
#             if extracted_date:
#                 search_params["where"] = {"date": {"$contains": extracted_date}}
#                 st.info(f"AI Agent is filtering results for date: {extracted_date}")

#             # Step 4: Final Search
#             results = collection.query(**search_params)

#             if results['ids'] and len(results['ids'][0]) > 0:
#                 match_path = results['metadatas'][0][0]['file_path']
#                 st.subheader("Match Found!")
#                 st.image(match_path, use_container_width=True)
#                 st.caption(f"Path: {match_path}")
#             else:
#                 st.warning("No images match that description.")

#         except Exception as e:
#             st.error(f"Search failed. You might have hit a rate limit. Error: {e}")

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
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyC03XkmFj9jhoWlaTW69zKnNvJcs1u0HVc")
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