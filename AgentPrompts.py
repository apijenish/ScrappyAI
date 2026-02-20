from StateDefinition import InvestigationState

class ScrappyAgentsPrompts:

    def IntentAgentPrompt(state:InvestigationState)->str:

        question = state['question']
        _intentAgentPrompt =f"""Analyze this business question and extract key information.
        Question: {question}"""

        return _intentAgentPrompt
