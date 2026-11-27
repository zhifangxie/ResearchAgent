from typing_extensions import NotRequired, TypedDict
from typing import List, Optional
from src.utils.objects import Analyst
from langgraph.graph import MessagesState
from typing_extensions import Annotated
import operator

class GenerateAnalystsState(TypedDict):
    topic: str # Research topic
    max_analysts: int # Number of analysts
    human_analyst_feedback: NotRequired[Optional[str]] # Human feedback, can be missing (NotRequired) or None (Optional)
    analysts: NotRequired[List[Analyst]] # Analyst asking questions


# add_messages is for conversation history.
# operator.add is for accumulating other data, such as your context and sections.
class InterviewState(MessagesState):
    # MessagesState brings in: messages: Annotated[list[AnyMessage], add_messages]
    max_num_turns: int # Number turns of conversation
    context_history: Annotated[list, operator.add] # All source docs retrieved across the interview; used for section writing
    analyst: Analyst # Analyst asking questions
    sections: list # Final key we duplicate in outer state for Send() API; for downstream section writing
    end_interview: NotRequired[bool] # Set by generate_question when the analyst is done


# What the interview sub-graph returns to the main graph. Without this, every parallel interview
# would also write back shared keys such as max_num_turns and raise InvalidUpdateError
class InterviewOutputState(TypedDict):
    sections: list


# main graph has all state components from GenerateAnalytsState
class ResearchGraphState(TypedDict):
    topic: str # Research topic
    max_analysts: int # Number of analysts
    max_num_turns: int # Number of turns per interview
    human_analyst_feedback: NotRequired[Optional[str]] # Human feedback
    analysts: List[Analyst] # Analyst asking questions
    # one section per each analyst; different sections are merged here (reduce)
    sections: Annotated[list, operator.add] # Send() API key
    introduction: str # Introduction for the final report
    content: str # Content for the final report
    conclusion: str # Conclusion for the final report
    final_report: str # Final report