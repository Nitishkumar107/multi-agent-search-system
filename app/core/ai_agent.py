from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import AIMessage
from langgraph.prebuilt import create_react_agent
from app.config.settings import settings


def get_response_from_ai_agent(llm_id, query, allow_web_search, system_prompt):
    # OpenRouter is OpenAI-compatible — just point to their base URL
    llm = ChatOpenAI(
        model=llm_id,
        base_url="https://openrouter.ai/api/v1",
        api_key=settings.openrouter_api_key,
    )

    tools = [TavilySearchResults(max_results=3)] if allow_web_search else []

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt
    )

    state = {"messages": query}

    response = agent.invoke(state)

    messages = response.get("messages")

    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]

    return ai_messages[-1]
