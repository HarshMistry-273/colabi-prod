import json
from crewai import Agent, Process, Task, Crew
from src.agent.models import Agent as AgentModel
from langchain.tools import Tool
from src.config import Config
from langchain_openai import ChatOpenAI
from src.crew.prompts import get_comment_task_prompt, get_task_prompt
from src.crew.serializers import OutputFile
from crewai.tasks.task_output import TaskOutput
from src.crew.tools import ToolKit
from src.task.models import Tasks as TasksModel


class CustomAgent:
    """
    A custom agent class that creates and manages a crew of agents to perform tasks.

    This class initializes agents, creates tasks, and manages a crew to execute those tasks.
    It uses OpenAI's ChatGPT model for natural language processing.

    Attributes:
        model (ChatOpenAI): The language model used by the agents.
        role (str): The role of the primary agent.
        goal (str): The goal of the primary agent.
        backstory (str): The backstory of the primary agent.
        tools (list[Tool]): A list of tools available to the primary agent.
        agents (list[Agent]): A list of agents (primary and comment agents).
        expected_output (str): The expected output format for the primary task.
        description (str): The description of the primary task.
        tasks (list[Task]): A list of tasks to be performed.
        crew (Crew): A crew object managing the agents and tasks.
    """

    def __init__(
        self,
        agent: AgentModel,
        agent_instruction: str,
        agent_output: str,
        model: str = Config.MODEL_NAME,
    ):
        self.model = ChatOpenAI(
            model=model,
            api_key=Config.OPENAI_API_KEY,
        )
        self.agent = agent
        self.custom_agent = self._create_agent()

        self.agent_instruction = agent_instruction
        self.agent_output = agent_output
        self.tasks = self._create_tasks()

        self.crew = self._create_crew()

    def _create_agent(self) -> list[Agent]:
        agent_list = []
        custome_agent = Agent(
            role=self.agent.description,
            goal=self.agent.key_feature,
            backstory=self.agent.personality,
            llm=self.model,
            tools=[
                eval(f"ToolKit.{tool_name}.value")
                for tool_name in json.loads(self.agent.tools)
            ],
            verbose=False,
        )
        agent_list.append(custome_agent)
        if not self.agent.is_chatbot:
            comment_agent = Agent(
                role="Comment agent",
                goal="Comment on the previous task completed by agents.",
                backstory="You are obeserver of task being completed by Agents and you look for if task is being completed and as expexted",
                llm=self.model,
                verbose=False,
            )
        agent_list.append(comment_agent)

        return agent_list

    def _create_tasks(self) -> list[Task]:
        tasks = []
        custom_task = Task(
            description=self.agent_instruction,
            expected_output=self.expected_ouput,
            agent=self.custom_agent,
            output_json=OutputFile,
        )
        tasks.append(custom_task)

        if not self.agent.is_chatbot:
            comment_prompt = get_comment_task_prompt()
            comment_task = Task(
                description=comment_prompt,
                expected_output="Task reviewed: ",
                agent=self.custom_agent[1],
            )
            tasks.append(comment_task)

        return tasks

    def _create_crew(self) -> Crew:
        crew = Crew(
            agents=self.custom_agent,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            output_log_file="crew.log",
        )
        return crew

    async def main(self) -> tuple[TaskOutput]:
        if self.agent.is_chatbot:
            response = await self.crew.kickoff_async(
                inputs={"description": self.agent_instruction}
            )
            return response

        response = await self.crew.kickoff_async(
            inputs={"description": self.agent_instruction}
        )
        output = response.tasks_output

        custom_task_output = output[0]
        comment_task_output = output[1]

        return custom_task_output, comment_task_output
