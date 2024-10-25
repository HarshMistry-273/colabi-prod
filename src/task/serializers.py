from typing import Optional
from src.task.models import Tasks
from pydantic import BaseModel


class CreateTaskSchema(BaseModel):
    task_id: int
    from_user: int
    to_user: int
    from_user_role_id:  int
    include_previous_output: Optional[bool] = False
    previous_output: Optional[list[str]] = []
    is_csv: Optional[bool] = False


def get_task_serializer(tasks: list[Tasks]) -> list[dict]:
    tasks_list = []

    if not isinstance(tasks, list):
        tasks = [tasks]

    for task in tasks:
        tasks_list.append(
            {
                # Primary and Foreign Keys
                "id": task.id,
                "ai_project_detail_id": task.ai_project_detail_id,
                "workflow_id": task.workflow_id,
                "category_id": task.category_id,
                # Basic Task Information
                "uuid": task.uuid,
                "title": task.title,
                "description": task.description,
                "start_date": task.start_date,
                "video_file": task.video_file,
                "completion_date": task.completion_date,
                "reoccurring": task.reoccurring,
                # Agent Related Fields
                "assign_task_agent_id": task.assign_task_agent_id,
                "agent_tool": task.agent_tool,
                "agent_instruction": task.agent_instruction,
                "agent_output": task.agent_output,
                "agent_parameter": task.agent_parameter,
                # Team Member Related Fields
                "assign_task_team_member_id": task.assign_task_team_member_id,
                "team_member_ai_agent_for_assistance": task.team_member_ai_agent_for_assistance,
                "team_member_instruction": task.team_member_instruction,
                "team_member_output": task.team_member_output,
                # Colabi Member Related Fields
                "assign_task_colabi_member_id": task.assign_task_colabi_member_id,
                "colabi_member_ai_agent_for_assistance": task.colabi_member_ai_agent_for_assistance,
                "colabi_member_instruction": task.colabi_member_instruction,
                "colabi_member_output": task.colabi_member_output,
                # Self Related Fields
                "assign_task_my_self_id": task.assign_task_my_self_id,
                "my_self_ai_agent_for_assistance": task.my_self_ai_agent_for_assistance,
                "my_self_instruction": task.my_self_instruction,
                "my_self_output": task.my_self_output,
                # Client Related Fields
                "assign_task_client_id": task.assign_task_client_id,
                "client_ai_agent_for_assistance": task.client_ai_agent_for_assistance,
                "client_instruction": task.client_instruction,
                "client_output": task.client_output,
                # Metadata
                "created_at": str(task.created_at),
                "updated_at": str(task.updated_at),
                "created_by": str(task.created_by),
            }
        )

    return tasks_list
