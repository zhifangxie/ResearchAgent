from src.utils.states import InterviewState
from src.utils.nodes import generate_question, search_and_answer, write_section
from src.utils.edges import route_question
from langgraph.graph import StateGraph, START, END

# Add nodes and edges 
interview_builder = StateGraph(InterviewState)
interview_builder.add_node("ask_question", generate_question)
interview_builder.add_node("search_and_answer", search_and_answer)
interview_builder.add_node("write_section", write_section)

# Flow
interview_builder.add_edge(START, "ask_question")
interview_builder.add_conditional_edges("ask_question", route_question, ["search_and_answer", "write_section"])
interview_builder.add_edge("search_and_answer", "ask_question")
interview_builder.add_edge("write_section", END)

question_answer_graph = interview_builder.compile()