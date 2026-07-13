import yaml
import json
import re
from pathlib import Path
from typing import List, Dict, Any
from ..services.llm_service import llm_service

class ExtractionAgent:
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

    def extract_clauses(self, text: str) -> List[Dict[str, Any]]:
        """
        Uses the Gemini LLM to extract key clauses from contract text.
        """
        system_prompt = self.prompts.get("extraction", "")
        # Limit text size to prevent token limit errors in standard contexts
        trimmed_text = text[:30000] 
        
        prompt = f"{system_prompt}\n\nContract Text:\n{trimmed_text}"
        
        response_text = llm_service.generate_content(prompt)
        
        # Parse JSON from response
        return self._parse_json_list(response_text)

    def _parse_json_list(self, text: str) -> List[Dict[str, Any]]:
        try:
            # Clean up potential markdown formatting wrapping the JSON
            cleaned = text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            # Find the first '[' and last ']' to extract JSON list
            start = cleaned.find("[")
            end = cleaned.rfind("]")
            if start != -1 and end != -1:
                cleaned = cleaned[start:end+1]
                
            return json.loads(cleaned)
        except Exception as e:
            print(f"Failed to parse JSON from LLM output: {e}. Raw: {text}")
            # Return basic list of matches based on keyword fallback if parsing fails
            return self._keyword_fallback(text)

    def _keyword_fallback(self, text: str) -> List[Dict[str, Any]]:
        # A simple fallback parser
        clauses = []
        # Attempt to look for object structures
        matches = re.findall(r'\{\s*"type"\s*:\s*"([^"]+)"\s*,\s*"content"\s*:\s*"([^"]+)"\s*,\s*"risk_level"\s*:\s*"([^"]+)"\s*\}', text)
        for m in matches:
            clauses.append({
                "type": m[0],
                "content": m[1],
                "risk_level": m[2]
            })
        if not clauses:
            # Absolute fallback
            clauses.append({
                "type": "Other",
                "content": "Failed to parse clauses from LLM response. Please review raw output.",
                "risk_level": "Medium"
            })
        return clauses

extraction_agent = ExtractionAgent()
