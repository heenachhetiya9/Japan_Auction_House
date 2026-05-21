import streamlit as st
from agents.sql_agent import get_sql_agent

st.set_page_config(page_title="Japan Auction House AI")

st.title("Japan Auction House - Agentic AI")

st.write("Ask anything about auction sales data")

user_question = st.text_input("Enter your question")

if st.button("Generate Insight"):

    if user_question:

        with st.spinner("Thinking..."):

            try:
                agent = get_sql_agent()

                response = agent.run(user_question)

                st.success("Response Generated")

                st.write(response)

            except Exception as e:
                st.error(f"Error: {str(e)}")