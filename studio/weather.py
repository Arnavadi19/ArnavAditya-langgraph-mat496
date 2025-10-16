from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

def get_weather(location: str) -> str:
    """Get current weather for a location.

    Args:
        location: The city or location to get weather for
    """
    # Simulate weather API response
    weather_data = {
        "new york": "Sunny, 72°F",
        "london": "Rainy, 60°F", 
        "tokyo": "Cloudy, 68°F",
        "paris": "Sunny, 75°F",
        "sydney": "Windy, 65°F"
    }
    return weather_data.get(location.lower(), f"Weather data not available for {location}. Sunny, 70°F")

def recommend_clothing(weather: str, temperature: str) -> str:
    """Recommend clothing based on weather conditions.

    Args:
        weather: Weather condition (e.g., sunny, rainy, cloudy)
        temperature: Temperature description (e.g., hot, cold, mild)
    """
    recommendations = {
        "sunny": "Light clothing, sunglasses, and sunscreen",
        "rainy": "Waterproof jacket, umbrella, and boots", 
        "cloudy": "Light jacket or sweater",
        "windy": "Windbreaker jacket and secure hat",
        "snowy": "Heavy coat, gloves, and warm boots"
    }
    
    weather_lower = weather.lower()
    for condition in recommendations:
        if condition in weather_lower:
            return f"Recommended clothing: {recommendations[condition]}"
    
    return "Recommended clothing: Comfortable casual wear"

tools = [get_weather, recommend_clothing]

# Define LLM with bound tools
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

# System message
sys_msg = SystemMessage(content="You are a helpful weather assistant. You can check weather conditions and provide clothing recommendations. Always be friendly and helpful!")

# Node
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message from assistant is a tool call -> route to tools
    # If not a tool call -> route to END
    tools_condition,
)
builder.add_edge("tools", "assistant")

# Compile graph
graph = builder.compile()