from state import ScrappyInvestigationState

class ScrappyAgentPrompt:

    def IntentAgentPrompt(state:ScrappyInvestigationState):

        question = state['question']
        return f"""Analyze this business question and extract key information.
        Question: {question}
        You must respond with ONLY a valid JSON object. No explanation, no markdown, 
        no extra text — just the raw JSON object.
        {{
            "question_type": "...",
            "metrics_mentioned": [],
            "dimensions": []
        }}"""

    def PlannerAgentPrompt(state:ScrappyInvestigationState):
        pass
    
    def QueryBuilderAgentPrompt(state:ScrappyInvestigationState):
        pass

    def DataRetrievalAgentPrompt(state:ScrappyInvestigationState):
        pass

    def SummaryAgentPrompt(state:ScrappyInvestigationState):
        pass

