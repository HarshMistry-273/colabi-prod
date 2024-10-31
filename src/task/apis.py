import logging.config
from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import get_db_session
from src.task.task import task_creation_celery
from src.task.serializers import CreateTaskSchema
from src.task.controllers import TaskController
import logging
from src.utils.logger import logger_set

router = APIRouter()

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


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


@router.post("")
def create_task(
    tasks: CreateTaskSchema, request: Request, db: Session = Depends(get_db_session)
):
    """
    Create a new task, process it using a custom agent, and return the results.

    This function performs the following steps:
    1. Creates a new task based on the provided CreateTaskSchema.
    2. Retrieves the associated agent and its tools.
    3. Initializes a CustomAgent with the agent's details and task information.
    4. Executes the task using the CustomAgent.
    5. Processes the output, including CSV file creation if required.
    6. Updates the task with the results.
    7. Returns a JSON response with the task details and outputs.

    Args:
        tasks (CreateTaskSchema): The schema containing task creation details.
        request (Request): The incoming request object.

    Returns:
        JSONResponse: A response containing the task details, outputs, and any attachments.

    Raises:
        Potential exceptions from called functions are not explicitly handled in this function.
    """
    logger.info("Task create endpoint")

    try:
        get_task = TaskController.get_tasks_by_id_ctrl(db, tasks.task_id)

        res = task_creation_celery(
            agent_id=get_task.assign_task_agent_id,
            task_id=get_task.id,
            base_url=str(request.base_url),
            include_previous_output=tasks.include_previous_output,
            previous_output=tasks.previous_output,
            is_csv=tasks.is_csv,
            from_user=tasks.from_user,
            to_user=tasks.to_user,
            from_user_role_id=tasks.from_user_role_id,
        )
        logger_set.info(
            f"Task created successfully, Task id : {get_task.id}, Agent id : {get_task.assign_task_agent_id}"
        )
        return JSONResponse(
            status_code=200,
            content={
                "message": "Task started",
                "data": {"task_id": get_task.id},
                "status": True,
                "error": "",
            },
        )
    except HTTPException as e:
        logger_set.error(f"Could not update agent : {str(e)}")
        return JSONResponse(
            status_code=e.status_code,
            content={
                "message": str(e.detail),
                "data": {},
                "status": False,
                "error": str(e.detail),
            },
        )
    except Exception as e:
        logger_set.info(f"Error creating task : {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "data": {},
                "status": False,
                "error": str(e),
            },
        )
