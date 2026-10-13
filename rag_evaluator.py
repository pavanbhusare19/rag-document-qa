
"""Reusable RAG pipeline for automatic evaluation."""

from pathlib import Path
import os

import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).parent
DB_DIR = ROOT / "chroma_db"
COLLECTION_NAME = "rag_documents"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 4

SYSTEM_PROMPT = """You are a careful document question-answering assistant.
Answer only using the supplied retrieved context. If evidence is insufficient,
say: 'I could not find that information in the indexed documents.'
Do not invent facts. Mention supporting source filenames."""


class RAGEvaluator:
    def __init__(self):
        load_dotenv(ROOT / ".env")

        api_key = os.getenv("GROQ_API_KEY", "").strip()
        if not api_key or api_key == "paste_your_groq_api_key_here":
            raise RuntimeError("Set GROQ_API_KEY in your .env file.")

        client = chromadb.PersistentClient(path=str(DB_DIR))
        self.collection = client.get_collection(COLLECTION_NAME)
        self.embedder = SentenceTransformer(EMBEDDING_MODEL)
        self.llm = Groq(api_key=api_key)
        self.model_name = os.getenv(
            "GROQ_MODEL", "llama-3.3-70b-versatile"
        )

    def answer(self, question):
        embedding = self.embedder.encode(
            [question], normalize_embeddings=True
        )[0].tolist()

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=min(TOP_K, self.collection.count()),
            include=["documents", "metadatas", "distances"],
        )

        docs = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        contexts = []
        for doc, meta in zip(docs, metadatas):
            source = meta.get("source", "unknown")
            contexts.append({
                "text": doc,
                "source": source,
            })

        if not contexts:
            return {
                "answer": "I could not find that information in the indexed documents.",
                "contexts": [],
            }

        context_text = "\n\n".join(
            f"[Source: {item['source']}]\n{item['text']}"
            for item in contexts
        )

        response = self.llm.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Question:\n{question}\n\n"
                        f"Retrieved context:\n{context_text}\n\n"
                        "Answer concisely using only evidence in the context. "
                        "Cite source filenames."
                    ),
                },
            ],
            temperature=0,
        )

        answer = response.choices[0].message.content or ""
        return {"answer": answer, "contexts": contexts}


if __name__ == "__main__":
    rag = RAGEvaluator()
    result = rag.answer("Why are virtual environments useful in Python?")
    print("Answer:", result["answer"])
    print("Retrieved sources:", [c["source"] for c in result["contexts"]])
