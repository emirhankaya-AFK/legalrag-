import streamlit as st
import requests

BACKEND_URL = "http://localhost:8001"

st.set_page_config(page_title="Export Reports - LegalRAG", layout="wide")

st.title("📊 Export Reports")
st.write("Download comprehensive PDF audits, raw JSON extractions, or CSV summaries of your contract audits.")

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
    selected_doc_name = st.selectbox("Select Analyzed Contract to Export", list(doc_options.keys()))
    selected_doc_id = doc_options[selected_doc_name]
    
    # Check if analysis exists
    analysis_exists = False
    try:
        ans_res = requests.get(f"{BACKEND_URL}/analysis/{selected_doc_id}")
        if ans_res.status_code == 200:
            analysis_exists = True
    except Exception:
        pass
        
    if not analysis_exists:
        st.warning("No analysis data found for this document. Run analysis first on the Analysis page.")
    else:
        st.success(f"Analysis reports ready for {selected_doc_name}!")
        
        st.write("### Choose Export Format")
        
        # Download links
        pdf_url = f"{BACKEND_URL}/analysis/{selected_doc_id}/pdf"
        csv_url = f"{BACKEND_URL}/analysis/{selected_doc_id}/csv"
        json_url = f"{BACKEND_URL}/analysis/{selected_doc_id}"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background-color: white; border: 1px solid #E2E8F0; padding: 1.5rem; border-radius: 8px; text-align: center;">
                <span style="font-size: 2.5rem;">📕</span>
                <h4>PDF Report</h4>
                <p style="color: #64748B; font-size: 0.85rem;">Includes risk scores, clause tables, explanations, and mitigation tips.</p>
                <a href="{pdf_url}" target="_blank">
                    <button style="background-color: #EF4444; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; font-weight: bold; cursor: pointer; width: 100%;">
                        Download PDF
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div style="background-color: white; border: 1px solid #E2E8F0; padding: 1.5rem; border-radius: 8px; text-align: center;">
                <span style="font-size: 2.5rem;">📗</span>
                <h4>CSV Summary</h4>
                <p style="color: #64748B; font-size: 0.85rem;">Tabular list of clauses, categories, risk ratings, and brief descriptions.</p>
                <a href="{csv_url}" target="_blank">
                    <button style="background-color: #10B981; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; font-weight: bold; cursor: pointer; width: 100%;">
                        Download CSV
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div style="background-color: white; border: 1px solid #E2E8F0; padding: 1.5rem; border-radius: 8px; text-align: center;">
                <span style="font-size: 2.5rem;">📘</span>
                <h4>JSON Data</h4>
                <p style="color: #64748B; font-size: 0.85rem;">Raw JSON structure of all extracted clauses and parsed parameters.</p>
                <a href="{json_url}" target="_blank">
                    <button style="background-color: #3B82F6; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; font-weight: bold; cursor: pointer; width: 100%;">
                        Download JSON
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
