from state import ScrappyInvestigationState

class ScrappyAgentPrompt:

    def IntentAgentPrompt(state:ScrappyInvestigationState)->str:

        question = state['question']
        _intentAgentPrompt =f"""Analyze this business question and extract key information.
        Question: {question}"""

        return _intentAgentPrompt
