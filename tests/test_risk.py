import pytest
from backend.agents.risk_agent import risk_agent

def test_risk_scoring():
    mock_clauses = [
        {"type": "Liability", "content": "Contractor's liability is unlimited.", "risk_level": "High"},
        {"type": "Payment", "content": "Immediate upfront fee is required.", "risk_level": "Medium"}
    ]
    result = risk_agent.analyze_risk(mock_clauses)
    
    assert "risk_score" in result
    assert "triggered_rules" in result
    assert 0 <= result["risk_score"] <= 100
