from state import ScrappyInvestigationState

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
            "metrics_mentioned": "list of business metrics referenced in the question",
            "dimensions": "list of analytical dimensions relevant to the question",
            "tables_needed": "list of database tables required to answer the question"
        }}
        """

    def PlannerAgentPrompt(state:ScrappyInvestigationState):

        state = state
        return f"""You are a data investigation planner for a retail analytics system.

        Given a business question, create a structured investigation plan to uncover insights.

        Question Type: {state['question_type']}
        Metrics: {state['metrics_mentioned']}
        Dimensions: {state['dimensions']}

        Generate 3-4 logical investigation steps that progressively drill deeper into the problem.
        Each step should build on the previous one.

        Return ONLY a JSON object with these fields:
        {{
            "investigation_steps": [
                {{
                    "number": "sequential step number",
                    "action": "specific analytical action to take",
                    "why": "reason this step helps answer the question"
                }}
            ],
            "focus_areas": "list of specific dimensions or patterns worth investigating"
        }}"""
    
    def QueryBuilderAgentPrompt(state:ScrappyInvestigationState):
        state = state

        return f"""
        
        Below is the database schema.

SCHEMA:
=======

Table: stores
- store_id (int, PK)
- store_name (varchar)
- city (varchar)
- state (varchar)
- region (varchar)

Table: products
- product_id (int, PK)
- product_name (varchar)
- category (varchar)
- brand (varchar)
- price (decimal)

Table: sales_fact
- sale_id (int, PK)
- store_id (int, FK -> stores.store_id)
- product_id (int, FK -> products.product_id)
- date_id (int, FK -> calendar_dim.date_id)
- quantity_sold (int)
- revenue (decimal)
- cost (decimal)
- profit (decimal)

Table: inventory_snapshots
- snapshot_id (int, PK)
- store_id (int, FK -> stores.store_id)
- product_id (int, FK -> products.product_id)
- date_id (int, FK -> calendar_dim.date_id)
- inventory_level (int)

Table: calendar_dim
- date_id (int, PK)
- full_date (date)
- day_of_week (varchar)
- month (int)
- quarter (int)
- year (int)

Table: promotions
- promo_id (int, PK)
- product_id (int, FK -> products.product_id)
- start_date (date)
- end_date (date)
- discount_pct (decimal)
- campaign_name (varchar)

RELATIONSHIPS:
==============
- sales_fact connects to stores, products, and calendar_dim via foreign keys
- inventory_snapshots connects to stores, products, and calendar_dim via foreign keys
- promotions connects to products via product_id

OUTPUT:
=======
Generate a MySQL query for the following investigation steps:

investigation_steps: {state['investigation_steps']}
focus:{state['focus_areas']}

Return ONLY the SQL query in json format. Do not wrap the response in markdown code blocks.
{{
    sql_queries:[]
}}

"""
        

    def DataRetrievalAgentPrompt(state:ScrappyInvestigationState):
        pass

    def SummaryAgentPrompt(state:ScrappyInvestigationState):
        pass

