import json
import requests
from enum import Enum
from crewai_tools import (
    tool,
    DallETool,
    ScrapeWebsiteTool,
    YoutubeChannelSearchTool,
    YoutubeVideoSearchTool,
)
from langchain.tools import Tool
from langchain_community.tools import (
    TavilySearchResults,
    google_trends,
    WikipediaQueryRun,
    YouSearchTool,
)
from langchain_community.utilities import (
    GoogleSerperAPIWrapper,
    google_trends as google_trends_weapper,
    WikipediaAPIWrapper,
)
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from crewai import Crew, Task, Agent
from src.config import Config


class CustomTools:
    """
    A utility class that provides static methods to create custom search tools.

    This class contains methods to create tools for Tavily search and Google Serper API search.
    These tools can be used in conjunction with agent-based systems or other applications
    that require search functionality.
    """

    @staticmethod
    def dalle_tool():
        tool = DallETool(
            model="dall-e-3",
            size="1024x1024",
            quality="standard",
        )

        return tool

    @staticmethod
    def scrape_website():
        tool = ScrapeWebsiteTool()
        return tool

    @staticmethod
    def youtube_channel_search():
        tool = YoutubeChannelSearchTool()
        return tool

    @staticmethod
    def youtube_video_search():
        tool = YoutubeVideoSearchTool()
        return tool

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
    def google_serper_api(
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

    @staticmethod
    def google_trends_api(
        tool_name: str = "google_trends",
        description: str = "search trends",
        serpapi_api_key: str = None,
    ):
        google_trend_tool = google_trends.GoogleTrendsQueryRun(
            api_wrapper=google_trends_weapper.GoogleTrendsAPIWrapper()
        )
        tool = Tool(
            name=tool_name,
            func=lambda query: google_trend_tool.run(query),
            description=description,
        )

        return tool

    @staticmethod
    def open_weather_map(
        tool_name: str = "open_weather_map",
        description: str = "find the wether conditions",
    ):
        open_weather_api = OpenWeatherMapAPIWrapper()
        tool = Tool(
            name=tool_name,
            func=lambda query: open_weather_api.run(query),
            description=description,
        )
        return tool

    @staticmethod
    def wikipedia(
        tool_name: str = "wikipedia",
        description: str = "Wikipedia is a multilingual free online encyclopedia written and maintained by a community of volunteers, known as Wikipedians",
    ):
        wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

        tool = Tool(
            name=tool_name,
            func=lambda query: wikipedia_tool.run(query),
            description=description,
        )

        return tool

    # @staticmethod
    # def youtube(
    #     tool_name: str = "youtube",
    #     description: str = "Wikipedia is a multilingual free online encyclopedia written and maintained by a community of volunteers, known as Wikipedians",
    # ):
    #     youtube_search_tool = YouSearchTool()

    #     tool = Tool(
    #         name=tool_name,
    #         func=lambda query: youtube_search_tool.run(query),
    #         description=description,
    #     )

    #     return tool

    @tool("ExposeAction")
    @staticmethod
    def exposed_action(api_key: str) -> dict:
        """Fetch the valid action id for the given instruction

        Args:
            api_key (str): Zapier actions api key

        Returns:
            dict: JSON containing the valid action id of the action
        """

        url = Config.EXPOSED_ACTION_URL

        payload = {}

        headers = {
            "accept": "application/json",
            "x-api-key": api_key,
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()

    @tool("ZapierTools")
    @staticmethod
    def zapier_nla_tool(api_key: str, instructions: str):
        """Perform actions based on the action id provided using Zapier's Natural Language Analytics

        Args:
            api_key (str): Zapier actions api key
            instructions (str): Description of the task
            id (str): Zapier action id

        Returns:
            dict: JSON response of the task performed
        """
        action_id_agent = Agent(
            name="Zapier Action ID Fetcher",
            role="Identifier retriever for Zapier actions",
            goal="Retrieve the correct action ID from Zapier's exposed action route based on user-provided action instructions, enabling accurate execution of intended workflows.",
            backstory="Retrieve the correct action ID from Zapier's exposed action route based on user-provided action instructions, enabling accurate execution of intended workflows.",
            tools=[CustomTools.exposed_action],
        )
        task_one = Task(
            name="ID Fetcher Task",
            description=(
                "If the specified action is not found in the provided JSON, respond with 'None'. "
                "Your task is to retrieve the valid action ID from the JSON based on the given user instruction. "
                "Use only the provided data for action retrieval: api_key = {api_key}, instructions = {instructions}. "
                "Do not alter or use any additional data beyond this."
            ),
            agent=action_id_agent,
            expected_output="Only provide the action ID. Do not include any additional text or context in your response.",
        )
        crew = Crew(agents=[action_id_agent], tasks=[task_one], verbose=True)
        crew_output = crew.kickoff({"api_key": api_key, "instructions": instructions})
        id = crew_output.raw

        if id.lower() == "none":
            return {"response": "No action found please active app."}
        url = f"https://actions.zapier.com/api/v1/exposed/{id}/execute/"

        headers = {
            "accept": "application/json",
            "x-api-key": api_key,
            "User-Agent": "PostmanRuntime/7.42.0",
            "Content-Type": "application/json",
        }

        payload = json.dumps(
            {"instructions": instructions, "preview_only": False, "additionalProp1": {}}
        )

        response = requests.request("POST", url, headers=headers, data=payload)
        print("Response...", response.text)

        return response.json()


class ToolKit(Enum):
    # YOUTUBE_SEARCH = (CustomTools.youtube(),)
    YOUTUBE_VIDEO_SEARCH = (CustomTools.youtube_video_search(),)
    YOUTUBE_CHANNEL_SEARCH = (CustomTools.youtube_channel_search(),)
    DALLE_TOOL = (CustomTools.dalle_tool(),)
    SCRAPE_WEBSITE = (CustomTools.scrape_website(),)
    TAVILY_SEARCH = (CustomTools.tavily_search_results(),)
    GOOGLE_SERPER_SEARCH = (CustomTools.google_serper_api(),)
    GOOGLE_TRENDS = (CustomTools.google_trends_api(),)
    OPEN_WEATHER_MAP = (CustomTools.open_weather_map(),)
    ZAPIER_NLA = (CustomTools.zapier_nla_tool,)
    WIKIPEDIA = (CustomTools.wikipedia(),)
