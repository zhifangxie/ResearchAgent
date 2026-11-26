from src.utils.states import GenerateAnalystsState
from src.utils.nodes import create_analysts, human_feedback, dummy
from src.utils.edges import should_continue
from langgraph.graph import START, END, StateGraph


# building our graph
builder = StateGraph(GenerateAnalystsState)

builder.add_node("create_analysts", create_analysts)
builder.add_node("human_feedback", human_feedback)
builder.add_node("dummy", dummy)

builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "human_feedback")
builder.add_conditional_edges("human_feedback", should_continue)
builder.add_edge("dummy", END)


# interrupt already exists in human_feedback node
graph = builder.compile()
# interrupt_before pauses the graph before the human_feedback node.
# graph = builder.compile(interrupt_before=['human_feedback'])
