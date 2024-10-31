import requests
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.tools import Tool
from src.config import Config
from enum import Enum
from crewai_tools import tool


class CustomTools:
    """
    A utility class that provides static methods to create custom search tools.

    This class contains methods to create tools for Tavily search and Google Serper API search.
    These tools can be used in conjunction with agent-based systems or other applications
    that require search functionality.
    """

    @staticmethod
    def tavily_search_results(
        tool_name: str = "tavily_search",
        description: str = "search results",
        max_results: int = 10,
        search_depth: str = "advanced",
        include_answer: bool = True,
    ):
        search = TavilySearchResults(
            max_results=max_results,
            search_depth=search_depth,
            include_answer=include_answer,
        )
        tool = Tool(
            name=tool_name,
            func=lambda query: search.invoke(query),
            description=description,
        )

        return tool
    
    @staticmethod
    def google_serper_api_wrapper(
        tool_name: str = "google_serper_search",
        description: str = "search results",
        serper_api_key: str = None,
    ):
        search = GoogleSerperAPIWrapper(serper_api_key=serper_api_key)

        tool = Tool(
            name=tool_name,
            func=lambda query: search.results(query),
            description=description,
        )

        return tool

    @tool("Webhook Trigger")
    @staticmethod
    def send_email(url: str, payload: dict) -> str:
        """Tool to send a POST request to a webhook URL with a specified payload."""
        headers = {"Content-Type": "application/json"}
        res = requests.request("POST", url, headers=headers, json=payload)
        return res.json()


class ToolKit(Enum):
    TAVILY_SEARCH = (CustomTools.tavily_search_results(),)
    GOOGLE_SERPER_SEARCH = (CustomTools.google_serper_api_wrapper(),)
    ZAPIER_SENT_GMAIL = (CustomTools.send_email,)


# [tool_name.name for tool_name in ToolKit]
# eval(f"ToolKit.{value}.value")
