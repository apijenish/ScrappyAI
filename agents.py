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
        pass

    def summary_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        pass

