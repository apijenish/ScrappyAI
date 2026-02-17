from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from ScrappyAgents import ScrappyInvestigationAgents
from StateDefinition import InvestigationState


class ScrappyOrchestrator:
    """This is the main orchestrator"""
    
    def __init__(self):
        self.graph = ScrappyInvestigationWorkflow.init_agents()

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



class ScrappyInvestigationWorkflow:


    @staticmethod
    def init_agents():
        agents = ScrappyInvestigationAgents()

        workflow = StateGraph(InvestigationState)

        workflow.add_node("intent", agents.intent_agent)
        workflow.add_node("planner", agents.planner_agent)
        workflow.add_node("query_builder", agents.query_builder_agent)
        workflow.add_node("data retrevial",agents.data_retrieval_agent)
        workflow.add_node("explainer", agents.summary_agent)

        workflow.set_entry_point("intent")

        workflow.add_edge("intent", "planner")
        workflow.add_edge("planner", "query_builder")
        workflow.add_edge("query_builder", "explainer")
        workflow.add_edge("explainer", END)

        return workflow.compile()

      