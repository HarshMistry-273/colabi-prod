from fastapi import HTTPException
from src.task.models import Tasks, CompletedTaskDetails
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from crewai import Agent


class TaskController:
    # @staticmethod
    # async def create_tasks_ctrl(db: Session, task):
    #     try:
    #         new_task = Task(
    #             description=task.description,
    #             agent_id=task.agent_id,
    #             expected_output=task.expected_output,
    #         )
    #         db.add(new_task)
    #         db.commit()
    #         db.refresh(new_task)
    #         return new_task
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))

    # @staticmethod
    # async def async_create_tasks_ctrl(db: AsyncSession, task):
    # try:
    #     new_task = Task(
    #         description=task.description,
    #         agent_id=task.agent_id,
    #         expected_output=task.expected_output,
    #     )
    #     db.add(new_task)
    #     await db.commit()
    #     await db.refresh(new_task)
    #     return new_task
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_tasks_by_id_ctrl(db: Session, id: int) -> Tasks:
        task = db.query(Tasks).filter(Tasks.id == id).first()
        return task

    # @staticmethod
    # async def async_get_tasks_ctrl(db: AsyncSession, id):
    #     try:
    #         if id:
    #             task = await db.query(Tasks).filter(Tasks.id == id).first()
    #         else:
    #             task = await db.query(Tasks).all()
    #         return task
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=str(e))

    # @staticmethod
    # async def update_task_ctrl(db: Session, id, res, comment, full_file_url):
    #     try:
    #         # def update_task(db, id, res, comment, full_file_url):
    #         task = get_tasks_by_id_ctrl(db, )

    #         if not task:
    #             return {"error": "Task not found"}

    #         task.response = res
    #         task.comment = comment
    #         task.attachments = full_file_url
    #         task.status = "completed"

    #         db.commit()
    #         db.refresh(task)
    #         # Retrieve the updated task
    #         # updated_task = TaskController.get_tasks_ctrl(db, id=id)

    #         return task

    #     except Exception as e:
    #         print(str(e))
    #         raise HTTPException(status_code=500, detail=str(e))


class TaskCompletedController:
    @staticmethod
    def get_completed_task_details_by_id(db: Session, task_id: int) -> CompletedTaskDetails:
        completed_task = (
            db.query(CompletedTaskDetails)
            .filter(CompletedTaskDetails.task_id == task_id)
            .first()
        )
        return completed_task
