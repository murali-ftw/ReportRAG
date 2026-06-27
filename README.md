# ReportRAG

ReportRAG is a Streamlit frontend for asking questions over company reports through a Langflow RAG pipeline. The app uses Postgres as the source of truth for report metadata, looks up the correct PDF path from the company name entered by the user, and sends the resolved inputs to a Langflow API endpoint.

## Current Flow

1. The user opens the Streamlit app.
2. The user enters:
   - Company name
   - Question
3. The app searches Postgres for a matching `"CompanyName"` in the configured reports table.
4. The app selects the newest matching document by `"DocumentYear"`.
5. The app sends these inputs to Langflow:
   - `pdf_path`: the `"Path"` value from Postgres
   - question: the user's question
   - company name: the exact `"CompanyName"` value stored in Postgres
6. Langflow returns the final answer, which is displayed in Streamlit.

The request payload is also shown in the Streamlit app under the `Langflow request payload` expander for debugging.

## Project Structure

```text
ReportRAG/
├── app.py
├── database.py
├── document_service.py
├── langflow_client.py
├── ui_components.py
├── keys.py
├── chroma.py
├── requirements.txt
├── sql/
│   └── create_documents.sql
└── reports/
    ├── Aramco.pdf
    ├── JPMorgan.pdf
    ├── Microsoft.pdf
    └── Walmart.pdf
```

## File Responsibilities

`app.py`

Main Streamlit application. It renders the form, validates inputs, looks up the company document in Postgres, sends the resolved inputs to Langflow, and displays the answer.

`database.py`

Handles Postgres access. It contains the table-name validation, document fetch query, and company lookup query.

`langflow_client.py`

Builds the Langflow payload, sends the HTTP request, parses the Langflow response, and raises readable errors when Langflow returns a non-200 response.

`ui_components.py`

Contains Streamlit UI helpers for collecting the company name and user question.

`document_service.py`

Contains helper functions for filtering and labeling document records. It is currently useful for document-list workflows.

`keys.py`

Stores local configuration and credentials. This file is intentionally ignored by Git in `.gitignore`.

`sql/create_documents.sql`

Creates the Postgres table and inserts initial report metadata records.

`chroma.py`

Utility script for inspecting a local ChromaDB collection and printing its contents as a pandas DataFrame.

## Requirements

- Python 3.10+
- Postgres
- Langflow running locally
- The PDF reports available at the paths stored in Postgres

Python packages are listed in `requirements.txt`:

```text
streamlit
requests
psycopg[binary]
```

If you plan to run `chroma.py`, install these additional packages:

```bash
venv/bin/python -m pip install chromadb pandas
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
venv/bin/python -m pip install -r requirements.txt
```

## Configuration

Update `keys.py` with your local settings:

```python
LANGFLOW_API_KEY = "YOUR_LANGFLOW_API_KEY"
LANGFLOW_URL = "http://localhost:7860/api/v1/run/YOUR_FLOW_ID"

POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "reportrag",
    "user": "postgres",
    "password": "YOUR_POSTGRES_PASSWORD",
}

DOCUMENTS_TABLE = "reports"
```

Do not commit real credentials. `keys.py` is ignored by Git.

## Database Schema

The app expects a Postgres table with these columns:

| Column | Type | Description |
| --- | --- | --- |
| `"Uuid"` | UUID | Primary key for the report metadata record |
| `"CompanyName"` | TEXT | Company name used for lookup and passed to Langflow |
| `"ReportType"` | TEXT | Type of report, such as annual report |
| `"DownloadURL"` | TEXT | Optional source URL for the report |
| `"Path"` | TEXT | Local PDF path passed to Langflow as `pdf_path` |
| `"DocumentYear"` | INTEGER | Report year used to choose the newest matching report |

Create and seed the table:

```bash
createdb -U postgres reportrag
psql -U postgres -d reportrag -f sql/create_documents.sql
```

If your Postgres user or database name is different, adjust the command and `POSTGRES_CONFIG` in `keys.py`.

## Langflow Payload

The app sends this payload shape:

```json
{
  "output_type": "chat",
  "input_type": "text",
  "session_id": "generated-uuid",
  "tweaks": {
    "CustomComponent-x7cmR": {
      "pdf_path": "/absolute/path/to/report.pdf"
    },
    "TextInput-mQ6Fe": {
      "input_value": "User question"
    },
    "TextInput-X0bII": {
      "input_value": "CompanyName from Postgres"
    }
  }
}
```

The parameter order inside the Python client is:

```python
ask_langflow(path, question, company_name)
```

## Run The App

Start Langflow first, then run Streamlit:

```bash
venv/bin/python -m streamlit run app.py
```

Open the local URL printed by Streamlit, usually:

```text
http://localhost:8501
```

## Example Usage

Company name:

```text
Microsoft
```

Question:

```text
What were the main revenue drivers in this report?
```

The app will search Postgres for `Microsoft`, retrieve the latest matching report path, and send the PDF path, question, and exact stored company name to Langflow.

## Troubleshooting

### Company Not Found

Check that the company exists in Postgres:

```sql
SELECT "CompanyName", "Path", "DocumentYear"
FROM reports
ORDER BY "CompanyName";
```

The lookup is case-insensitive, but the company must otherwise match the stored name.

### Langflow 500 Error

The app displays the response body from Langflow when the API returns an error. Common causes:

- The PDF path in Postgres does not exist.
- Langflow is not running.
- The flow ID in `LANGFLOW_URL` is incorrect.
- The custom component expects a different input field name.
- The PDF splitter component cannot read or parse the file.

Confirm the payload shown in the `Langflow request payload` expander. The PDF path should be an absolute path that exists on the same machine where Langflow is running.

### Postgres Connection Error

Check `POSTGRES_CONFIG` in `keys.py` and confirm that Postgres is running:

```bash
psql -U postgres -d reportrag
```

### Missing Python Package

Install dependencies again:

```bash
venv/bin/python -m pip install -r requirements.txt
```

## Notes

- The table name is configured using `DOCUMENTS_TABLE` in `keys.py`.
- The current SQL file creates a table named `reports`.
- When multiple documents match a company, the app uses the newest `"DocumentYear"`.
- The PDF path sent to Langflow comes only from Postgres, not from direct user input.

