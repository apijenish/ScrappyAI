from state import ScrappyInvestigationState
from prompts import ScrappyAgentPrompt
from engine import ScrappyReasonEngine



class ScrappyInvestigationAgent:

    def __init__(self):
        self.engine = ScrappyReasonEngine()

    def intent_agent(self, state:ScrappyInvestigationState)-> ScrappyInvestigationState:
        
        #Get the Intent Agent prompt
        prompt = ScrappyAgentPrompt.IntentAgentPrompt(state)
        result = self.engine.invoke_llm(prompt)

        #Update the state
        state['question_type']=result.get("question_type")
        state['metrics_mentioned'] = result.get("metrics_mentioned")
        state['dimensions']=result.get("dimensions")

        return state


    def planner_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        prompt = ScrappyAgentPrompt.PlannerAgentPrompt(state)
        result = self.engine.invoke_llm(prompt)

        state['investigation_steps']=result.get("investigation_steps")
        state['focus_areas']=result.get("focus_areas")

        return state

    def query_builder_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        prompt = ScrappyAgentPrompt.QueryBuilderAgentPrompt(state)
        result = self.engine.invoke_llm(prompt)

        for sql in result['sql_queries']:
            print(sql["query"])

        print(result)

        state['generated_queries'].extend(result['sql_queries'])
        return state

    def data_retrieval_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        query_results = []

        for sql_item in state.get('generated_queries', []):
            query = sql_item.get("query", "")
            label = sql_item.get("label", "Query")

            print(f"\n[DataRetrieval] Running: {label}")
            print(f"{query}")
            result = self.engine.execute_sql(query)

            query_results.append({
                "label": label,
                "query": query,
                "columns": result["columns"],
                "rows": result["rows"],       # list of dicts
                "error": result["error"],
            })

            if result["error"]:
                print(f"SQL Error: {result['error']}")
            else:
                print(f"Returned {len(result['rows'])} rows")

        state['query_results'] = query_results
        return state

    def summary_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        pass

