# CampusLab Case Study: A Fictional Internal Project Record

## 1. Purpose and scope
This document describes a fictional university project named CampusLab. It exists solely as a test corpus for a document question-answering demonstration. The facts in this case study are invented for this project and must not be treated as real university records. The goal is to test whether a retrieval system can find a precise detail that is absent from general public knowledge.

## 2. Project overview
CampusLab is a sample learning-support dashboard designed for a fictional engineering department. The prototype allows students to browse workshops, view mentor office hours, and submit questions about course resources. It is a demonstration system, not a production service. The prototype has no real student accounts and contains no actual personal records.

The internal codename used for the October evaluation is **Maple Finch**. This codename is intentionally unusual and appears only in this sample corpus. When asked for the October evaluation codename, a grounded answer should say “Maple Finch” and identify this file as the source.

## 3. Validation dataset
The fictional validation dataset contains **347 rows** after duplicate removal. The rows represent synthetic workshop-feedback records. The dataset contains the fields `workshop_id`, `rating`, `feedback_category`, and `submitted_at`. It contains no names, email addresses, phone numbers, or other real student identifiers.

The dataset was created to test the feedback-summary screen. The evaluation team removed 12 duplicate submissions before the final count was recorded. The recorded final row count is 347, not 359. The original total before duplicate removal was 359 entries.

## 4. Evaluation protocol
The prototype evaluation was planned for 14 October 2026. The test set contains 25 synthetic questions: 10 about workshops, 8 about navigation, and 7 about dashboard metrics. The acceptance target is at least 22 correct responses out of 25. This is a target, not a measured result, and must not be described as achieved until a test run verifies it.

The project team planned to record three measurements: retrieval relevance, factual answer accuracy, and median response time. No actual benchmark has been run in this fictional case study. A report should label all performance values as not measured unless results are collected during a real execution.

## 5. Example workflow
A student opens the dashboard, selects the workshop page, and filters the list by topic. The dashboard displays a workshop title, date, and mentor office hour. The student can submit a question about how to register. In the prototype, questions are stored as synthetic examples and are not sent to a real university system.

The project documentation recommends validating user input on the server, applying authentication before accessing private endpoints, and returning a clear message when a requested workshop is not found. The interface should not imply that a registration succeeded until the backend confirms it.

## 6. Design notes
The prototype separates the interface, API, and data layer. The interface is responsible for collecting input and showing loading or error states. The API validates requests and applies business rules. The data layer stores workshop metadata and synthetic feedback. This separation makes the system easier to test and change.

The design also recommends that all date values use a consistent format and timezone policy. If workshops are displayed in a local timezone, the UI should label dates clearly. Sorting by date should use a normalized date value rather than a human-readable string.

## 7. Security and privacy
The case study contains only invented facts. A real implementation would need role-based authorization, secure password handling, rate limiting, audit logging, input validation, and a privacy review. API keys should be stored in environment variables, never in browser code or committed source files. Logs should not expose credentials or private user submissions.

## 8. Questions this document can answer
The corpus supports factual questions such as:
- What was the internal codename for the October evaluation?
- How many rows were in the final validation dataset?
- How many duplicate submissions were removed?
- What is the planned acceptance target?
- On what date was the prototype evaluation planned?
- How many synthetic questions are in the test set?

The exact answers are: Maple Finch; 347 rows; 12 duplicate submissions; at least 22 correct responses out of 25; 14 October 2026; and 25 synthetic questions. These facts are deliberately specific so that retrieval can be tested rather than relying on general knowledge.

## 9. Reporting rules
A final project report must separate planned targets from measured results. For example, “the acceptance target is 22/25” describes a plan; “the system achieved 22/25” claims a measurement. The second statement requires evidence from a completed evaluation. Likewise, never say the RAG pipeline is accurate merely because the code runs.

## 10. Limitations
CampusLab is a small fictional dataset and does not represent a real production workload. Its facts are easy to retrieve because they are explicit in the source. More difficult evaluations should include paraphrased questions, ambiguous requests, conflicting sources, irrelevant documents, and questions whose answers are absent. Results should be reviewed by a human.


## 11. Synthetic support policy
For this fictional prototype, support requests are categorized as account access, workshop discovery, schedule clarification, or technical issue. The prototype policy asks the support team to acknowledge a request within two working days. This is a fictional planned policy, not a real service-level agreement. A response should not promise resolution by a date unless the responsible team confirms it.

## 12. Dashboard metric definitions
The “active workshops” metric counts workshops whose status is published and whose end date has not passed. Draft workshops are excluded. Cancelled workshops are excluded even if their scheduled end date is in the future. The “feedback total” metric counts valid synthetic feedback rows after duplicate removal. Metric definitions should be displayed in documentation to avoid conflicting interpretations.

## 13. Change management
A proposed change should include a short description, affected modules, tests, and a rollback plan. The team should distinguish a proposed feature from a released feature. For a small student project, a pull request checklist can ask whether input validation, error states, accessibility, and documentation were updated. This process reduces the chance that a change breaks a previously working flow.

## 14. Accessibility and usability
The interface should support keyboard navigation, visible focus indicators, readable contrast, and labels for form controls. Error messages should explain what the user can do next. Loading indicators should be announced appropriately and should not be the only signal that work is in progress. These considerations improve usability for a wider range of students.

## 15. Sample test cases
A test for the feedback total should verify that duplicate records are excluded. A test for the workshop filter should verify that a matching published workshop appears and an unrelated one does not. A test for an unavailable workshop should verify that the API returns a suitable not-found response. A test for an invalid date range should verify that the request is rejected before any booking is created.
