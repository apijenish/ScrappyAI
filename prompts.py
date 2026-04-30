# every LLM prompt used by ScrappyAI's agents.

from state import ScrappyInvestigationState

SCHEMA = """
DATABASE CONTEXT:
=================
Synthetic retail analytics database. Star schema with sales_fact as the central fact table.
All date filtering MUST go through calendar_dim via date_id — there are no raw DATE columns
in the fact or junction tables (except calendar_dim.full_date itself).

TABLES:
=======

Table: calendar_dim
  Purpose : Time dimension. Always JOIN this table when filtering or grouping by any date attribute.
  Columns :
    date_id      INT          PRIMARY KEY
    full_date    DATE         Actual calendar date — use for date range filters: full_date BETWEEN '2025-01-01' AND '2025-03-31'
    day_of_week  VARCHAR(20)  e.g. 'Monday', 'Tuesday'
    month        INT          Numeric month 1-12. Use month = 5 for May, NOT month = 'May'
    quarter      INT          Numeric quarter 1-4
    year         INT          Four-digit year e.g. 2025

Table: stores
  Purpose : Physical retail location attributes.
  Columns :
    store_id     INT          PRIMARY KEY
    store_name   VARCHAR(255)
    city         VARCHAR(100)
    state        VARCHAR(100)
    region       VARCHAR(100)

Table: products
  Purpose : Product metadata catalogue for all items sold.
  Columns :
    product_id   INT           PRIMARY KEY
    product_name VARCHAR(255)
    category     VARCHAR(100)
    brand        VARCHAR(100)
    price        DECIMAL(10,2) List price of the product

Table: sales_fact  ← CENTRAL FACT TABLE
  Purpose : Transactional sales records. Start every revenue, profit, or volume query here.
  Columns :
    sale_id       INT           PRIMARY KEY
    store_id      INT           FK → stores.store_id
    product_id    INT           FK → products.product_id
    date_id       INT           FK → calendar_dim.date_id
    quantity_sold INT
    revenue       DECIMAL(12,2)
    cost          DECIMAL(12,2)
    profit        DECIMAL(12,2) Pre-computed: revenue - cost

Table: inventory_snapshots
  Purpose : Point-in-time inventory levels per store, product, and date.
            Use for stock availability, out-of-stock risk, or replenishment analysis.
  Columns :
    snapshot_id     INT  PRIMARY KEY
    store_id        INT  FK → stores.store_id
    product_id      INT  FK → products.product_id
    date_id         INT  FK → calendar_dim.date_id
    inventory_level INT

Table: promotions
  Purpose : Promotional campaigns linked to products over a date range.
            Use to correlate discount activity with sales spikes or margin changes.
  Columns :
    promo_id      INT           PRIMARY KEY
    product_id    INT           FK → products.product_id
    start_date_id INT           FK → calendar_dim.date_id (start of promotion window)
    end_date_id   INT           FK → calendar_dim.date_id (end of promotion window)
    discount_pct  DECIMAL(5,2)  e.g. 15.00 means 15% discount
    campaign_name VARCHAR(255)

   promotions has NO direct DATE columns. To filter by date range, JOIN calendar_dim twice:
    JOIN calendar_dim cd_start ON promotions.start_date_id = cd_start.date_id
    JOIN calendar_dim cd_end   ON promotions.end_date_id   = cd_end.date_id

RELATIONSHIPS:
==============
sales_fact.store_id            → stores.store_id
sales_fact.product_id          → products.product_id
sales_fact.date_id             → calendar_dim.date_id
inventory_snapshots.store_id   → stores.store_id
inventory_snapshots.product_id → products.product_id
inventory_snapshots.date_id    → calendar_dim.date_id
promotions.product_id          → products.product_id
promotions.start_date_id       → calendar_dim.date_id
promotions.end_date_id         → calendar_dim.date_id

QUERY RULES (always follow):
=============================
- Filter by month using integers:   c.month = 5        (not 'May')
- Filter by day name using strings: c.day_of_week = 'Monday'
- Filter by date range using:       c.full_date BETWEEN '2025-01-01' AND '2025-12-31'
- promotions date filtering REQUIRES two calendar_dim JOINs (see alias pattern above)
- Always alias aggregates:          SUM(revenue) AS total_revenue
- Always ORDER BY for ranked results, LIMIT 500 unless all rows are explicitly needed
- No semicolons at end of query
"""

