import streamlit as st
import requests

BACKEND_URL = "http://localhost:8001"

st.set_page_config(page_title="Contract Q&A - LegalRAG", layout="wide")

st.title("💬 Contract Q&A")
st.write("Ask natural language questions about your contract, and get answers backed by cited clauses.")

# Fetch documents
try:
    doc_response = requests.get(f"{BACKEND_URL}/documents")
    documents = doc_response.json() if doc_response.status_code == 200 else []
except Exception as e:
    documents = []
    st.error(f"Error connecting to backend: {e}")

if not documents:
    st.info("Please upload contracts first in the Upload page.")
else:
    doc_options = {doc["filename"]: doc["id"] for doc in documents}
    selected_doc_name = st.selectbox("Select Contract to Ask About", list(doc_options.keys()))
    selected_doc_id = doc_options[selected_doc_name]
    
    question = st.text_input("Enter your question:", placeholder="e.g., What are my payment obligations? Is there a liability limit?")
    
    if st.button("💬 Ask AI"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching contract vector embeddings and generating answer..."):
                try:
                    payload = {"document_id": selected_doc_id, "question": question}
                    res = requests.post(f"{BACKEND_URL}/qa", json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        answer = data["answer"]
                        citations = data["citations"]
                        
                        st.write("### AI Answer")
                        st.info(answer)
                        
                        st.write("### Cited Sources")
                        if not citations:
                            st.write("No direct source sections cited.")
                        else:
                            for cit in citations:
                                st.markdown(f"""
                                <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 0.8rem; border-radius: 6px; margin-bottom: 0.8rem;">
                                    <div style="font-weight: bold; color: #1E3A8A; margin-bottom: 0.3rem;">
                                        Source #{cit['source_index']} | Type: {cit['clause_type']} | Page: {cit['page_num']}
                                    </div>
                                    <div style="font-style: italic; color: #475569; font-size: 0.9rem;">
                                        "{cit['snippet']}"
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.error(f"Q&A failed: {res.json().get('detail')}")
                except Exception as e:
                    st.error(f"Error querying Q&A backend: {e}")
