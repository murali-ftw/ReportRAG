import json
import uuid

import requests

from keys import LANGFLOW_API_KEY, LANGFLOW_URL


class LangflowAPIError(Exception):
    pass


def build_payload(path: str, question: str, company_name: str) -> dict:
    return {
        "output_type": "chat",
        "input_type": "text",
        "session_id": str(uuid.uuid4()),
        "tweaks": {
            "CustomComponent-x7cmR": {
                "pdf_path": path,
            },
            "TextInput-mQ6Fe": {
                "input_value": question,
            },
            "TextInput-X0bII": {
                "input_value": company_name,
            },
        },
    }


def extract_answer(response_json: dict) -> str:
    try:
        outputs = response_json["outputs"][0]["outputs"][0]
        message = outputs["results"]["message"]
        return message.get("text") or json.dumps(response_json, indent=2)
    except (KeyError, IndexError, TypeError):
        return json.dumps(response_json, indent=2)


def ask_langflow(path: str, question: str, company_name: str) -> tuple[str, dict]:
    payload = build_payload(path, question, company_name)
    headers = {"x-api-key": LANGFLOW_API_KEY}

    response = requests.post(
        LANGFLOW_URL,
        json=payload,
        headers=headers,
        timeout=120,
    )

    if not response.ok:
        try:
            error_body = json.dumps(response.json(), indent=2)
        except ValueError:
            error_body = response.text
        raise LangflowAPIError(
            f"{response.status_code} {response.reason}\n{error_body}"
        )

    response_json = response.json()
    return extract_answer(response_json), response_json
