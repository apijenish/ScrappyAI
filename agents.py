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

        print("Intent Agent")
        print("***************************")

        print(state["question_type"])
        print(state["metrics_mentioned"])
        print(state["dimensions"])

        return state


    def planner_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        prompt = ScrappyAgentPrompt.PlannerAgentPrompt(state)
        result = self.engine.invoke_llm(prompt)

        state['investigation_steps']=result.get("investigation_steps")
        state['focus_areas']=result.get("focus_areas")

        print("Planner Agent")
        print("***************************")

        print(state["investigation_steps"])
        print(state["focus_areas"])

        return state

    def query_builder_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:

        print("Query Builder Agent")
        print("***************************")

        state['generated_queries'] = []

        validation_errors = state.get('validation_errors',[])

        if validation_errors:
            print("there are few errors")

        else:
            
            for step in state.get("investigation_steps",[]):           
                prompt = ScrappyAgentPrompt.QueryBuilderAgentPrompt(state, step)
                result = self.engine.invoke_llm(prompt)
                state['generated_queries'].append(result)


        for sql in state['generated_queries']:
            print(sql)

        print(result)

        
        return state
    
    def validator_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        print("Validator Agent")
        print("***************************")

        validation_errors=[]

        for sql_item in state.get('generated_queries',[]):
            query = sql_item.get("query", "")
            label = sql_item.get("label", "Query")

            result = self.engine.execute_sql(query)

            if result.get('error'):
                validation_errors.append({'label':label,
                                          'query':query,
                                          'error':result.get('error')})
                
        state["validation_error"]=validation_errors

        return state


    def data_retrieval_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:

        print("Data Retrieval Agent")

        print("***************************")
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
                "rows": result["rows"],      
                "error": result["error"],
            })

            if result["error"]:
                print(f"SQL Error: {result['error']}")
            else:
                print(f"Returned {len(result['rows'])} rows")

        state['query_results'] = query_results
        return state

    def summary_agent(self, state: ScrappyInvestigationState) -> ScrappyInvestigationState:
        prompt = ScrappyAgentPrompt.SummaryAgentPrompt(state)
        result = self.engine.invoke_llm(prompt)
        state['summary'] = result.get("summary", "No summary available.")
        state['next_steps'] = result.get("next_steps", [])
        return state

