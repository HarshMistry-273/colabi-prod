from datetime import datetime
from fastapi import HTTPException
from src.task.models import CompletedTaskDetailFiles, Tasks, CompletedTaskDetails
from sqlalchemy.orm import Session


class TaskController:

    @staticmethod
    def get_tasks_by_id_ctrl(db: Session, id: int) -> Tasks:
        task = db.query(Tasks).filter(Tasks.id == id).first()

        if task:
            return task

        raise HTTPException(detail="Task not found", status_code=404)


class TaskCompletedController:
    @staticmethod
    def get_completed_task_details_by_id(
        db: Session, task_id: int
    ) -> CompletedTaskDetails:
        completed_task = (
            db.query(CompletedTaskDetails)
            .filter(CompletedTaskDetails.task_id == task_id)
            .first()
        )

        if completed_task:
            return completed_task

        raise HTTPException(detail="Completed task not found", status_code=404)

    @staticmethod
    def create_completed_task_details(
        db: Session,
        task_id: int,
        from_user: int,
        to_user: int,
        from_user_role_id: int,
        output: str,
        comment: str,
        file_path: str,
    ) -> CompletedTaskDetails:
        completed_task = CompletedTaskDetails(
            task_id=task_id,
            from_user=from_user,
            to_user=to_user,
            from_user_role_id=from_user_role_id,
            output=output,
            comment=comment,
            status=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        try:
            db.add(completed_task)
            db.commit()
            db.refresh(completed_task)
        except Exception as e:
            raise HTTPException(detail="Database error", status_code=400)

        if file_path:
            create_file = TaskCompletedFileController.create_completed_file_details(
                db, completed_task_id=completed_task.id, file_path=file_path
            )

            if not create_file:
                ...

        return completed_task.id


class TaskCompletedTaskDetails:
    @staticmethod
    def get_completed_task_by_id(db: Session, id: int = None):
        completed_task = (
            db.query(CompletedTaskDetails).filter(CompletedTaskDetails.id == id).first()
        )

        if completed_task:
            return completed_task
        raise HTTPException(detail="Completed task not found", status_code=404)

    @staticmethod
    def get_all_completed_task(db: Session):
        completed_task = db.query(CompletedTaskDetails).all()

        return completed_task


class TaskCompletedFileController:
    @staticmethod
    def create_completed_file_details(
        db: Session, completed_task_id: int, file_path: str
    ) -> CompletedTaskDetailFiles:
        com_task_file = CompletedTaskDetailFiles(
            completed_task_detail_id=completed_task_id, file_name=file_path
        )

        try:
            db.add(com_task_file)
            db.commit()
            db.refresh(com_task_file)
        except Exception as e:
            raise HTTPException(detail="Database error", status_code=400)
        return com_task_file
