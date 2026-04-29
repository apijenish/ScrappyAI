from langchain_ollama import ChatOllama
import json
import mysql.connector
from mysql.connector import Error
import os
import re

class ScrappyReasonEngine:

    #model_name = "llama3.1" deepseek-coder-v2 llama3.2 mistral-nemo
    model_name = "gemma4:31b-cloud"
    temperature = 0

    DB_CONFIG = {
        "host": os.environ.get("DB_HOST"),
        "port": os.environ.get("DB_PORT"),
        "database": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
    }

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

    def invoke_llm(self, prompt):
        response = self.llm.invoke(prompt)
        parsed = self._extract_jsons(response.content)
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
    # def _extract_jsons(self, text: str) -> dict:

    #     text = text.strip()

    #     # 1. Strip markdown code blocks (```json, ```python, ``` etc.)
    #     if "```" in text:
    #         match = re.search(r'```(?:\w+)?\n?(.*?)\n?```', text, re.DOTALL)
    #         if match:
    #             text = match.group(1).strip()

    #     # 2. Try to isolate a complete JSON object {...}
    #     json_match = re.search(r'\{.*\}', text, re.DOTALL)
    #     if json_match:
    #         text = json_match.group(0)
    #     else:
    #         # 3. No closing brace found — LLM truncated the output.
    #         #    Find the opening brace and take everything from there.
    #         open_idx = text.find('{')
    #         if open_idx != -1:
    #             text = text[open_idx:]

    #     # 4. First attempt: parse as-is
    #     try:
    #         return json.loads(text)
    #     except json.JSONDecodeError:
    #         pass

    #     # 5. Recovery: try closing any open brackets/braces to salvage truncated JSON.
    #     #    Strip trailing commas (common when truncated mid-field), then close structures.
    #     recovered = text.rstrip().rstrip(',')

    #     # Count unclosed brackets and braces
    #     open_braces   = recovered.count('{') - recovered.count('}')
    #     open_brackets = recovered.count('[') - recovered.count(']')

    #     # Close any open arrays first, then objects
    #     recovered += ']' * max(open_brackets, 0)
    #     recovered += '}' * max(open_braces, 0)

    #     try:
    #         result = json.loads(recovered)
    #         print(f"[Engine] Recovered truncated JSON successfully.")
    #         return result
    #     except json.JSONDecodeError as e:
    #         print(f"[Engine] JSON parse failed after recovery attempt: {e}")
    #         print(f"[Engine] Raw LLM output:\n{text[:400]}")
    #         return {}
    
    def _extract_jsons(self, text: str) -> dict:
        text = text.strip()

        # 1. Strip markdown code blocks
        if "```" in text:
            match = re.search(r'```(?:\w+)?\n?(.*?)\n?```', text, re.DOTALL)
            if match:
                text = match.group(1).strip()

        # 2. Find the first COMPLETE JSON object using bracket counting
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

    #Format the summary output to plain english
    @staticmethod
    def escape_markdown(text: str) -> str:
        """Escape characters that Streamlit/Markdown would misinterpret"""
        text = text.replace("$", r"$")   # Prevent LaTeX math rendering
        text = text.replace("_", r"_")   # Prevent italic rendering
        return text

