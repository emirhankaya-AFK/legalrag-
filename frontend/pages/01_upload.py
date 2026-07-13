import streamlit as st
import requests
from ..components.pdf_viewer import render_pdf_metadata

BACKEND_URL = "http://localhost:8001"

st.set_page_config(page_title="Upload Contracts - LegalRAG", layout="wide")

st.title("📂 Upload Contract Documents")
st.write("Upload one or more contract agreements (PDF, max 20MB each) to analyze.")

# File Uploader (Supports Batch Upload)
uploaded_files = st.file_uploader(
    "Choose PDF files", 
    type=["pdf"], 
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("🚀 Upload Documents"):
        success_count = 0
        for uploaded_file in uploaded_files:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            try:
                response = requests.post(f"{BACKEND_URL}/documents/upload", files=files)
                if response.status_code == 200:
                    success_count += 1
                else:
                    st.error(f"Failed to upload {uploaded_file.name}: {response.json().get('detail')}")
            except Exception as e:
                st.error(f"Error uploading {uploaded_file.name}: {e}")
        
        if success_count > 0:
            st.success(f"Successfully uploaded {success_count} contract(s)!")
            st.rerun()

st.markdown("<br><hr><br>", unsafe_allow_html=True)
st.subheader("📚 Managed Contracts")

try:
    response = requests.get(f"{BACKEND_URL}/documents")
    if response.status_code == 200:
        documents = response.json()
        if not documents:
            st.info("No documents uploaded yet.")
        else:
            for doc in documents:
                col1, col2 = st.columns([4, 1])
                with col1:
                    render_pdf_metadata(
                        filename=doc["filename"],
                        size_bytes=doc["file_size"],
                        upload_date=doc["upload_date"]
                    )
                with col2:
                    st.write("")
                    st.write("")
                    if st.button("🗑️ Delete", key=f"del_{doc['id']}"):
                        del_response = requests.delete(f"{BACKEND_URL}/documents/{doc['id']}")
                        if del_response.status_code == 200:
                            st.success(f"Deleted {doc['filename']}")
                            st.rerun()
                        else:
                            st.error("Failed to delete document.")
    else:
        st.error("Could not fetch documents from backend. Check if FastAPI is running.")
except Exception as e:
    st.error(f"Connection error to backend: {e}")
