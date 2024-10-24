# from langchain_community.document_loaders import (
#     PyPDFLoader,
#     TextLoader,
#     CSVLoader,
#     JSONLoader,
# )
# from src.preprocessing import splitter
# breakpoint()
# docs = JSONLoader(
#     {"id": "id", "data": "data", "data_type": "data_type"}
# ).load_and_split(splitter)

from langchain.tools import BaseTool
from typing import Optional, Type
from langchain_openai import ChatOpenAI
import requests
import json

from src.config import Config


class WebhookTool(BaseTool):
    """Tool for making webhook POST requests to a specified endpoint."""

    name = "webhook_tool"
    description = "Use this tool to send data to a webhook endpoint"
    webhook_url: str

    def __init__(self, webhook_url: str):
        """Initialize the webhook tool with the target URL."""
        super().__init__()
        self.webhook_url = webhook_url

    def _run(self, payload: str) -> str:
        """Execute the webhook request with the given payload."""
        try:
            # Convert string payload to JSON if needed
            if isinstance(payload, str):
                try:
                    payload_data = json.loads(payload)
                except json.JSONDecodeError:
                    payload_data = {"message": payload}
            else:
                payload_data = payload

            # Make the POST request
            response = requests.post(
                self.webhook_url,
                json=payload_data,
                headers={"Content-Type": "application/json"},
            )

            # Handle the response
            if response.status_code in [200, 201]:
                return (
                    f"Webhook request successful. Status code: {response.status_code}"
                )
            else:
                return f"Webhook request failed. Status code: {response.status_code}, Response: {response.text}"

        except Exception as e:
            return f"Error sending webhook request: {str(e)}"

    def _arun(self, payload: str) -> str:
        """Async version of the webhook request (placeholder for future implementation)."""
        # For async implementation, you would use aiohttp or httpx here
        raise NotImplementedError("Async version not implemented yet")


# Example usage with LangChain
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI


def setup_webhook_agent(webhook_url: str, openai_api_key: str):
    """Setup an agent with webhook capabilities."""

    # Initialize the webhook tool
    webhook_tool = WebhookTool(webhook_url=webhook_url)

    # Initialize the language model
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

    # Create the agent with the webhook tool
    agent = initialize_agent(
        tools=[webhook_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    return agent


# Example usage with CrewAI
from crewai import Agent, Task, Crew


def setup_webhook_crew(webhook_url: str = None, openai_api_key: str = None):
    """Setup a CrewAI agent with webhook capabilities."""

    # Initialize the webhook tool
    webhook_tool = WebhookTool(webhook_url=webhook_url)

    # Create an agent with the webhook tool
    agent = Agent(
        role="Webhook Manager",
        goal="Send data to webhook endpoints accurately",
        backstory="I am responsible for managing webhook communications",
        tools=[webhook_tool],
        llm=ChatOpenAI(
            model=Config.MODEL_NAME,
            api_key=Config.OPENAI_API_KEY,
        ),
    )

    return agent


agent = setup_webhook_agent("")
