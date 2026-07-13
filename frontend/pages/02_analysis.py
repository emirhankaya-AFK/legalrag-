import streamlit as st
import requests
import json
from ..components.results_formatter import render_clause_card, render_risk_explanation

BACKEND_URL = "http://localhost:8001"

st.set_page_config(page_title="Risk Analysis - LegalRAG", layout="wide")

st.title("⚖️ Contract Analysis & Audit")

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
    # 1. Single Document Analysis Mode
    doc_options = {doc["filename"]: doc["id"] for doc in documents}
    selected_doc_name = st.selectbox("Select Contract to Analyze", list(doc_options.keys()))
    selected_doc_id = doc_options[selected_doc_name]

    if st.button("🚀 Run AI Audit"):
        with st.spinner("Analyzing contract text and calculating risk matrix..."):
            try:
                res = requests.post(f"{BACKEND_URL}/analysis/run/{selected_doc_id}")
                if res.status_code == 200:
                    st.success("Analysis complete!")
                else:
                    st.error(f"Analysis failed: {res.json().get('detail')}")
            except Exception as e:
                st.error(f"Error running analysis: {e}")

    # Fetch existing analysis if it exists
    analysis_data = None
    try:
        ans_res = requests.get(f"{BACKEND_URL}/analysis/{selected_doc_id}")
        if ans_res.status_code == 200:
            analysis_data = ans_res.json()
    except Exception:
        pass

    if analysis_data:
        analysis = analysis_data["analysis"]
        clauses = analysis_data["clauses"]
        risks = json.loads(analysis["risk_explanation"] or "[]")
        score = analysis["risk_score"]

        # Risk Score Metric
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"""
            <div style="background-color: white; border: 2px solid #E2E8F0; padding: 1.5rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <span style="font-size: 0.9rem; font-weight: bold; color: #64748B; text-transform: uppercase;">Overall Risk Score</span>
                <h1 style="color: {'#DC2626' if score >= 60 else '#D97706' if score >= 30 else '#059669'}; font-size: 3.5rem; margin: 0.5rem 0;">{score}</h1>
                <div style="background-color: #F1F5F9; border-radius: 9999px; height: 10px; width: 100%; overflow: hidden;">
                    <div style="background-color: {'#DC2626' if score >= 60 else '#D97706' if score >= 30 else '#059669'}; height: 100%; width: {score}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Save Analysis as Template Feature
            st.write("")
            template_name = st.text_input("Template Name", value=f"{selected_doc_name}_template")
            if st.button("💾 Save as Template"):
                # Simulating template saving in session state
                if "templates" not in st.session_state:
                    st.session_state["templates"] = {}
                st.session_state["templates"][template_name] = {
                    "doc_id": selected_doc_id,
                    "risk_score": score,
                    "clauses": clauses
                }
                st.success(f"Saved template: '{template_name}'")
        
        with col2:
            st.subheader("📝 Executive Summary")
            st.write(analysis["summary"])

        # Display tabs for Clauses and Risks
        tab1, tab2, tab3 = st.tabs(["📌 Extracted Key Clauses", "⚠️ Identified Risks & Explanations", "📁 Saved Templates"])
        
        with tab1:
            if not clauses:
                st.write("No clauses extracted.")
            else:
                for cl in clauses:
                    render_clause_card(
                        clause_type=cl["clause_type"],
                        risk_level=cl["risk_level"],
                        content=cl["content"],
                        page=cl.get("page_num")
                    )
                    
        with tab2:
            if not risks:
                st.info("No substantial risks detected matching config profiles.")
            else:
                for r in risks:
                    render_risk_explanation(
                        clause_type=r.get("clause_type", "General"),
                        explanation=r.get("risk_explanation", ""),
                        severity=r.get("severity", "Medium")
                    )

        with tab3:
            templates = st.session_state.get("templates", {})
            if not templates:
                st.info("No templates saved yet.")
            else:
                for name, data in templates.items():
                    st.markdown(f"**Template**: `{name}` (Base Contract ID: `{data['doc_id']}` | Risk Score: `{data['risk_score']}`)")

    else:
        st.info("Please run the AI Audit to populate the clauses and risk scorecard.")

    # 2. Side-by-Side Comparison Feature
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.subheader("🔄 Compare Two Contracts")
    
    if len(documents) >= 2:
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            compare_doc1 = st.selectbox("Select First Contract", list(doc_options.keys()), key="comp1")
        with col_c2:
            compare_doc2 = st.selectbox("Select Second Contract", list(doc_options.keys()), key="comp2")
            
        if st.button("⚔️ Compare Contracts"):
            id1, id2 = doc_options[compare_doc1], doc_options[compare_doc2]
            try:
                # Retrieve analyses
                ans1_res = requests.get(f"{BACKEND_URL}/analysis/{id1}")
                ans2_res = requests.get(f"{BACKEND_URL}/analysis/{id2}")
                
                if ans1_res.status_code == 200 and ans2_res.status_code == 200:
                    c1_data, c2_data = ans1_res.json(), ans2_res.json()
                    
                    st.write("### Side-by-Side Comparison")
                    col_res1, col_res2 = st.columns(2)
                    
                    with col_res1:
                        st.markdown(f"#### {compare_doc1}")
                        st.metric("Risk Score", f"{c1_data['analysis']['risk_score']}/100")
                        st.write("**Key Clauses Summary:**")
                        for cl in c1_data["clauses"][:3]:
                            st.write(f"- **{cl['clause_type']}** ({cl['risk_level']}): {cl['content'][:120]}...")
                            
                    with col_res2:
                        st.markdown(f"#### {compare_doc2}")
                        st.metric("Risk Score", f"{c2_data['analysis']['risk_score']}/100")
                        st.write("**Key Clauses Summary:**")
                        for cl in c2_data["clauses"][:3]:
                            st.write(f"- **{cl['clause_type']}** ({cl['risk_level']}): {cl['content'][:120]}...")
                else:
                    st.error("Please run AI Audit on both contracts first before comparing them.")
            except Exception as e:
                st.error(f"Failed to compare: {e}")
    else:
        st.info("Upload at least two contracts to enable side-by-side comparisons.")
