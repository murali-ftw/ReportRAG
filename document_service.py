from collections.abc import Iterable


def get_company_names(documents: Iterable[dict]) -> list[str]:
    return sorted({document["company_name"] for document in documents})


def get_documents_for_company(documents: Iterable[dict], company_name: str) -> list[dict]:
    return [
        document
        for document in documents
        if document["company_name"] == company_name
    ]


def get_document_label(document: dict) -> str:
    return (
        f'{document["report_type"]} '
        f'({document["document_year"]}) - {document["path"]}'
    )

