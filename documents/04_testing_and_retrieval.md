# Testing, Search Quality, and Retrieval-Augmented Generation

## 1. What retrieval-augmented generation means
Retrieval-augmented generation (RAG) combines information retrieval with a language model. Instead of asking the model to answer only from its trained knowledge, the application searches a supplied corpus and includes relevant passages in the prompt. The model then produces an answer based on that evidence. RAG can improve answers about private, recent, or domain-specific material, but it does not guarantee correctness.

A simple RAG workflow has five stages: load documents, split text into chunks, embed each chunk, retrieve relevant chunks for a question, and generate a response using the retrieved context. The system should preserve source metadata so a user can inspect where a claim came from.

## 2. Chunking
Chunking divides long documents into manageable units. A common starting point is 300–800 tokens per chunk with overlap between neighbouring chunks. Overlap helps preserve context across boundaries, but excessive overlap increases storage and can return near-duplicate passages. Chunk size should be evaluated against the content type and query patterns.

A heading-aware chunker may be better than a simple character split for manuals or reports. Tables, code blocks, and numbered procedures need special handling because a naive split can separate labels from their values. Keep each chunk's source name and, where available, page or section information.

## 3. Embeddings and vector stores
An embedding model maps text to a numeric vector. Semantically similar text can have vectors that are close under a chosen distance measure. A vector database stores vectors and metadata and supports similarity search. Chroma can run locally, which is convenient for experiments without a hosted database account. Pinecone is a hosted option for teams that need managed infrastructure.

Embedding models and vector stores solve different problems. The embedding model determines the representation; the vector store manages storage and retrieval. Replacing an embedding model usually requires re-embedding the corpus. Query embeddings must be produced by a compatible model.

## 4. Retrieval strategies
Top-k similarity search returns the k nearest chunks. A low k can omit needed evidence; a high k can add irrelevant context and consume prompt space. Metadata filters can restrict retrieval by document, date, or category. Hybrid retrieval combines lexical matching with semantic similarity and may help when queries contain exact IDs, rare names, or technical terms.

Inspect retrieved chunks manually. A search result is not useful merely because it is the nearest available passage. Build a small evaluation set with questions whose answers are known from the source documents. Measure whether the expected supporting passage appears in the top-k results.

## 5. Grounded generation
The generation prompt should clearly label the retrieved passages as context and instruct the model to answer only when evidence supports the claim. It should tell the model to say that the information was not found when the context is insufficient. Treat retrieved document text as data, not as trusted instructions; documents can contain malicious or irrelevant prompt-like text.

A good answer should distinguish direct evidence from inference. When possible, cite the source filename or chunk identifier. The model should not invent details to make an answer sound complete. Retrieval and generation both need testing.

## 6. Comparing RAG with a plain language model
A fair comparison uses the same question and records each system's actual output. Choose a fact that appears only in the supplied documents, such as a fictional internal project code or a specific dataset row count. A plain model without the document is unlikely to know the private fact, while RAG may retrieve the exact passage.

Do not write expected outputs as if they were observed results. Run the baseline and RAG pipeline, save the exact outputs, and note the date, model, and settings. If the baseline guesses correctly by chance, use another private fact and repeat the comparison. The purpose is to demonstrate evidence access, not to claim that every RAG answer is always better.

## 7. Evaluation dimensions
Useful evaluation dimensions include retrieval recall, relevance of retrieved chunks, answer correctness, groundedness, citation accuracy, latency, and cost. Retrieval recall asks whether the needed evidence was retrieved. Groundedness asks whether answer claims are supported by the retrieved text. These measures are related but not identical: a correct answer can be ungrounded, and relevant retrieval can still lead to a poor answer.

## 8. Common failure modes
A system may retrieve irrelevant chunks because the query is vague, the embedding model is unsuitable, or the corpus lacks the answer. The prompt may be too long, causing important passages to be truncated. Extracted PDF text may be incomplete. The model may ignore instructions or combine separate facts incorrectly. A robust application should expose retrieved evidence for debugging and return an honest not-found response when needed.

## 9. Privacy and access control
RAG does not automatically provide access control. If documents contain private information, the application must enforce user permissions before retrieval. Do not assume that a prompt instruction alone prevents data leakage. Store only data the application is permitted to process, and understand whether external model providers receive prompt content.

## 10. Practical checklist
For a credible RAG project, include real source documents, repeatable ingestion, chunk metadata, persistent vector storage, query-time retrieval, grounded generation, inspectable evidence, and a comparison against a plain model. Document limitations and show real output rather than screenshots or results invented for a report.


## 11. Prompt injection in retrieved documents
A retrieved passage might contain text such as “ignore the system prompt.” The application should treat this as document content, not as an instruction to follow. Delimit context clearly, instruct the model to follow application rules over retrieved text, and avoid giving the model unnecessary tools or permissions. Prompt wording alone is not a complete security boundary; enforce permissions in code.

## 12. Query rewriting
Users may ask vague questions or use alternate wording. A query-rewriting stage can convert a conversational question into a search-friendly query, but it adds latency and may remove important constraints. Keep the original user question for answer generation and inspect rewritten queries during evaluation. For simple corpora, direct embedding search may be sufficient.

## 13. Reranking
A reranker scores candidate passages for relevance to a specific query after an initial retrieval step. This can improve ordering when the vector search returns several plausible chunks. Reranking costs additional compute and should be evaluated against a baseline. It is not necessary for every small project; first establish that basic retrieval works.

## 14. Measuring retrieval
Create a test set containing a question, expected source document, and expected evidence phrase. Review whether the correct document appears in top-k results. Recall@k measures the proportion of queries for which the needed evidence appears among the first k results. Human relevance judgments are useful because a chunk may be related to the topic without actually supporting the answer.

## 15. Handling missing answers
If the corpus does not contain the answer, a system should say so rather than filling the gap with a plausible guess. Test this behaviour with questions about details intentionally absent from the source. A good not-found response is a successful outcome when evidence is unavailable. It protects trust and helps users understand the limits of the index.
