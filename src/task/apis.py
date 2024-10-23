# import logging.config
# import os
# from fastapi import APIRouter, HTTPException, Request, Depends
# from sqlalchemy.orm import Session
# from fastapi.responses import FileResponse, JSONResponse
# from database import get_db_session
# from src.task.task import task_creation_celery
# from src.task.serializers import CreateTaskSchema
# from src.task.controllers import TaskController
# import logging
# from src.utils.logger import logger_set

# router = APIRouter()

# logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
# logger = logging.getLogger(__name__)

# @router.get("")
# async def get_task(id: str, db: Session = Depends(get_db_session)):
#     """
#     Retrieve a task by its ID and return its details as a JSON response.

#     This function performs the following steps:
#     1. Calls the get_tasks_ctrl function with the provided ID to retrieve the task.
#     2. Constructs a JSON response containing the task's details.

#     Args:
#         id (str): The unique identifier of the task to retrieve.

#     Returns:
#         JSONResponse: A response containing the task details, including:
#             - id: The task's unique identifier.
#             - description: The task's description.
#             - agent_id: The ID of the agent associated with the task.
#             - output: The task's response or output.
#             - comment: Any comments associated with the task.
#             - status: The current status of the task.
#             - created_at: The timestamp when the task was created (as a string).
#     """
#     try:
#         logger.info("Task get endpoint")
#         tasks = TaskController.get_tasks_ctrl(db, id)

#         logger_set.info("Task listed successfully.")
#         return JSONResponse(
#             status_code=200,
#             content={
#                 "message": "Task fetched",
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
#             },
#         )
#     except Exception as e:
#         logger_set.error(f"Error fetching tasks : {e}")
#         return JSONResponse(
#             status_code=500,
#             content={"data": {}, "error_msg": "Invalid request", "error": str(e)},
#         )