from state import ScrappyInvestigationState
from agents import ScrappyInvestigationAgent
from langgraph.graph import StateGraph, END

def create_workflow()->StateGraph:
    agents = ScrappyInvestigationAgent()

    workflow = StateGraph(ScrappyInvestigationState)

    workflow.add_node("intent", agents.intent_agent)
    workflow.add_node("planner", agents.planner_agent)
    workflow.add_node("query_builder", agents.query_builder_agent)
    workflow.add_node("data retrevial",agents.data_retrieval_agent)
    workflow.add_node("explainer", agents.summary_agent)

    workflow.set_entry_point("intent")

    workflow.add_edge("intent", "planner")
    workflow.add_edge("planner", "query_builder")
    workflow.add_edge("query_builder", "data retrevial")
    workflow.add_edge("data retrevial", "explainer")
    workflow.add_edge("explainer", END)

    return workflow.compile()