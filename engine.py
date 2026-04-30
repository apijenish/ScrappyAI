# This code has two responsibilities. Invoke the LLM and Execute the SQL
# All agents share a single instance of ScrappyReasonEngine

from langchain_ollama import ChatOllama
import json
import mysql.connector
from mysql.connector import Error
import os
import re

class ScrappyReasonEngine:

    # LLM Configuration
    model_name = os.environ.get("LLM_MODEL")
    temperature = 0

    # DB Configuration
    DB_CONFIG = {
        "host": os.environ.get("DB_HOST"),
        "port": os.environ.get("DB_PORT"),
        "database": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
    }

    # Initialises the ChatOllama client.
    def __init__(self):
        self.llm = ChatOllama(
            model=self.model_name,
            temperature=self.temperature,
            format="json",
            base_url="https://ollama.com",
            client_kwargs={
                "headers": {
                    "Authorization": f"Bearer {os.environ.get('OLLAMA_API_KEY')}"
                }
            }
        )

    # Send a prompt to the LLM and return the parsed JSON response
    def invoke_llm(self, prompt):
        response = self.llm.invoke(prompt)
        parsed = self._extract_jsons(response.content)
        return parsed
    
    # Execute a single SELECT query
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


    # Private Helper methods       
    def _extract_jsons(self, text: str) -> dict:
        text = text.strip()

        # Strip markdown code blocks
        if "```" in text:
            match = re.search(r'```(?:\w+)?\n?(.*?)\n?```', text, re.DOTALL)
            if match:
                text = match.group(1).strip()

        # Find the first COMPLETE JSON object using bracket counting
        start = text.find('{')
        if start == -1:
            print("[Engine] No JSON object found in LLM output.")
            return {}

        depth = 0
        in_string = False
        escape_next = False

        for i, ch in enumerate(text[start:], start=start):
            if escape_next:
                escape_next = False
                continue
            if ch == '\\' and in_string:
                escape_next = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    candidate = text[start:i+1]
                    try:
                        return json.loads(candidate)
                    except json.JSONDecodeError as e:
                        print(f"[Engine] JSON parse failed: {e}")
                        print(f"[Engine] Raw LLM output:\n{candidate[:400]}")
                        return {}

        print("[Engine] Could not find a complete JSON object.")
        return {}

    # Format the summary output to plain english
    @staticmethod
    def escape_markdown(text: str) -> str:
        """Escape characters that Streamlit/Markdown would misinterpret"""
        text = text.replace("$", r"$")
        text = text.replace("_", r"_")
        return text

