# RAG Document Q\&A (Chroma + Sentence Transformers + Groq)

A beginner-friendly Retrieval-Augmented Generation (RAG) project. It indexes a local corpus, stores embeddings in a persistent Chroma vector database, retrieves relevant passages for each question, displays those passages for inspection, and sends the retrieved context to an LLM for a grounded answer.

## Features

* Reads `.md`, `.txt`, and text-based `.pdf` files from `documents/`
* Chunks text into roughly 550-word passages with 80-word overlap
* Uses `sentence-transformers/all-MiniLM-L6-v2` embeddings locally
* Stores vectors and source metadata in local Chroma
* Retrieves the top 4 chunks and prints them before generation
* Calls Groq for the final answer; instructs the model to admit when the evidence is missing
* Includes a fictional CampusLab document with unique facts for the RAG-vs-baseline test

> Note: this starter chunker uses words as a practical approximation, not exact model tokens. Scanned PDFs need OCR and are not automatically processed.

## Requirements

* Python 3.10 or newer recommended
* Internet connection for first-time package/model download and Groq requests
* A Groq API key for generated answers. Create your own key through Groq's official console. Never publish it.

## Setup on Windows PowerShell

Run each command from the project folder:

```powershell
python -m venv .venv
.\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\.venv\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\Scripts\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` in a text editor and replace `paste\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_your\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_groq\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_api\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_key\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_here` with your own key. Keep `.env` private.

If PowerShell blocks virtual-environment activation, you can instead run the environment's Python directly:

```powershell
.\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\.venv\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\Scripts\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\python.exe -m pip install -r requirements.txt
.\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\.venv\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\Scripts\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\python.exe ingest.py
.\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\.venv\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\Scripts\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\python.exe app.py
```

## Index the documents

```powershell
python ingest.py
```

The first run downloads the embedding model, so it may take several minutes. The script creates `chroma\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_db/`, which is generated local data and is excluded from Git.

To add your own files, place `.md`, `.txt`, or text-based `.pdf` files under `documents/`, then rerun `python ingest.py`. Re-ingestion rebuilds the local index from all supported files.

## Ask questions

```powershell
python app.py
```

Try these questions:

* What was the internal codename for the October evaluation?
* How many rows were in the final validation dataset?
* How many duplicate submissions were removed?
* What was the planned acceptance target?
* What is the policy for information not found in the documents?

The app prints source filenames, chunk numbers, distances, and retrieved text so you can check whether the evidence is relevant.

## RAG vs plain LLM comparison (required evidence)

Use the private fictional fact in `documents/05\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_campuslab\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_case\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_study.md`. To make the comparison fair, ask the exact same question in a plain LLM chat with no project documents attached, then ask it through this RAG application.

**Question:** “What was the internal codename for the October evaluation in the CampusLab case study?”

* Plain LLM baseline: open a normal chat with the same model (or another clearly named baseline model), do not provide the document, ask the question, and copy its actual response below.
* RAG: run `python app.py`, ask the same question, and copy the actual response and retrieved source/chunk evidence below.
* Do not copy the expected answer into the baseline prompt. If the baseline happens to guess correctly, select another unique fact from the document and repeat the comparison.
* Record the date and model used. Do not claim results until you have run both tests.

### Observed results — fill in after running

|Field|Plain LLM baseline|RAG application|
|-|-|-|
|Date tested|Not run yet|Not run yet|
|Model|Fill in actual model|`GROQ\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_MODEL` value from `.env`|
|Actual output|Paste exact output here|Paste exact answer here|
|Evidence|No document supplied|Paste source filename and chunk number|
|Assessment|Did it know the private fact?|Did retrieved evidence support the answer?|

**Do not submit the table with placeholders.** Replace every placeholder with actual observed outputs, then add a short paragraph explaining whether retrieval improved the answer and whether the cited chunk supported it.

## Suggested README comparison paragraph template

After running both tests, complete this in your own words:

> I asked both systems the same question without giving the baseline model access to the CampusLab source. The plain model answered: “...”. The RAG system answered: “...” and retrieved `...` (chunk `...`). The retrieved passage \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\[did/did not] explicitly support the answer. This test \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\[did/did not] demonstrate an advantage from access to the document for this question. One limitation is that this is a small fictional corpus and a single question is not a full evaluation.

## Project structure

```text
rag-document-qa/
├── app.py
├── ingest.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── documents/
    ├── 01\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_python\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_fundamentals.md
    ├── 02\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_data\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_structures\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_and\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_functions.md
    ├── 03\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_files\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_errors\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_modules.md
    ├── 04\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_testing\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_and\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_retrieval.md
    └── 05\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_campuslab\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_case\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_study.md
```

## Push to GitHub

