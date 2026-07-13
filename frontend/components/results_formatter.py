import streamlit as st
from typing import Dict, Any, List

def format_risk_level(level: str) -> str:
    level = level.lower().strip()
    if level == "high":
        return '<span style="background-color: #FEE2E2; color: #991B1B; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85rem;">🔴 HIGH RISK</span>'
    elif level == "medium":
        return '<span style="background-color: #FEF3C7; color: #92400E; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85rem;">🟡 MEDIUM RISK</span>'
    else:
        return '<span style="background-color: #D1FAE5; color: #065F46; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.85rem;">🟢 LOW RISK</span>'

def render_clause_card(clause_type: str, risk_level: str, content: str, page: int = None):
    page_str = f" | Page {page}" if page else ""
    st.markdown(f"""
    <div style="background-color: white; border: 1px solid #E2E8F0; padding: 1.2rem; border-radius: 8px; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
            <strong style="color: #1E3A8A; font-size: 1.1rem;">📌 {clause_type} Clause{page_str}</strong>
            {format_risk_level(risk_level)}
        </div>
        <p style="color: #334155; font-size: 0.95rem; white-space: pre-wrap; line-height: 1.5; font-style: italic; background-color: #F8FAFC; padding: 0.8rem; border-radius: 6px; border-left: 3px solid #3B82F6;">
            "{content}"
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_risk_explanation(clause_type: str, explanation: str, severity: str):
    st.markdown(f"""
    <div style="background-color: #FFFBEB; border: 1px solid #FCD34D; padding: 1rem; border-radius: 8px; margin-bottom: 0.8rem; border-left: 5px solid #F59E0B;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <strong style="color: #78350F;">⚠️ Risk in {clause_type} Clause</strong>
            {format_risk_level(severity)}
        </div>
        <span style="color: #451A03; font-size: 0.95rem;">{explanation}</span>
    </div>
    """, unsafe_allow_html=True)
