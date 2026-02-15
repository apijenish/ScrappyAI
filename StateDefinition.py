from typing_extensions import TypedDict, NotRequired, Annotated
import operator

class InvestigationState(TypedDict):

    """
    State that flows through the entire agent workflow
    Each agent can read from and write to this state
    """

    #User Input
    question: str

    #Intent Agent output
    question_type: NotRequired[str]
    metrics_mentioned: NotRequired[list[str]]
    dimensions: NotRequired[list[str]]
    
    #Planner Agent output
    investigation_steps: NotRequired[list[dict]]
    focus_areas: NotRequired[list[str]]
    
    # Query Builder outputs
    generated_queries: NotRequired[Annotated[list[dict], operator.add]]  # Accumulate queries
    sql_query:NotRequired[list[str]]
    
    # Explainer outputs
    summary: NotRequired[str]
    next_steps: NotRequired[list[str]]
    
    # Metadata
    messages: NotRequired[Annotated[list, operator.add]]  # Conversation history
    current_agent: NotRequired[str]


