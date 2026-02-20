from StateDefinition import InvestigationState
from AgentPrompts import ScrappyAgentsPrompts


class ScrappyInvestigationAgents:

    def __init__(self):
        pass

    def intent_agent(self, state:InvestigationState)-> InvestigationState:
        
        #Get the Intent Agent prompt
        question = ScrappyAgentsPrompts.IntentAgentPrompt(state)
        print(question)

        #Test the state
        state['notebook'] = "Jenish"

        return state


    def planner_agent(self, state:InvestigationState)->InvestigationState:
        pass

    def query_builder_agent(self, state:InvestigationState)->InvestigationState:
        pass

    def data_retrieval_agent(self, state:InvestigationState)->InvestigationState:
        pass

    def summary_agent(self, state:InvestigationState)->InvestigationState:
        pass

