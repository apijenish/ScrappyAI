from state import ScrappyInvestigationState
from agents import ScrappyInvestigationAgent
from langgraph.graph import StateGraph, END

MAX_RETRIES = 2

def should_retry(state: ScrappyInvestigationState) -> str:
    """
    Routing function for the conditional edge after validator.
    Returns 'retry' if there are failed queries and retries remain,
    otherwise returns 'proceed'.
    """
    errors = state.get("validation_errors", [])
    retry_count = state.get("retry_count", 0)

    if errors and retry_count < MAX_RETRIES:
        state["retry_count"] = retry_count + 1
        print(f"[Workflow] Retrying query builder (attempt {state['retry_count']}/{MAX_RETRIES})")
        return "retry"
    
    if errors:
        print(f"[Workflow] Max retries reached. Proceeding with {len(errors)} failed queries.")

    return "proceed"

def create_workflow()->StateGraph:
    agents = ScrappyInvestigationAgent()

    workflow = StateGraph(ScrappyInvestigationState)

    workflow.add_node("intent", agents.intent_agent)
    workflow.add_node("planner", agents.planner_agent)
    workflow.add_node("query_builder", agents.query_builder_agent)
    workflow.add_node("validator", agents.validator_agent)
    workflow.add_node("data_retrieval",agents.data_retrieval_agent)
    workflow.add_node("explainer", agents.summary_agent)

    workflow.set_entry_point("intent")

    workflow.add_edge("intent", "planner")
    workflow.add_edge("planner", "query_builder")
    workflow.add_edge("query_builder", "validator")

    workflow.add_conditional_edges("validator", should_retry,
                                   {
                                       "retry":"query_builder",
                                       "proceed":"data_retrieval"
                                   })

    workflow.add_edge("data_retrieval", "explainer")
    workflow.add_edge("explainer", END)

    return workflow.compile()