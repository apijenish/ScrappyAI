from state import ScrappyInvestigationState

SCHEMA = """
SCHEMA:
=======
Table: stores           → store_id (PK), store_name, city, state, region
Table: products         → product_id (PK), product_name, category, brand, price
Table: sales_fact       → sale_id (PK), store_id*, product_id*, date_id*, quantity_sold, revenue, cost, profit
Table: inventory_snapshots → snapshot_id (PK), store_id*, product_id*, date_id*, inventory_level
Table: calendar_dim     → date_id (PK), full_date (DATE), day_of_week, month, quarter, year
Table: promotions       → promo_id (PK), product_id*, start_date (DATE), end_date (DATE), discount_pct, campaign_name

(* = foreign key)

RELATIONSHIPS:
==============
sales_fact.store_id      → stores.store_id
sales_fact.product_id    → products.product_id
sales_fact.date_id       → calendar_dim.date_id
inventory_snapshots.*    → same pattern as sales_fact
promotions.product_id    → products.product_id
"""


class ScrappyAgentPrompt:

    def IntentAgentPrompt(state:ScrappyInvestigationState):

        question = state['question']
        return f"""

        Analyze this business question and extract key information needed to query a retail database.
        Question: "{question}"
        Return ONLY a valid JSON object.
        - Do not add comments or annotations inside the JSON
        - Do not add explanations in parentheses next to values
        - Do not wrap in markdown code blocks
        - All values must be valid JSON types: string, number, array, object, or boolean
        {{
            "question_type": "the type of analysis being requested",
            "metrics_mentioned": "Business metrics referenced in the question",
            "dimensions": "Analytical dimensions relevant to the question",
            "tables_needed": "Database tables required to answer the question"
        }}
        """

    def PlannerAgentPrompt(state:ScrappyInvestigationState):

        state = state
        return f"""You are a data investigation planner for a retail analytics system.

        Given a business question, create a structured investigation plan to uncover insights.

        Question Type: {state['question_type']}
        Metrics: {state['metrics_mentioned']}
        Dimensions: {state['dimensions']}

        Generate 1 logical investigation steps that progressively drill deeper into the problem.
        Each step should build on the previous one.

        Return ONLY a JSON object with these fields:
        {{
            "investigation_steps": [
                {{
                    "number": "sequential step number",
                    "label": "short title e.g. Weekly Revenue Trend",
                    "action": "specific analytical action to take",
                    "why": "reason this step helps answer the question"
                }}
            ],
            "focus_areas": "list of specific dimensions or patterns worth investigating"
        }}"""
    
    def QueryBuilderAgentPrompt(state:ScrappyInvestigationState, step:dict):

        original_question = state.get("question")

        return f"""You are an expert MySQL query writer for a retail analytics database.

TASK:
=====
Write exactly ONE MySQL SELECT query to accomplish this investigation step.

Step label : {step['label']}
Step action: {step['action']}
Step why   : {step['why']}

CONTEXT:
========
Original question  : "{original_question}"
Metrics of interest: {state.get('metrics_mentioned')}
Dimensions         : {state.get('dimensions')}

QUERY RULES:
============
- Valid MySQL only — use CURDATE(), DATE_SUB(), DATEDIFF() for date math
- Always JOIN calendar_dim for any date filtering (join on date_id)
- Always alias aggregated columns: SUM(revenue) AS total_revenue
- Prefer JOINs over subqueries for readability
- Add ORDER BY for any ranked or trended results
- LIMIT 50 rows unless the step explicitly needs all rows
- No semicolons at the end

{SCHEMA}

Return a JSON object in exactly this format
Do not include any explanation
The query must be a single line with no newlines or indentation:

{{"label": "{step['label']}", "query": "SELECT ... FROM ... WHERE ..."}}

"""        

    def DataRetrievalAgentPrompt(state:ScrappyInvestigationState):
        pass

    def SummaryAgentPrompt(state: ScrappyInvestigationState):
        results_text = ""
        for r in state.get("query_results", []):
            results_text += f"\n{r['label']}: {len(r['rows'])} rows returned."
            if r['error']:
                results_text += f" (Error: {r['error']})"

        return f"""You are a business analyst summarizing data investigation results.

Original question: "{state.get('question')}"
Data gathered: {results_text}

Return ONLY a JSON object:
{{
    "summary": "2-3 sentence plain English answer to the original question",
    "next_steps": ["follow-up action 1", "follow-up action 2"]
}}"""

        

