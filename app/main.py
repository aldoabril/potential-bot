from langchain_core.messages import HumanMessage
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiplies a and b."""
    return a * b


# Initialize model
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

# Bind tools
tools = [add, multiply]
llm_with_tools = llm.bind_tools(tools)

# Query
query = "What is 3 * 12? Also, what is 11 + 49?"
messages = [HumanMessage(query)]

# Get AI response
ai_msg = llm_with_tools.invoke(messages)
print(ai_msg.tool_calls)

# Append AI message to conversation
messages.append(ai_msg)

for tool_call in ai_msg.tool_calls:
    selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

# Print conversation history
print(messages)
