import streamlit as st

st.set_page_config(
    page_title="LegalRAG - AI Contract Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Sleek Aesthetics
st.markdown("""
<style>
    :root {
        --primary-color: #1E3A8A;
        --secondary-color: #3B82F6;
        --background-color: #F8FAFC;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.2rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        border: 1px solid #E2E8F0;
        text-align: center;
    }
    .feature-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚖️ LegalRAG</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Advanced Agentic AI Contract Audit & Risk Analysis Platform</div>', unsafe_allow_html=True)

st.write(
    "Welcome to **LegalRAG**, your AI-powered copilot for legal document review. "
    "LegalRAG analyzes agreements, extracts key clauses, scores risk matrices, "
    "and offers context-aware Q&A citations."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>🔍 Clause Extraction</h3>
        <p>Extracts liability, payment, confidentiality, indemnification, and custom clauses automatically.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>⚠️ Risk Analyzer</h3>
        <p>Identifies unfavorable terms, calculates overall risk scores, and recommends mitigation actions.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>💬 Semantic Q&A</h3>
        <p>Ask natural language questions about your contracts and get instant citations linked to exact sections.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr><br>", unsafe_allow_html=True)

st.markdown('<div class="feature-header">Getting Started</div>', unsafe_allow_html=True)
st.markdown("""
1. Navigate to **01_upload** in the sidebar to upload your contracts.
2. Go to **02_analysis** to execute the audit and evaluate the risk score.
3. Open **03_qa** to converse with the documents and verify terms.
4. Export the findings from **04_reports**.
""")
st.sidebar.info("Select a page above to begin.")
st.sidebar.markdown("---")
st.sidebar.caption("Powered by Gemini 2.0 & ChromaDB")
