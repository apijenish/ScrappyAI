from StateDefinition import InvestigationState


class ScrappyInvestigationAgents:

    def __init__(self):
        pass

    def intent_agent(self, state:InvestigationState)-> InvestigationState:
        pass

    def planner_agent(self, state:InvestigationState)->InvestigationState:
        pass

    def query_builder_agent(self, state:InvestigationState)->InvestigationState:
        pass

    def data_retrieval_agent(self, state:InvestigationState)->InvestigationState:
        pass

    def summary_agent(self, state:InvestigationState)->InvestigationState:
        pass

