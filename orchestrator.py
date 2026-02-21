from langchain_core.messages import HumanMessage
from workflow import create_workflow


class ScrappyOrchestrator:
    
    def __init__(self):
        self.graph = create_workflow()

    def investigate(self, question:str)->dict:
        
        #Initialize the state
        initial_state = {
            "question":question,
            "messages":[HumanMessage(content=question)],
            "generated_queries":[],
            "current_agent":"intent"
        }

        #Run the graph
        final_state = self.graph.invoke(initial_state)

        return final_state


      