
"""Load documents, split them into chunks, and build a lightweight TF-IDF index."""
from pathlib import Path
import json
import re

from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer

ROOT = Path(__file__).parent
DOCS = ROOT / "documents"
INDEX_FILE = ROOT / "tfidf_index.json"
CHUNK_WORDS = 550
OVERLAP_WORDS = 80
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


def chunk_text(text, size=CHUNK_WORDS, overlap=OVERLAP_WORDS):
    words = text.split()
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
    paths = sorted(
        p for p in DOCS.rglob("*")
        if p.is_file() and p.suffix.lower() in SUPPORTED
    )
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

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
        max_features=30000,
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9_-]+\b",
    )
    matrix = vectorizer.fit_transform([r["text"] for r in records])

    index_data = {
        "records": records,
        "vocabulary": {k: int(v) for k, v in vectorizer.vocabulary_.items()},
        "idf": vectorizer.idf_.tolist(),
        "matrix": matrix.toarray().tolist(),
    }
    INDEX_FILE.write_text(
        json.dumps(index_data),
        encoding="utf-8",
    )

    print(f"Indexed {len(records)} chunks from {len(paths)} documents.")
    print(f"Saved lightweight TF-IDF index to: {INDEX_FILE}")


if __name__ == "__main__":
    main()
