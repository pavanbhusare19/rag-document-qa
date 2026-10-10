# Files, Exceptions, Modules, and Configuration

## 1. Reading and writing files
Python's `open()` function supports file operations. Prefer a context manager:
```python
with open("notes.txt", "r", encoding="utf-8") as file:
    content = file.read()
```
The `with` block ensures the file is closed even if an error occurs. Specify the encoding for text files so behaviour is predictable across environments. Use `pathlib.Path` for readable path manipulation.

Reading an entire file is convenient for small files. For large files, process line by line or in chunks to reduce memory usage. When writing output, understand whether the selected mode overwrites (`w`), appends (`a`), or reads (`r`). An accidental overwrite can destroy useful data.

## 2. Exceptions
Exceptions represent failures or unusual conditions. Catch a specific exception when the program can meaningfully recover. A broad `except Exception` around an entire application can hide defects and make debugging difficult. If an exception cannot be handled locally, allow it to propagate or log it with context and re-raise it.

Error messages shown to users should be understandable. Technical details belong in controlled logs, not in public responses. Never include API keys, passwords, or full private records in error messages.

## 3. Modules and packages
A module is a Python file that can be imported. A package groups modules in a directory. Separate code by responsibility: configuration, document loading, chunking, retrieval, user interface, and tests are reasonable boundaries for a small retrieval application. Avoid circular imports where modules depend on each other in both directions.

A `requirements.txt` file records Python packages needed by the project. Pinning exact versions can improve reproducibility, but dependencies should also be updated responsibly for security fixes. Test upgrades before changing a deployed environment.

## 4. Environment variables
Environment variables are a common way to configure deployment-specific values such as API keys and database URLs. A local `.env` file can be loaded by a development utility, but it should be excluded from version control. Commit `.env.example` with placeholder names and safe sample values, not real credentials.

If an API call fails with an authentication error, check that the environment variable is set in the correct shell or `.env` file, that the key is not surrounded by accidental quotes or spaces, and that the account permits the requested model. Never paste a secret into a public issue or repository.

## 5. Logging
Use structured, appropriately leveled logs. `DEBUG` is useful during local troubleshooting; `INFO` records important events; `WARNING` marks unexpected but recoverable conditions; `ERROR` indicates a failed operation. Avoid logging sensitive user content unless there is a clear, reviewed need.

Logs should answer what happened, where it happened, and what identifier can help correlate related events. They should not be a substitute for user-facing validation messages or automated tests.

## 6. Working with PDF documents
PDFs may contain selectable text, scanned images, columns, tables, or page headers. Text extraction can lose reading order and formatting. A robust document pipeline should inspect extracted text and handle empty pages. Scanned PDFs may require OCR, which is a separate step and can introduce recognition errors.

Track the source filename and page number when possible. This provenance makes it easier to inspect a retrieved passage and cite it in a generated answer. Do not claim a document supports a fact if the relevant text was not actually extracted.

## 7. Data quality
Before indexing documents, remove repeated navigation, irrelevant boilerplate, and corrupted text where practical. Preserve headings because they provide context. Do not merge unrelated sections into one chunk merely to reach a target length. Chunk size is a trade-off: very small chunks can lose context; very large chunks can dilute relevance.

## 8. Reproducible setup
Document the Python version, dependencies, configuration, indexing command, query command, and reset instructions. Keep source documents in a known directory and write the vector index to a local data directory excluded from Git if it is generated. If a database schema or embedding model changes, rebuild the index so vectors and metadata stay consistent.

## 9. Safe project delivery
Before pushing code, inspect staged files with `git status`. Add a `.gitignore` for `.env`, virtual environments, Python caches, local vector stores, and editor files. If a secret is accidentally committed, deleting it in a later commit does not make the exposed secret safe; revoke or rotate it.

## 10. Troubleshooting order
When a command fails, read the first meaningful error and the final traceback line. Verify the current working directory, filenames, Python interpreter, virtual environment, dependency installation, and configuration. Change one likely cause at a time and rerun the command. This makes it easier to identify the actual fix.


## 11. Command-line interfaces
A command-line program should provide clear help text, sensible defaults, and meaningful exit codes. Separate argument parsing from the underlying operation so the core logic can be tested without invoking a shell. Avoid requiring a developer to edit source code just to change a directory or model name; use command-line options or environment variables.

## 12. Configuration validation
Validate configuration at startup. If a required API key is missing, report the variable name without printing any secret. If a configured folder does not exist, either create it when that is safe or explain how to fix the path. Failing early is usually better than allowing a long job to run and then fail during the first external request.

## 13. Backups and generated data
Generated indexes can usually be rebuilt from source documents and embedding settings. Keep source files separate from generated artifacts and document the rebuild command. For important user data, define backup and restore procedures. A local development vector store is not a backup strategy for production information.
