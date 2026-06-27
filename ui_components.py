import streamlit as st


def render_query_inputs() -> tuple[str, str, bool]:
    company_name = st.text_input(
        "Company name",
        placeholder="Microsoft",
        help="This is matched against the CompanyName column in Postgres.",
    )
    user_question = st.text_area(
        "Question",
        placeholder="What were the main revenue drivers in this report?",
        height=120,
    )
    submitted = st.form_submit_button("Ask")
    return company_name, user_question, submitted
