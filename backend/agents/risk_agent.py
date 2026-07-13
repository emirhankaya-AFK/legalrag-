import yaml
import json
from pathlib import Path
from typing import List, Dict, Any
from ..services.llm_service import llm_service

class RiskAgent:
    def __init__(self):
        self.rules_path = Path(__file__).resolve().parent.parent / "config" / "risk_rules.yaml"
        self.prompt_path = Path(__file__).resolve().parent.parent / "config" / "prompts.yaml"
        self._load_config()

    def _load_config(self):
        # Load risk rules
        try:
            with open(self.rules_path, "r") as f:
                self.rules_data = yaml.safe_load(f)
                self.rules = self.rules_data.get("rules", [])
        except Exception as e:
            print(f"Error loading risk_rules.yaml: {e}")
            self.rules = []

        # Load prompts
        try:
            with open(self.prompt_path, "r") as f:
                self.prompts = yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading prompts.yaml: {e}")
            self.prompts = {}

    def analyze_risk(self, clauses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes the extracted clauses, matches them against the risk rules,
        calculates the normalized risk score (0-100), and generates explanations.
        """
        if not clauses:
            return {"risk_score": 0, "explanations": [], "triggered_rules": []}

        # Format clauses for LLM prompt
        clauses_str = json.dumps(clauses, indent=2)
        rules_str = yaml.dump(self.rules)
        
        system_prompt = self.prompts.get("risk_analysis", "")
        
        prompt = (
            f"{system_prompt}\n\n"
            f"Here are the rules to evaluate:\n{rules_str}\n\n"
            f"Here are the extracted contract clauses:\n{clauses_str}\n\n"
            f"Analyze and identify which of the rules are triggered. For each triggered rule, "
            f"explain why it is triggered based on the clause content. Return a JSON list of objects "
            f"containing 'rule_id', 'clause_type', 'risk_explanation', and 'severity'."
        )
        
        response_text = llm_service.generate_content(prompt)
        triggered_results = self._parse_json_list(response_text)
        
        # Calculate risk score based on rules matching
        total_points = 0
        max_points = sum(rule.get("points", 0) for rule in self.rules)
        triggered_rules_list = []
        
        # Map of rule_id to rule details
        rules_map = {rule["id"]: rule for rule in self.rules}
        
        for tr in triggered_results:
            rule_id = tr.get("rule_id")
            # If the LLM returned a valid rule_id that exists in our rules
            if rule_id in rules_map:
                rule = rules_map[rule_id]
                if rule_id not in [r["id"] for r in triggered_rules_list]:
                    total_points += rule.get("points", 0)
                    triggered_rules_list.append({
                        "id": rule_id,
                        "name": rule.get("name"),
                        "points": rule.get("points"),
                        "explanation": tr.get("risk_explanation", ""),
                        "severity": tr.get("severity", "Medium")
                    })
                    
        # Normalize score to 0 - 100
        risk_score = 0
        if max_points > 0:
            risk_score = int((total_points / max_points) * 100)
            
        return {
            "risk_score": min(100, max(0, risk_score)),
            "explanations": triggered_results,
            "triggered_rules": triggered_rules_list
        }

    def _parse_json_list(self, text: str) -> List[Dict[str, Any]]:
        try:
            cleaned = text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            start = cleaned.find("[")
            end = cleaned.rfind("]")
            if start != -1 and end != -1:
                cleaned = cleaned[start:end+1]
                
            return json.loads(cleaned)
        except Exception as e:
            print(f"Failed to parse risk JSON list: {e}. Raw: {text}")
            # Return empty or construct basic list from rules
            return []

risk_agent = RiskAgent()
