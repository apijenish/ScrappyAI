from langchain_ollama import ChatOllama
import json
import mysql.connector
from mysql.connector import Error

class ScrappyReasonEngine:

    model_name = "llama3.1"
    temperature = 0

    DB_CONFIG = {
        "host":"localhost",
        "port":"3306",
        "database":"scrappy_data",
        "user":"root",
        "password":"root"
    }

    def __init__(self):
        self.llm = ChatOllama(model=self.model_name,temperature=self.temperature)

    def invoke_llm(self, prompt):
        response = self.llm.invoke(prompt)
        parsed = self._extract_json(response.content)
        return parsed
    
    def execute_sql(self, query:str):
        try:
            conn = mysql.connector.connect(**self.DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            cursor.close()
            conn.close()
            return {"columns": columns, "rows": rows, "error": None}
        except Error as e:
            return {"columns": [], "rows": [], "error": str(e)}



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
    



 
