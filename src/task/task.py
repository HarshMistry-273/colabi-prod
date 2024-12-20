import json
import pandas as pd
from fastapi import HTTPException
from database import get_db_session_celery
from src.agent.controllers import AgentController
from src.config import Config
from src.crew.agents import CustomAgent
from src.crew.prompts import get_desc_prompt
from src.task.controllers import TaskController, TaskCompletedController, TaskUtils
from src.tool.controllers import ToolsController
from src.utils.pinecone import PineConeConfig
from src.utils.utils import get_uuid
from src.celery import celery_app
from asgiref.sync import async_to_sync
from src.utils.logger import logger_set


@celery_app.task()
def task_creation_celery(
    agent_id: int,
    task_id: int,
    base_url: str,
    include_previous_output: bool,
    previous_outputs: list[int],
    is_csv: bool,
    completed_task_id: int,
) -> str:
    try:
        logger_set.info(f"Celery task started. Task Id: {task_id}")
        with get_db_session_celery() as db:
            agent = AgentController.get_agents_by_id_ctrl(db, agent_id)
            task = TaskController.get_tasks_by_id_ctrl(db, task_id)
            task_params = {}
            params = ""

            try:
                if task.agent_parameter:
                    task_params = json.loads(task.agent_parameter)
                    keys = list(task_params.keys())

                    for i in keys:
                        var = f"{i} = {{{i}}},"
                        params = params + var
            except Exception as e:
                pass
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
                previous_output = TaskUtils.get_previous_outputs(
                    db=db, previous_outputs=previous_outputs
                )

            # Tools
            tool_ids = json.loads(task.agent_tool)
            tools = ToolsController.get_tools_list_as_tool_instance(
                db=db, tool_ids=tool_ids
            )

            prompt = get_desc_prompt(
                agent=agent,
                agent_instruction=task.agent_instruction,
                previous_output=previous_output,
                doc_context=doc_context,
                params=params,
            )

            init_task = CustomAgent(
                agent=agent,
                agent_instruction=prompt,
                agent_output=task.agent_output,
                tools=tools,
                params=task_params,
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

            TaskCompletedController.update_completed_task_details(
                db=db,
                completed_task_id=completed_task_id,
                output=custom_task_output.raw,
                comment=comment_task_output.raw,
                file_path=full_file_url,
                status=1,
            )

        return f"Task completed: {task_id}, Completed Task Id: {completed_task_id}"
    except Exception as e:
        logger_set.info(f"Celery task failed. Task Id: {task_id}. Error: {str(e)}")

        TaskCompletedController.update_completed_task_details(
            db=db,
            completed_task_id=completed_task_id,
            status=2,
        )
        return f"Task failed: {task_id}, Completed Task Id: {completed_task_id}"


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
