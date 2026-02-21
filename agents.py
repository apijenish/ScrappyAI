from state import ScrappyInvestigationState
from prompts import ScrappyAgentPrompt


class ScrappyInvestigationAgent:

    def __init__(self):
        pass

    def intent_agent(self, state:ScrappyInvestigationState)-> ScrappyInvestigationState:
        
        #Get the Intent Agent prompt
        question = ScrappyAgentPrompt.IntentAgentPrompt(state)
        print(question)

        #Test the state
        state['notebook'] = "Jenish"

        return state


    def planner_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        pass

    def query_builder_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        pass

    def data_retrieval_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        pass

    def summary_agent(self, state:ScrappyInvestigationState)->ScrappyInvestigationState:
        pass

