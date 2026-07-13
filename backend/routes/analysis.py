from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
import json
import io
from pathlib import Path
from ..services.storage_service import storage_service
from ..services.pdf_service import pdf_service
from ..services.rag_service import rag_service
from ..agents.extraction_agent import extraction_agent
from ..agents.risk_agent import risk_agent
from ..agents.summary_agent import summary_agent

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.post("/run/{document_id}")
def run_analysis(document_id: int):
    doc = storage_service.get_document(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    try:
        # 1. Parse PDF text
        file_path = Path(doc["file_path"])
        parsing_result = pdf_service.extract_text(file_path)
        full_text = parsing_result["full_text"]
        
        # 2. Clause Extraction
        extracted_clauses = extraction_agent.extract_clauses(full_text)
        
        # Save clauses in DB and RAG Index
        # Clear existing ones first in case of re-analysis
        rag_service.delete_document_clauses(document_id)
        
        # Save to SQLite & Index in ChromaDB
        for cl in extracted_clauses:
            storage_service.add_clause(
                document_id=document_id,
                clause_type=cl.get("type", "Other"),
                content=cl.get("content", ""),
                risk_level=cl.get("risk_level", "Medium"),
                page_num=cl.get("page_num")
            )
            
        # Index in Chroma DB
        rag_service.add_clauses(document_id, extracted_clauses)
        
        # 3. Risk Scoring & Assessment
        risk_result = risk_agent.analyze_risk(extracted_clauses)
        
        # 4. Generate Executive Summary
        summary_text = summary_agent.generate_text_summary(
            filename=doc["filename"],
            risk_score=risk_result["risk_score"],
            clauses=extracted_clauses,
            risks=risk_result["explanations"]
        )
        
        # Save analysis in SQLite
        storage_service.add_analysis(
            document_id=document_id,
            risk_score=risk_result["risk_score"],
            summary=summary_text,
            risk_explanation=json.dumps(risk_result["explanations"])
        )
        
        return {
            "status": "success",
            "document_id": document_id,
            "risk_score": risk_result["risk_score"],
            "summary": summary_text,
            "clauses": extracted_clauses,
            "risks": risk_result["explanations"]
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

@router.get("/{document_id}")
def get_analysis(document_id: int):
    analysis = storage_service.get_analysis(document_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found for this document. Please run analysis first.")
        
    clauses = storage_service.get_clauses(document_id)
    
    return {
        "analysis": analysis,
        "clauses": clauses
    }

@router.get("/{document_id}/pdf")
def get_pdf_report(document_id: int):
    doc = storage_service.get_document(document_id)
    analysis = storage_service.get_analysis(document_id)
    if not doc or not analysis:
        raise HTTPException(status_code=404, detail="Document or analysis not found")
        
    clauses = storage_service.get_clauses(document_id)
    risks = json.loads(analysis["risk_explanation"] or "[]")
    
    pdf_bytes = summary_agent.generate_pdf_report(
        filename=doc["filename"],
        risk_score=analysis["risk_score"],
        summary_text=analysis["summary"],
        clauses=clauses,
        risks=risks
    )
    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=LegalRAG_Report_{document_id}.pdf"}
    )

@router.get("/{document_id}/csv")
def get_csv_report(document_id: int):
    doc = storage_service.get_document(document_id)
    analysis = storage_service.get_analysis(document_id)
    if not doc or not analysis:
        raise HTTPException(status_code=404, detail="Document or analysis not found")
        
    clauses = storage_service.get_clauses(document_id)
    risks = json.loads(analysis["risk_explanation"] or "[]")
    
    csv_str = summary_agent.generate_csv_summary(clauses, risks)
    
    return Response(
        content=csv_str,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=LegalRAG_Summary_{document_id}.csv"}
    )
