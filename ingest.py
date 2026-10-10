"""Load local source documents, chunk them, embed them, and store them in Chroma."""
from pathlib import Path
import shutil

import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

ROOT = Path(__file__).parent
DOCS = ROOT / "documents"
DB_DIR = ROOT / "chroma_db"
COLLECTION_NAME = "rag_documents"
CHUNK_WORDS = 550
OVERLAP_WORDS = 80
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
SUPPORTED = {".txt", ".md", ".pdf"}


def read_document(path: Path):
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                yield f"[Page {page_num}]\n{text}"
    else:
        text = path.read_text(encoding="utf-8", errors="replace")
        if text.strip():
            yield text


def chunk_text(text: str, size: int = CHUNK_WORDS, overlap: int = OVERLAP_WORDS):
    words = text.split()
    if not words:
        return []
    chunks = []
    step = max(1, size - overlap)
    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start + size])
        if chunk:
            chunks.append(chunk)
        if start + size >= len(words):
            break
    return chunks


def main():
    paths = sorted(p for p in DOCS.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED)
    if not paths:
        raise SystemExit(f"No .txt, .md, or .pdf files found in {DOCS}")

    records = []
    for path in paths:
        for section_num, text in enumerate(read_document(path), start=1):
            for chunk_num, chunk in enumerate(chunk_text(text), start=1):
                records.append({
                    "id": f"{path.name}::s{section_num}::c{chunk_num}",
                    "text": chunk,
                    "source": path.name,
                    "chunk": chunk_num,
                    "section": section_num,
                })

    if not records:
        raise SystemExit("No readable text found. Check your documents.")

    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = model.encode([r["text"] for r in records], normalize_embeddings=True, show_progress_bar=True)
    if DB_DIR.exists():
        shutil.rmtree(DB_DIR)
    client = chromadb.PersistentClient(path=str(DB_DIR))
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    batch_size = 64
    for start in range(0, len(records), batch_size):
        batch = records[start:start + batch_size]
        vectors = embeddings[start:start + batch_size].tolist()
        collection.add(
            ids=[r["id"] for r in batch],
            documents=[r["text"] for r in batch],
            metadatas=[{"source": r["source"], "chunk": r["chunk"], "section": r["section"]} for r in batch],
            embeddings=vectors,
        )
    total_words = sum(len(r["text"].split()) for r in records)
    print(f"Indexed {len(records)} chunks from {len(paths)} documents.")
    print(f"Approximate indexed words (including overlap): {total_words:,}")
    print(f"Chroma database saved to: {DB_DIR}")


if __name__ == "__main__":
    main()
