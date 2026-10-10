# Manual Test Plan

Run `python ingest.py` before testing.

| Test | Question | Expected evidence to inspect |
|---|---|---|
| Private fact | What was the internal codename for the October evaluation? | `05_campuslab_case_study.md`, passage containing “Maple Finch” |
| Exact count | How many rows were in the final validation dataset? | `05_campuslab_case_study.md`, passage containing 347 rows |
| Duplicate count | How many duplicate submissions were removed? | `05_campuslab_case_study.md`, passage containing 12 duplicates |
| Technical explanation | Why use overlap in chunking? | `04_testing_and_retrieval.md`, chunking section |
| Missing answer | What is the CampusLab director's personal phone number? | No supporting source passage should be present; the app should say it could not find the information |

For each test, record the retrieved source, chunk, and whether the text actually supports the answer. Similarity distance alone is not proof of relevance.
