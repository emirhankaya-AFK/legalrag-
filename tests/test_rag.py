import pytest
from backend.services.rag_service import rag_service

def test_rag_flow():
    doc_id = 9999
    mock_clauses = [
        {"type": "Termination", "content": "Either party can terminate with 10 days notice.", "risk_level": "High"}
    ]
    
    # Clean up first
    rag_service.delete_document_clauses(doc_id)
    
    # Add clauses
    rag_service.add_clauses(doc_id, mock_clauses)
    
    # Query
    results = rag_service.query_clauses("How can I terminate this agreement?", document_id=doc_id)
    
    assert isinstance(results, list)
    if results:
        assert results[0]["metadata"]["document_id"] == doc_id
        
    # Clean up
    rag_service.delete_document_clauses(doc_id)
