import streamlit as st

def render_pdf_metadata(filename: str, size_bytes: int, upload_date: str):
    size_mb = size_bytes / (1024 * 1024)
    st.markdown(f"""
    <div style="background-color: #EFF6FF; border: 1px solid #BFDBFE; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 15px;">
        <span style="font-size: 2rem;">📄</span>
        <div>
            <div style="font-weight: bold; color: #1E3A8A; font-size: 1.05rem;">{filename}</div>
            <div style="color: #60A5FA; font-size: 0.85rem;">
                Size: {size_mb:.2f} MB | Uploaded: {upload_date}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
