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
        pass

    def query_builder_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        pass

    def data_retrieval_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        pass

    def summary_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        pass

