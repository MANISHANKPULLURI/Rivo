from langgraph.graph import StateGraph, END
from backend.agents.state import AgentState
from backend.agents.nodes import researcher_node, critic_node

# 1. Initialize the Graph with our specific 'Filing Cabinet' (State)
workflow = StateGraph(AgentState)

# 2. Add our 'Brain Cells' (Nodes)
# We give them names so we can refer to them in the map
workflow.add_node("researcher", researcher_node)
workflow.add_node("critic", critic_node)

# 3. Define the Connections (Edges)
# The flow: START -> Researcher -> Critic -> END
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "critic")
workflow.add_edge("critic", END)

# 4. Compile the Graph
# This turns our 'Map' into a 'Program' we can run
app = workflow.compile()