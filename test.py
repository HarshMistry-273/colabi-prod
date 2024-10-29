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


# class WebhookTool(BaseTool):
#     """Tool for making webhook POST requests to a specified endpoint."""

#     name: str= "webhook_tool"
#     description: str = "Use this tool to send data to a webhook endpoint"
#     webhook_url: str

#     def __init__(self, webhook_url: str):
#         """Initialize the webhook tool with the target URL."""
#         # super().__init__()
#         self.webhook_url = webhook_url

#     def _run(self, payload: str) -> str:
#         """Execute the webhook request with the given payload."""
#         try:
#             # Convert string payload to JSON if needed
#             if isinstance(payload, str):
#                 try:
#                     payload_data = json.loads(payload)
#                 except json.JSONDecodeError:
#                     payload_data = {"message": payload}
#             else:
#                 payload_data = payload

#             # Make the POST request
#             response = requests.get(
#                 self.webhook_url,
#                 # json=payload_data,
#                 headers={"Content-Type": "application/json"},
#             )

#             # Handle the response
#             if response.status_code in [200, 201]:
#                 return (
#                     f"Webhook request successful. Status code: {response.content}"
#                 )
#             else:
#                 return f"Webhook request failed. Status code: {response.status_code}, Response: {response.text}"

#         except Exception as e:
#             return f"Error sending webhook request: {str(e)}"

#     def _arun(self, payload: str) -> str:
#         """Async version of the webhook request (placeholder for future implementation)."""
#         # For async implementation, you would use aiohttp or httpx here
#         raise NotImplementedError("Async version not implemented yet")


# # Example usage with LangChain
# from langchain.agents import initialize_agent, AgentType
# from langchain_openai import ChatOpenAI


# def setup_webhook_agent(webhook_url: str, openai_api_key: str):
#     """Setup an agent with webhook capabilities."""

#     # Initialize the webhook tool
#     webhook_tool = WebhookTool(webhook_url=webhook_url)

#     # Initialize the language model
#     llm = ChatOpenAI(openai_api_key=openai_api_key)

#     # Create the agent with the webhook tool
#     agent = initialize_agent(
#         tools=[webhook_tool],
#         llm=llm,
#         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#         verbose=True,
#     )

#     return agent


# Example usage with CrewAI
import json
from crewai import Agent, Task, Crew
from crewai_tools import tool
import requests
from langchain_openai import ChatOpenAI
import requests
from src.config import Config


@tool("Webhook Trigger")
def webhook_tool(url: str, payload: dict) -> str:
    """Tool to send a POST request to a webhook URL with a specified payload."""
    print("Payload...",payload)
    headers = {"Content-Type": "application/json"}
    res = requests.request("POST", url, headers=headers, json=payload)
    print(res.content)
    print(res.json())
    return res.json()  # Returns response as JSON


# Define the Agent
agent = Agent(
    role="Webhook Data Poster",
    goal="You are required to post data to the specified webhook URL accurately and without making any modifications to the payload. It is essential to ensure the payload remains unchanged during the transmission process. Simply deliver the provided data directly to the URL endpoint, maintaining its original structure and content to facilitate seamless processing on the receiving end.",
    backstory="Posts structured data to specified webhook URLs while preserving the exact payload format. You should ensure data integrity during transmission and handle responses effectively, adapting as needed to confirm successful delivery.",
    tools=[webhook_tool],
    llm=ChatOpenAI(
        model=Config.MODEL_NAME,
        api_key=Config.OPENAI_API_KEY,
    ),
    verbose=True,
)

# Define the Task for the Agent to hit the webhook URL
task = Task(
    description="Post structured data to the webhook URL {url}, PAYLOAD: {payload}",
    expected_output="Webhook Response: ",
    agent=agent,
    name="Post to Webhook",
)

# Example usage
webhook_url = "https://hooks.zapier.com/hooks/catch/20437545/291m0av/"  # Replace with your actual webhook URL
payload = {
        "to": "harsh281.rejoice@gmail.com",
        "from_email": "pranav258.rejoice@gmail.com",
        "subject": "This is the subject",
        "body_type": "text",
        "body": "This is an email body for test msg."
    }


# # Invoke the tool via agent and task
# response = webhook_tool(webhook_url, payload_data)  
# print("Response from webhook:", response)  

crew_a = Crew(         
    agent=[agent],      
    tasks=[task],      
    verbose=True,     
)

res = crew_a.kickoff({"url": webhook_url, "payload": payload})

print(res.raw)
