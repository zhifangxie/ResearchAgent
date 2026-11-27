from src.utils.states import GenerateAnalystsState, InterviewState, ResearchGraphState
from langgraph.graph import END
from dotenv import load_dotenv
from typing import Literal
from langchain.messages import HumanMessage
from langgraph.types import Send

load_dotenv()

# edges 
def should_continue(state: GenerateAnalystsState) -> Literal["create_analysts", "dummy"]:
    """ Return the next node to execute """

    # Check if human feedback
    human_analyst_feedback=state.get('human_analyst_feedback', None)

    if human_analyst_feedback:
        return "create_analysts"
    
    # Otherwise end
    return "dummy"

def route_question(state: InterviewState):
    """ After a question: search and answer, or end if the analyst is wrapping up
    (generate_question also sets end_interview once max_num_turns answers are reached) """
    if state.get("end_interview"):
        return "write_section"
    return "search_and_answer"

def initiate_all_interviews(state: ResearchGraphState):
    """ This is the "map" step where we run each interview sub-graph using Send API """    

    # Check if human feedback
    human_analyst_feedback=state.get('human_analyst_feedback')
    if human_analyst_feedback:
        # Return to create_analysts
        return "create_analysts"

    # Otherwise kick off interviews in parallel via Send() API
    else:
        topic = state["topic"]
        # conduct_interview: next node
        # {}: input received by the next node
        # map-reduce: run the same node multiple times in parallel, send input to each 
        # results are merged back together
        return [Send("conduct_interview", {"analyst": analyst,
                                           "messages": [HumanMessage(
                                               content=f"Write an article on {topic}"
                                           )
                                                       ]}) for analyst in state["analysts"]]
