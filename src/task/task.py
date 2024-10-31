import json
from fastapi import HTTPException
from database import get_db_session_celery
from src.agent.controllers import AgentController
from src.config import Config
from src.crew.agents import CustomAgent
from src.crew.prompts import get_desc_prompt
from src.task.controllers import TaskController, TaskCompletedController
from src.tool.controllers import ToolsController
from src.utils.pinecone import PineConeConfig
from src.utils.utils import get_uuid
from src.crew.tools import ToolKit
import pandas as pd
from src.celery import celery_app
from asgiref.sync import async_to_sync


# @celery_app.task()
def task_creation_celery(
    agent_id: str,
    task_id: str,
    base_url: str,
    include_previous_output: bool,
    previous_output: list[str],
    is_csv: bool,
    from_user: int,
    to_user: int,
    from_user_role_id: int,
) -> str:
    with get_db_session_celery() as db:
        agent = AgentController.get_agents_by_id_ctrl(db, agent_id)
        task = TaskController.get_tasks_by_id_ctrl(db, task_id)
        doc_context = []
        previous_output = []

        if agent.own_data:
            if not agent.vector_id:
                raise HTTPException(
                    detail="Vector of own file not found.", status_code=404
                )

            namespace = agent.vector_id

            ps = PineConeConfig(
                api_key=Config.PINECONE_API_KEY,
                index_name=Config.PINECONE_INDEX_NAME,
                namespace=namespace,
            )

            doc_context = ps.similarity_search(
                query=task.agent_instruction, score_threshold=0.2
            )

        if include_previous_output:
            for task_id in previous_output:
                output = TaskController.get_tasks_by_id_ctrl(db, task_id)
                previous_output.append(
                    {
                        "description": output.agent_instruction,
                        "expected_output": output.agent_output,
                        "response": TaskCompletedController.get_completed_task_details_by_id(
                            db=db, task_id=task_id
                        ).output,
                    }
                )

        # Tools
        tool_ids = json.loads(task.agent_tool)
        tools = []
        webhook_urls = []
        existing_tools = [tool_name.name for tool_name in ToolKit]

        for id in tool_ids:
            tool = ToolsController.get_tool_by_uuid(db=db, id=id)
            tool_name = tool.tool_name
            if tool.webhook_url:
                webhook_url = f"WEBHOOK URL OF {tool_name}: " + tool.webhook_url
                webhook_urls.append(webhook_url)

            if tool_name not in existing_tools:
                raise HTTPException(
                    detail=f"Tool {tool_name} not found", status_code=404
                )
            if id:
                tools.append(eval(f"ToolKit.{tool_name}.value[0]"))

        prompt = get_desc_prompt(
            agent=agent,
            agent_instruction=task.agent_instruction,
            previous_output=previous_output,
            doc_context=doc_context,
            webhook_urls=webhook_urls,
        )

        # url = "https://hooks.zapier.com/hooks/catch/20437545/291m0av/"
        # kwargs = {
        #     "payload": json.dumps(
        #         {
        #             "to": "harsh281.rejoice@gmail.com",
        #             "from_email": "pranav258.rejoice@gmail.com",
        #             "subject": "This is the subject",
        #             "body_type": "text",
        #             "body": "This is an email body for test msg.",
        #         }
        #     ),
        # }
        # kwargs.update({"url" : url})
        # prompt = get_task_prompt()

        init_task = CustomAgent(
            agent=agent,
            agent_instruction=prompt,
            agent_output=task.agent_output,
            tools=tools,
        )

        custom_task_output, comment_task_output = async_to_sync(init_task.main)()

        max_length = max(len(v) for v in custom_task_output.json_dict.values())

        # Handle the edge cases in which if we do get empty column
        for key in custom_task_output.json_dict.keys():
            custom_task_output.json_dict[key] += [None] * (
                max_length - len(custom_task_output.json_dict[key])
            )

        full_file_url = None
        if is_csv:
            file_name = f"{get_uuid()}.csv"
            pd.DataFrame(custom_task_output.json_dict).to_csv(
                "static/" + file_name, index=False
            )
            full_file_url = f"static/{file_name}"

        completed_task = TaskCompletedController.create_completed_task_details(
            db=db,
            task_id=task_id,
            from_user=from_user,
            to_user=to_user,
            from_user_role_id=from_user_role_id,
            output=custom_task_output.raw,
            comment=comment_task_output.raw,
            file_path=full_file_url,
        )
        return completed_task

    # return f"Task completed: {task_id}"


