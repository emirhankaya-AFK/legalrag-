import os
import json
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from ..config.settings import settings

class LLMService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.has_api_key = bool(self.api_key and self.api_key != "YOUR_GEMINI_API_KEY")
        if self.has_api_key:
            genai.configure(api_key=self.api_key)
        else:
            print("WARNING: GEMINI_API_KEY is not configured. Running in Mock Mode.")

    def generate_content(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """
        Generates content using gemini-2.0-flash.
        """
        if not self.has_api_key:
            return self._mock_llm_response(prompt)
            
        try:
            model = genai.GenerativeModel(
                model_name=settings.LLM_MODEL,
                system_instruction=system_instruction
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini LLM Call failed: {e}. Falling back to Mock.")
            return self._mock_llm_response(prompt)

    def generate_embeddings(self, text: str) -> List[float]:
        """
        Generates embeddings using text-embedding-004.
        """
        if not self.has_api_key:
            return self._mock_embeddings(text)
            
        try:
            result = genai.embed_content(
                model=f"models/{settings.EMBEDDING_MODEL}",
                content=text,
                task_type="retrieval_document"
            )
            return result["embedding"]
        except Exception as e:
            print(f"Gemini Embedding Call failed: {e}. Falling back to Mock.")
            return self._mock_embeddings(text)

    def _mock_embeddings(self, text: str) -> List[float]:
        # Return a deterministic mock vector of length 768
        import random
        # Seed based on hash of text for reproducibility
        random.seed(hash(text))
        return [random.uniform(-0.1, 0.1) for _ in range(768)]

    def _mock_llm_response(self, prompt: str) -> str:
        # Check the nature of the prompt to return appropriate mock data
        if "Extract clauses" in prompt or "extract key clauses" in prompt.lower():
            return json.dumps([
                {
                    "type": "Liability",
                    "content": "The Contractor's total liability under this agreement shall be unlimited in the event of gross negligence or breach of confidentiality.",
                    "risk_level": "High"
                },
                {
                    "type": "Payment",
                    "content": "Customer shall pay an upfront initiation fee of $10,000 immediately upon signing, and subsequent invoices net 7 days.",
                    "risk_level": "Medium"
                },
                {
                    "type": "Termination",
                    "content": "Either party may terminate this agreement without cause upon giving 10 days written notice to the other party.",
                    "risk_level": "High"
                },
                {
                    "type": "Indemnification",
                    "content": "Customer agrees to defend, indemnify, and hold harmless Contractor from any third-party claims arising out of this agreement.",
                    "risk_level": "High"
                }
            ])
        elif "risk_analysis" in prompt or "risky clauses" in prompt.lower():
            return json.dumps([
                {
                    "clause_type": "Liability",
                    "risk_explanation": "Unlimited liability for breach of confidentiality exposes the company to extreme financial damages.",
                    "severity": "High"
                },
                {
                    "clause_type": "Payment",
                    "risk_explanation": "Net 7 days payment terms are unusually short and could result in late fees or service interruption.",
                    "severity": "Medium"
                },
                {
                    "clause_type": "Termination",
                    "risk_explanation": "A 10-day termination notice is too short, potentially leaving operations vulnerable.",
                    "severity": "High"
                },
                {
                    "clause_type": "Indemnification",
                    "risk_explanation": "Broad indemnification of the contractor for all claims shifts disproportionate risk to the customer.",
                    "severity": "High"
                }
            ])
        elif "Based on this contract section, answer" in prompt or "answer the user's question" in prompt.lower():
            return "Based on Section 4 (Termination), the customer can terminate this agreement by providing at least 10 days written notice to the provider."
        else:
            return "Mock Response: Standard terms and conditions apply. Please configure your GEMINI_API_KEY for live responses."

llm_service = LLMService()
