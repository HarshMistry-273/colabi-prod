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

import os
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.utilities.zapier import ZapierNLAWrapper

os.environ["ZAPIER_NLA_API_KEY"] = os.environ.get("ZAPIER_NLA_API_KEY", "YOUR_ZAPIER_API_KEY")

zapier = ZapierNLAWrapper()
toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)

from langchain.agents import AgentType
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory

breakpoint()
toolkit.get_tools()