# AI Multimodal Image Finder 📸 🤖

### Built with Gemini Embedding 2 & Agentic RAG

## 🌟 The Problem
As our personal photo galleries grow into thousands of images, finding a specific memory becomes impossible. Traditional search relies on filenames (like `IMG_5432.jpg`) or manual tagging. This project solves that by allowing users to search their local image database using natural language, understanding both **visual content** and **temporal context (metadata)**.

## 🚀 Features
- **Multimodal Search:** Uses Google's `gemini-embedding-2-preview` to map text and images into the same 3072-dimensional vector space.
- **Agentic Metadata Filtering:** Uses Gemini 1.5 Flash as an agent to extract date/time intent from natural language queries (e.g., "in March").
- **Efficient Vector Storage:** Utilizes **ChromaDB** for persistent local storage and fast similarity retrieval.
- **EXIF Integration:** Automatically extracts "Date Taken" from image metadata to allow precise filtering.

## 🛠️ Tech Stack
- **AI Models:** Google Gemini Embedding 2, Gemini 1.5 Flash
- **Vector Database:** ChromaDB
- **Frontend:** Streamlit
- **Language:** Python 3.10+

## 📐 Architecture
1. **Indexing:** Images are processed via Gemini Embedding 2 to generate vectors and EXIF data is extracted for metadata. Both are stored in ChromaDB.
2. **Retrieval:** 
   - An LLM Agent parses the user query for date filters.
   - The query is converted into a vector.
   - ChromaDB performs a "where-filtered" similarity search.
3. **Display:** The best match is retrieved and displayed via Streamlit.

## ⚙️ Setup Instructions
1. Clone the repository: `git clone https://github.com/yourusername/AI-Multimodal-Image-Finder.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file and add your `GEMINI_API_KEY`.
4. Place your photos in the `my_images/` folder.
5. Run the app: `streamlit run app.py`

---
*Developed as a Final Year Project exploring Multimodal RAG and AI Agents.*