Create a new **public** repository named `rag-document-qa` on GitHub. Do not initialize it with another README if you are pushing this folder directly. From this folder:

```powershell
git init
git add .
git status
git commit -m "Build RAG document question answering project"
git branch -M main
git remote add origin https://github.com/YOUR\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_GITHUB\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_USERNAME/rag-document-qa.git
git push -u origin main
```

Before `git add`, verify `.env` is not present in the staged files. Replace `YOUR\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_GITHUB\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_USERNAME` with your GitHub username. After pushing, open the repository in a browser and verify the README and documents are visible.

## Troubleshooting

* **`GROQ\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_API\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_KEY` missing:** create `.env` from `.env.example` and add your own key.
* **No Chroma index:** run `python ingest.py` before `python app.py`.
* **Model download fails:** check internet connectivity and disk space; try again.
* **Package installation fails:** confirm Python version and that the virtual environment is active.
* **No relevant chunks:** check that source files contain selectable text, re-ingest, and try a more specific question.
* **PDF returns little or no text:** it may be scanned; OCR is not included in this starter project.

## Limitations

This is an educational prototype, not a production service. The project includes a custom evaluation script, but it is not a formal RAGAS benchmark. The word-based chunker is approximate, PDF extraction may lose layout, and retrieval can return irrelevant chunks. A language model can still make mistakes. Always inspect retrieved evidence and report only measurements actually obtained.



\## RAG vs Plain LLM Comparison



\### Test Question

What was the internal codename for the October evaluation in the CampusLab case study?



\### Plain LLM Result

The plain LLM could not verify the codename because the CampusLab case study document was not provided.



\### RAG System Result

The RAG system retrieved relevant information from `05\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_campuslab\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_case\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\_study.md` and returned the codename: \*\*Maple Finch\*\*.



\### Conclusion

The RAG system can retrieve relevant information from the provided documents and answer questions based on their content. The plain LLM did not have access to the case study document in this test.



\### Evidence

\- `evidence/Screenshot 2026-10-10 204320.png` — Document indexing output.

\- `evidence/Screenshot 2026-10-10 205449.png` — RAG answer and source.

\- `evidence/Screenshot 2026-10-10 210037.png` — Plain LLM comparison.

\- `evidence/Screenshot 2026-10-10 210951.png` — Validation dataset answer.

\- `evidence/Screenshot 2026-10-10 211432.png` — Acceptance target answer.

\- `evidence/Screenshot 2026-10-10 212927.png` — Not-found policy answer.

\## RAG Evaluation Results



\### Evaluation Method



The project was evaluated using a dataset of 20 test cases covering Python fundamentals, data structures, file handling, and RAG retrieval. A custom Groq LLM-as-judge evaluator measured answer faithfulness, answer relevancy, and the relevance of retrieved passages. Expected source hit rate was also calculated.



\*\*Evaluation date:\*\* October 13, 2026

\*\*Judge model:\*\* `openai/gpt-oss-120b`

\*\*Evaluation method:\*\* Custom LLM-as-judge; these are estimates, not official RAGAS metrics.



\### Results



| Metric | Result |

|---|---:|

| Total test cases | 20 |

| Successful evaluations | 19 |

| Failed evaluations | 1 |

| Average faithfulness | 98.26% |

| Average answer relevancy | 88.21% |

| Average context precision | 31.58% |

| Expected source hit rate | 84.21% |



The averages and source hit rate are calculated over the 19 successfully evaluated cases. Context precision represents the fraction of retrieved passages judged relevant to the question.



\### Evaluation Findings



The evaluator generally rated answers as faithful to the retrieved context. Answer relevancy was also high on average. However, context precision was comparatively low, indicating that some retrieved passages were not useful for answering their questions. Retrieval quality should be improved and tested further.



One test case failed because of an API connection error. A subsequent retry was blocked by the Groq token-per-day rate limit. The failed case is not included in the reported metric averages.



\### Evaluation Files



\- `evaluation\\\_dataset.json` — test questions, reference answers, and expected source information.

\- `evaluate\\\_rag.py` — runs the evaluation and saves detailed results and a summary.

\- `evaluation\\\_results.json` — individual answers, retrieved sources, and metric scores or errors.

\- `evaluation\\\_summary.json` — aggregate evaluation metrics.

\- `retry\\\_failed\\\_test.py` — retries failed evaluation cases.

\- `rebuild\\\_summary.py` — rebuilds the summary from saved results.

\- `evidence/` — screenshots documenting project tests and evaluation output.



\### Limitations



This is an educational prototype using a small document collection and a custom LLM-as-judge evaluator. Scores may vary with the judge model and its availability. The evaluation is not a formal RAGAS benchmark. Retrieval can include irrelevant passages, and additional tests are needed to assess robustness and improve retrieval quality.

