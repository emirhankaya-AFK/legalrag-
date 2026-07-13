import pytest
from backend.agents.extraction_agent import extraction_agent

def test_extraction_structure():
    mock_contract = "This contract dictates that payment must be made upfront immediately. Limitation of liability is absent."
    clauses = extraction_agent.extract_clauses(mock_contract)
    
    assert isinstance(clauses, list)
    if clauses:
        first_clause = clauses[0]
        assert "type" in first_clause
        assert "content" in first_clause
        assert "risk_level" in first_clause