# async def chat_task_creation(
#     websocket: WebSocket,
#     db: Session,
#     collection: Collection,
#     session_id: int,
#     agent_id: str,
#     task_id: str,
#     include_previous_output,
#     previous_output,
#     previous_queries,
#     previous_responses,
# ):
#     agent = await AgentController.get_agents_ctrl(db, agent_id)
#     if not agent:
#         await websocket.send_json({"error": "Agent not found"})
#         return
#     agent = agent[0]
#     task: Task = await TaskController.get_tasks_ctrl(db, task_id)
#     if not task:
#         await websocket.send_json({"error": "Task not found"})
#         return

#     relevant_output = []
#     if agent["is_custom_agent"]:
#         if agent["file_upload"]:
#             namespace = agent["vector_id"]
#             ps = PineConeConfig(
#                 api_key=Config.PINECONE_API_KEY,
#                 index_name=Config.PINECONE_INDEX_NAME,
#                 namespace=namespace,
#             )

#             try:
#                 vector_output = ps.vector_store.similarity_search(
#                     query=task.description, k=3
#                 )
#                 relevant_output = [
#                     str(vector_output[i].page_content)
#                     for i in range(len(vector_output))
#                 ]

#             except Exception as e:
#                 await websocket.send_json(
#                     {"error": "Pinecone search failed", "details": str(e)}
#                 )

#     previous_output = []
#     if include_previous_output:
#         for task_id in previous_output:
#             output = await TaskController.get_tasks_ctrl(db, task_id)
#             previous_output.append(
#                 {
#                     "description": output.description,
#                     "expected_output": output.expected_output,
#                     "response": output.response,
#                 }
#             )
#     prompt = await get_chat_bot_prompt(
#         task.description,
#         previous_queries,
#         previous_responses,
#         relevant_document=relevant_output,
#     )

#     agent_tools = agent["tools"]

#     tools = []
#     for tool in agent_tools:
#         agent_tool = await ToolController.get_tools_ctrl(db, tool)
#         tools.append(mapping[agent_tool[0]["name"]])
#     from crewai_tools import TXTSearchTool, PDFSearchTool, EXASearchTool
#     # tools.append(TXTSearchTool(txt="C:\\Users\\Dreamworld\\Desktop\\colabi\\static\\extended_meta_ads_report.txt"))
#     init_task = CustomAgent(
#         role=agent["role"],
#         backstory=agent["backstory"],
#         goal=agent["goal"],
#         tools=tools,
#         expected_output=task.expected_output,
#         description=prompt,
#         is_chatbot=True,
#     )

#     try:
#         custom_task_output = (
#             await init_task.main()
#         )  # Ensure this is an async operation if needed
#     except Exception as e:
#         await websocket.send_json({"error": "Agent task failed", "details": str(e)})
#         return

#     tasks = await TaskController.update_task_ctrl(
#         db, task_id, custom_task_output.raw, None, None
#     )
#     if tasks:
#         try:
#             collection.update_one(
#                 {"_id": session_id},
#                 {
#                     "$push": {
#                         "chat": {
#                             "chat_id": task.id,
#                             "query": tasks.description,
#                             "response": tasks.response,
#                             "created_at": tasks.created_at,
#                         }
#                     }
#                 },
#             )
#         except Exception as e:
#             await websocket.send_json(
#                 {"error": "Failed to update chat history", "details": str(e)}
#             )
#     if tasks:
#         await websocket.send_json(
#             {
#                 "message": "Task completed",
#                 "data": {
#                     "id": tasks.id,
#                     "description": tasks.description,
#                     "agent_id": tasks.agent_id,
#                     "output": tasks.response,
#                     "comment": tasks.comment,
#                     "attachments": tasks.attachments,
#                     "status": tasks.status,
#                     "created_at": str(tasks.created_at),
#                 },
#                 "error_msg": "",
#                 "error": "",
#             }
#         )
#     else:
#         await websocket.send_json({"error": "Task update failed"})
