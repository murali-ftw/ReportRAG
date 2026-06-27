import psycopg
import requests
import streamlit as st

from database import find_document_by_company
from langflow_client import LangflowAPIError, ask_langflow
from langflow_client import build_payload
from ui_components import render_query_inputs


st.set_page_config(page_title="Report RAG", layout="centered")

st.title("Report RAG")

with st.form("query_form"):
    company_name, user_question, submitted = render_query_inputs()

if submitted:
    if not company_name.strip() or not user_question.strip():
        st.error("Enter company name and question.")
    else:
        with st.spinner("Finding company document..."):
            try:
                document = find_document_by_company(company_name)
            except (psycopg.Error, ValueError) as exc:
                st.error(f"Error searching Postgres documents table: {exc}")
                document = None

        if document is None:
            st.error(
                "Company not found in Postgres. "
                "Check the CompanyName value in the documents table."
            )
        else:
            file_path = document["path"]
            schema_company_name = document["company_name"]
            payload_preview = build_payload(
                file_path.strip(),
                user_question.strip(),
                schema_company_name.strip(),
            )

            with st.expander("Langflow request payload"):
                st.json(payload_preview)

            with st.spinner("Querying Langflow..."):
                try:
                    answer, raw_response = ask_langflow(
                        file_path.strip(),
                        user_question.strip(),
                        schema_company_name.strip(),
                    )
                except LangflowAPIError as exc:
                    st.error("Langflow returned an error.")
                    st.code(str(exc))
                except requests.exceptions.RequestException as exc:
                    st.error(f"Error making API request: {exc}")
                except ValueError as exc:
                    st.error(f"Error parsing response: {exc}")
                else:
                    st.caption(
                        f'Using {schema_company_name} '
                        f'({document["document_year"]}) from {file_path}'
                    )
                    st.subheader("Answer")
                    st.write(answer)

                    with st.expander("Raw Langflow response"):
                        st.json(raw_response)
