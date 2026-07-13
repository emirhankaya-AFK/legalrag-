import yaml
from pathlib import Path
from typing import Dict, Any
from ..services.llm_service import llm_service
from ..services.rag_service import rag_service

class QAAgent:
    def __init__(self):
        self.prompt_path = Path(__file__).resolve().parent.parent / "config" / "prompts.yaml"
        self._load_prompts()

    def _load_prompts(self):
        try:
            with open(self.prompt_path, "r") as f:
                self.prompts = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading prompts.yaml: {e}")
            self.prompts = {}

    def answer_question(self, document_id: int, question: str) -> Dict[str, Any]:
        """
        Retrieves relevant clauses from ChromaDB and answers the question with citations.
        """
        # Retrieve top 4 relevant clauses from ChromaDB for this document
        matches = rag_service.query_clauses(query_text=question, document_id=document_id, n_results=4)
        
        # Build context
        context_parts = []
        citations = []
        for idx, match in enumerate(matches):
            metadata = match.get("metadata", {})
            clause_type = metadata.get("clause_type", "General")
            page_num = metadata.get("page_num", "Unknown")
            content = match.get("content", "")
            
            context_parts.append(f"Source {idx+1} [Type: {clause_type}, Page: {page_num}]:\n{content}")
            citations.append({
                "source_index": idx + 1,
                "clause_type": clause_type,
                "page_num": page_num,
                "snippet": content[:150] + "..." if len(content) > 150 else content
            })

        context_str = "\n\n".join(context_parts)
        system_prompt = self.prompts.get("qa", "")
        
        # Format user prompt
        prompt = system_prompt.format(context=context_str, question=question)
        
        # Call LLM
        answer = llm_service.generate_content(prompt)
        
        return {
            "answer": answer,
            "citations": citations,
            "context_used": matches
        }

qa_agent = QAAgent()
