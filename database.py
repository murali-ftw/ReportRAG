import psycopg
from psycopg.rows import dict_row

from keys import DOCUMENTS_TABLE, POSTGRES_CONFIG


def get_documents_table() -> str:
    if not DOCUMENTS_TABLE.isidentifier():
        raise ValueError("DOCUMENTS_TABLE must be a valid table identifier.")
    return DOCUMENTS_TABLE


def fetch_documents() -> list[dict]:
    query = f"""
        SELECT
            "Uuid"::text AS uuid,
            "CompanyName" AS company_name,
            "ReportType" AS report_type,
            "DownloadURL" AS download_url,
            "Path" AS path,
            "DocumentYear" AS document_year
        FROM {get_documents_table()}
        ORDER BY "CompanyName", "DocumentYear" DESC, "ReportType"
    """

    with psycopg.connect(**POSTGRES_CONFIG, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return list(cur.fetchall())


def find_document_by_company(company_name: str) -> dict | None:
    query = f"""
        SELECT
            "Uuid"::text AS uuid,
            "CompanyName" AS company_name,
            "ReportType" AS report_type,
            "DownloadURL" AS download_url,
            "Path" AS path,
            "DocumentYear" AS document_year
        FROM {get_documents_table()}
        WHERE lower("CompanyName") = lower(%s)
        ORDER BY "DocumentYear" DESC, "ReportType"
        LIMIT 1
    """

    with psycopg.connect(**POSTGRES_CONFIG, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (company_name.strip(),))
            return cur.fetchone()
