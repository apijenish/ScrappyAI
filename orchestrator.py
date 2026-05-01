# entry point that bridges the Streamlit UI and the LangGraph workflow

from langchain_core.messages import HumanMessage
from workflow import create_workflow


class ScrappyOrchestrator:
    # Compile the LangGraph workflow once when the orchestrator is created
    def __init__(self):
        self.graph = create_workflow()

    def investigate(self, question:str)->dict:       
        #Initialize the state
        initial_state = {
            "question":question,
            "messages":[HumanMessage(content=question)],
            "generated_queries":[],
            "current_agent":"intent",
            "retry_count":0,
            "validation_errors":[]
        }

        #Run the graph
        final_state = self.graph.invoke(initial_state)

        return final_state


      