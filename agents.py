
# Contains every agent node in the ScrappAI Pipeline
# All agent nodes into a single class
# ---------------------------------------------------


from state import ScrappyInvestigationState
from prompts import ScrappyAgentPrompt
from engine import ScrappyReasonEngine


class ScrappyInvestigationAgent:
    #One engine shared by every agents.
    def __init__(self):
        self.engine = ScrappyReasonEngine()

    # Analyse the user's raw question and extract structured intent data.
    def intent_agent(self, state:ScrappyInvestigationState)-> ScrappyInvestigationState:
        
        print("\n")
        print("Intent Agent")
        print("***************************")
        print("\n")

        # Build the prompt using the current state and invoke the LLM
        prompt = ScrappyAgentPrompt.IntentAgentPrompt(state)
        result = self.engine.invoke_llm(prompt)

        # Update the state
        state['question_type']=result.get("question_type")
        state['metrics_mentioned'] = result.get("metrics_mentioned")
        state['dimensions']=result.get("dimensions")

        print(state["question_type"])
        print(state["metrics_mentioned"])
        print(state["dimensions"])

        return state

    # Convert the structured intent into a concrete investigation plan.
    def planner_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        
        print("\n")
        print("Planner Agent")
        print("***************************")
        print("\n")

        # Build the prompt using the current state and invoke the LLM
        prompt = ScrappyAgentPrompt.PlannerAgentPrompt(state)
        result = self.engine.invoke_llm(prompt)

        # Update the state
        state['investigation_steps']=result.get("investigation_steps")
        state['focus_areas']=result.get("focus_areas")

        print(state["investigation_steps"])
        print(state["focus_areas"])

        return state

    # Translate each investigation step (or failed query) into a MySQL SELECT query.    
    def query_builder_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:

        print("\n")
        print("Query Builder Agent")
        print("***************************")
        print("\n") 

        # Retry if there are any failed queries
        validation_errors = state.get('validation_errors',[])

        if validation_errors:
            for failed_query in state.get('validation_errors'):
                prompt = ScrappyAgentPrompt.QueryValidateAgentPrompt(state, failed_query)
                result = self.engine.invoke_llm(prompt)
                state['generated_queries'].append(result)
            
        else:

            # Generate all the queries from scratch    
            state['generated_queries'] = []
            
            for passed_query in state.get("investigation_steps",[]):           
                prompt = ScrappyAgentPrompt.QueryBuilderAgentPrompt(state, passed_query)
                result = self.engine.invoke_llm(prompt)
                state['generated_queries'].append(result)


        for sql in state['generated_queries']:
            print(sql)

        return state

    # Validate every generated query by actually executing it against the DB.
    # The conditional edge in workflow.py reads validation_errors and retry_count
    # to decide whether to loop back to query_builder or proceed to data_retrieval.
    def validator_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        
        print("\n")
        print("Validator Agent")
        print("***************************")
        print("\n")

        errors=[]
        passed=[]

        # Iterate over the generated queries
        for sql_item in state.get('generated_queries',[]):
            query = sql_item.get("query", "")
            label = sql_item.get("label", "Query")

            result = self.engine.execute_sql(query)
            # If the query could not be executed
            if result.get('error') or len(result.get('rows', [])) == 0:
                errors.append({'label':label,
                                          'query':query,
                                          'error':result.get('error')})
            # If the query passed    
            else:
                passed.append(sql_item)
        if len(errors)>0:
            print("Failed queries found")

        # Update the state        
        state['validation_errors'] = errors
        state['generated_queries'] = passed
        state["retry_count"] = state.get('retry_count',0) + 1

        return state

    # Execute all validated queries and collect their full result sets.
    def data_retrieval_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:

        print("\n")
        print("Data Retrieval Agent")
        print("***************************")
        print("\n")

        query_results = []

        for sql_item in state.get('generated_queries', []):
            query = sql_item.get("query", "")
            label = sql_item.get("label", "Query")

            print(f"\n[DataRetrieval] Running: {label}")
            print(f"{query}")
            result = self.engine.execute_sql(query)

            # Store everything the summary agent needs
            query_results.append({
                "label": label,
                "query": query,
                "columns": result["columns"],
                "rows": result["rows"],      
                "error": result["error"],
            })

            if result["error"]:
                print(f"SQL Error: {result['error']}")
            else:
                print(f"Returned {len(result['rows'])} rows")

        # Update state
        state['query_results'] = query_results
        return state
    
    # Summarize all DB query results into a plain-English business answer.
    def summary_agent(self, state: ScrappyInvestigationState) -> ScrappyInvestigationState:

        print("\n")
        print("Summary Agent")
        print("***************************")
        print("\n")

        prompt = ScrappyAgentPrompt.SummaryAgentPrompt(state)
        result = self.engine.invoke_llm(prompt)

        # format the summary text for safe Markdown rendering in Streamlit
        # state['summary'] = ScrappyReasonEngine.escape_markdown(result.get("summary", "No summary available."))
        state['summary'] = result.get("summary", "No summary available.")
        print(result.get("summary"))

        # Update the state
        state['next_steps'] = result.get("next_steps", [])

        return state

