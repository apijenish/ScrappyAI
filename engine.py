from langchain_ollama import ChatOllama
import json

class ScrappyReasonEngine:

    model_name = "llama3.1"
    temperature = 0.3

    def __init__(self):
        self.llm = ChatOllama(model=self.model_name,temperature=self.temperature)

    def invoke_llm(self, prompt):
        response = self.llm.invoke(prompt)
        pasrsed = self._extract_json(response.content)
        return pasrsed

    # Helper methods
    def _extract_json(self, text: str) -> dict:
        """Extract JSON from LLM response"""
        # Remove markdown code blocks
        text = text.strip()
        if "```" in text:
            import re
            match = re.search(r'```(?:json)?\n(.*?)\n```', text, re.DOTALL)
            if match:
                text = match.group(1)
        
        return json.loads(text)
    




    
