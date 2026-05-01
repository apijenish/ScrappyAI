
# State that flows through the entire agent workflow
# Each agent can read from and write to this state

from typing_extensions import TypedDict, NotRequired, Annotated
import operator

class ScrappyInvestigationState(TypedDict):

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
    generated_queries: NotRequired[list[dict]]  # Accumulate queries

    # Validator output
    retry_count:NotRequired[int]
    validation_errors:NotRequired[list[dict]]

    # Data Retrieval outputs  ← NEW
    query_results: NotRequired[list[dict]]  # [{label, query, columns, rows, error}]
    
    # Explainer outputs
    summary: NotRequired[str]
    next_steps: NotRequired[list[str]]
    
    # Metadata
    messages: NotRequired[Annotated[list, operator.add]]  # Conversation history
    current_agent: NotRequired[str]