class ScrappyAgentPrompt:

    @staticmethod
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

    @staticmethod
    def PlannerAgentPrompt(state:ScrappyInvestigationState):

        state = state
        return f"""You are a data investigation planner for a retail analytics system.

        Given a business question, create a structured investigation plan to uncover insights.

        Question Type: {state['question_type']}
        Metrics: {state['metrics_mentioned']}
        Dimensions: {state['dimensions']}

        Generate 2-3 logical investigation steps that progressively drill deeper into the problem.
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
    
    @staticmethod
    def QueryBuilderAgentPrompt(state:ScrappyInvestigationState, step:dict):

        original_question = state.get("question")

        return f"""You are an expert MySQL query writer for a database.

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
        - LIMIT 500 rows unless the step explicitly needs all rows
        - No semicolons at the end

        {SCHEMA}

        Return a JSON object in exactly this format
        Do not include any explanation
        The query must be a single line with no newlines or indentation:

        {{"label": "{step['label']}", "query": "SELECT ... FROM ... WHERE ..."}}

        """        

    @staticmethod
    def QueryValidateAgentPrompt(state: ScrappyInvestigationState, step: dict):
        label = step.get('label')
        query = step.get('query')
        error = step.get('error')

        return f"""You are an expert MySQL query writer.

        THE FOLLOWING QUERY FAILED — DO NOT reproduce it:
        ==================================================
        Label : {label}
        Query : {query}
        Error : {error}

        Your job is to write a DIFFERENT, corrected query that fixes the error above.
        Do NOT copy the original query. Rewrite it from scratch using the schema below.

        Before writing the query, identify:
        1. What specifically caused the error
        2. Which table or column name is wrong or missing
        3. What the correct fix is

        {SCHEMA}

        Return ONLY a JSON object. No explanation. Query must be a single line:
        {{"label": "{label}", "query": "SELECT ... FROM ... WHERE ..."}}
        """
        

    @staticmethod
    def DataRetrievalAgentPrompt(state:ScrappyInvestigationState):
        pass # Data retrieval is handled directly in the agent; no LLM prompt needed


    @staticmethod
    def SummaryAgentPrompt(state: ScrappyInvestigationState):

        # Summarize results
        results_text = ""
        for r in state.get("query_results", []): 
            results_text += f"\n- {r['label']}: {len(r['rows'])} rows returned."
            if r.get('error'):
                results_text += f" (Failed: {r['error']})"
            elif r['rows']:
                # Only send first 1000 rows as a sample, not all rows
                results_text += f"\n  Columns: {r['columns']}"
                results_text += f"\n  Sample data (first 1000 rows): {r['rows'][:1000]}"

        return f"""You are an expert business analyst. You have years worth of operational and sales experience. Answer the question below using the data provided.

        IMPORTANT: You must respond with ONLY a JSON object. 
        Do NOT write any code. Do NOT write any explanation outside the JSON.
        Do NOT use markdown. Just the raw JSON object and nothing else.

        FORMATTING RULES (always follow):
        - All monetary values must include a dollar sign: $3,461,976.88 not 3,461,976.88
        - All percentages must include a percent sign: 12.5% not 12.5
        - All quantities must include a unit: 1,200 units not 1,200
        - Round monetary values to 2 decimal places
        - Use commas as thousands separators

        Question: "{state.get('question')}"

        Data collected:
        {results_text}

        Respond with exactly this JSON structure:
        {{
            "summary": "Summarize in plain English answer to the question based on the data in few sentences. Always include $ for money, % for percentages, and appropriate units for quantities.",
            "next_steps": ["follow-up action 1", "follow-up action 2"]
        }}"""
        

