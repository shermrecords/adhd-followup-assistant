from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime
import os, uuid

from PyPDF2 import PdfReader
import docx

router = APIRouter()

# Setup Chroma client (persistent DB in ./rag_store)
CHROMA_PATH = "/opt/render/project/src/rag_store"
os.makedirs(CHROMA_PATH, exist_ok=True)

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(
    "general_rag",
    embedding_function=embedding_functions.DefaultEmbeddingFunction()
)

class TextIn(BaseModel):
    text: str
    source: str = "pasted"

def chunk_text(text: str, size: int = 500, overlap: int = 50):
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunk = words[i:i+size]
        chunks.append(" ".join(chunk))
        i += size - overlap
    return chunks

@router.post("/rag/upload_text")
async def upload_text(body: TextIn):
    chunks = chunk_text(body.text)
    ids = []
    for idx, ch in enumerate(chunks):
        ids.append(str(uuid.uuid4()))
        collection.add(
            documents=[ch],
            ids=[ids[-1]],
            metadatas=[{
                "source": body.source,
                "chunk": idx,
                "date": datetime.utcnow().isoformat()
            }]
        )
    return {"status": "ok", "chunks": len(chunks)}

@router.post("/rag/upload_file")
async def upload_file(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    raw = await file.read()
    text = ""

    if ext == ".pdf":
        with open("temp.pdf", "wb") as f: f.write(raw)
        reader = PdfReader("temp.pdf")
        text = "\n".join([p.extract_text() or "" for p in reader.pages])

    elif ext in [".docx", ".doc"]:
        with open("temp.docx", "wb") as f: f.write(raw)
        d = docx.Document("temp.docx")
        text = "\n".join([p.text for p in d.paragraphs])

    elif ext in [".txt"]:
        text = raw.decode("utf-8", errors="ignore")

    else:
        return {"error": "Unsupported file type"}

    chunks = chunk_text(text)
    ids = []
    for idx, ch in enumerate(chunks):
        ids.append(str(uuid.uuid4()))
        collection.add(
            documents=[ch],
            ids=[ids[-1]],
            metadatas=[{
                "source": file.filename,
                "chunk": idx,
                "date": datetime.utcnow().isoformat()
            }]
        )

    return {"status": "ok", "chunks": len(chunks)}

@router.get("/rag/list")
async def list_docs():
    # Note: Chroma doesn’t have perfect “list all docs” API,
    # so we just return collection count
    count = collection.count()
    return {"count": count, "collection": "general_rag"}

class SearchIn(BaseModel):
    query: str
    k: int = 3

@router.post("/rag/search")
async def search_docs(body: SearchIn):
    results = collection.query(query_texts=[body.query], n_results=body.k)
    return {"results": results}
