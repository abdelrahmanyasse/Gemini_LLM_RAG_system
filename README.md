# Jarvis: Gemini RAG Chatbot

A command-line chatbot that answers questions using **Retrieval-Augmented Generation (RAG)**. Documents are split into chunks, embedded locally, and stored in a persistent ChromaDB vector store. At question time, the most relevant chunks are retrieved and passed to **Google Gemini** as context, so answers are grounded in your own documents instead of the model's general knowledge alone.

The default knowledge base describes my own ML projects, so Jarvis can answer questions about my work. You can swap in any `.txt` documents.

## How it works

```
 data/knowledge_base/*.txt
            │
            ▼
   ┌─────────────────┐   chunk (500 chars)   ┌──────────────────────┐
   │    ingest.py    │ ───────────────────▶  │ all-MiniLM-L6-v2     │
   └─────────────────┘                       │ (local embeddings)   │
                                             └──────────┬───────────┘
                                                        ▼
                                             ┌──────────────────────┐
                                             │ ChromaDB (./chroma_db)│
                                             └──────────┬───────────┘
                                                        │ top-3 chunks
 user question ──▶ Chatbot.py ── embed query ───────────┘
                       │
                       ▼
        prompt = retrieved context + question
                       │
                       ▼
              Gemini (gemini-2.0-flash-lite)
                       │
                       ▼
                    answer
```

1. **Ingest (`ingest.py`)**: loads every `.txt` file in `data/knowledge_base/`, splits it into 500-character chunks, embeds each chunk with `all-MiniLM-L6-v2`, and stores it in a persistent ChromaDB collection named `jarvis_knowledge`.
2. **Retrieve (`Chatbot.py`)**: the user's question is sanitized and embedded with the same model, and the 3 most similar chunks are fetched from ChromaDB.
3. **Generate (`Chatbot.py`)**: the retrieved chunks and the original question are combined into one prompt and sent to Gemini through a chat session, so the conversation history is kept. If the context doesn't contain the answer, the prompt tells the model to answer from its own knowledge.

## Tech stack

| Component | Tool |
|---|---|
| LLM | Google Gemini (`gemini-2.0-flash-lite`) via `google-generativeai` |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`), run locally |
| Vector store | ChromaDB (persistent, on disk) |
| Config | `python-dotenv` |

Embeddings run locally, so ingestion and retrieval use no API quota. Only the final answer generation calls the Gemini API.

## Project structure

```
.
├── Chatbot.py              # Interactive chat loop (retrieve → augment → generate)
├── ingest.py               # Builds the vector store from the knowledge base
├── test_retrieval.py       # Quick check that retrieval returns the right chunk
├── data/
│   └── knowledge_base/     # Your .txt documents go here
└── chroma_db/              # Persistent vector store (created by ingest.py)
```

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/abdelrahmanyasse/Gemini_LLM_RAG_system.git
cd Gemini_LLM_RAG_system
```

**2. Install dependencies**
```bash
pip install google-generativeai chromadb sentence-transformers python-dotenv
```

**3. Add your Gemini API key**

Get a key from [Google AI Studio](https://aistudio.google.com/) and create a `.env` file in the project root:
```
GEMINI_API_KEY=your_api_key_here
```

**4. Build the vector store**

Put your `.txt` files in `data/knowledge_base/`, then run:
```bash
python ingest.py
```

**5. Start chatting**
```bash
python Chatbot.py
```
Type `exit`, `quit`, `bye`, or `goodbye` to end the session.

## Example

Knowledge base content (`data/knowledge_base/test.txt`) includes facts about my projects, such as a face verification system with 98.60% accuracy and an AUC of 0.9957. Asking Jarvis:

```
You: what accuracy did the face verification project achieve
Jarvis: <answer grounded in the retrieved chunk>
```

To check retrieval on its own, without calling Gemini:
```bash
python test_retrieval.py
```

## Known limitations

- **Fixed-size chunking.** Text is split every 500 characters, which can cut sentences in half. Sentence- or paragraph-aware splitting with some overlap would retrieve better.
- **Re-running ingestion.** Chunk IDs are `chunk_0`, `chunk_1`, and so on, so running `ingest.py` again after changing the documents won't cleanly replace old chunks. Delete `chroma_db/` first to rebuild from scratch.
- **Plain-text only.** Only `.txt` files are loaded for now.
- **Small knowledge base.** The sample data is a single short file, so retrieval is only lightly tested.

## Roadmap

- [ ] Support PDF and DOCX documents (official documents, reports)
- [ ] Better chunking with overlap
- [ ] Show the source chunk used for each answer
- [ ] Add a `requirements.txt` and a web UI (Streamlit or Gradio)
- [ ] Connect it to my job recommendation engine (TF-IDF + cosine similarity) so it can answer career questions grounded in real documents

## Author

**Abdelrahman**, ML / Computer Vision engineer based in Cairo, Egypt.
