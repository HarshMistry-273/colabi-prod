from sqlalchemy import (
    BIGINT,
    Column,
    Integer,
    SmallInteger,
    String,
    Text,
    Date,
    DateTime,
    BigInteger,
)
from database import Base


class Tasks(Base):
    __tablename__ = "tasks"

    # Primary and Foreign Keys
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    ai_project_detail_id = Column(Integer, nullable=False)
    workflow_id = Column(Integer, nullable=False)
    category_id = Column(BigInteger, nullable=True)

    # Basic Task Information
    uuid = Column(String(250), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    video_file = Column(String(255), nullable=True)
    completion_date = Column(Date, nullable=True)
    reoccurring = Column(String(255), nullable=True)

    # Agent Related Fields
    assign_task_agent_id = Column(String(1000), nullable=True)
    agent_tool = Column(String(1000), nullable=True)
    agent_instruction = Column(Text, nullable=True)
    agent_output = Column(Text, nullable=True)
    agent_parameter = Column(Text, nullable=True)

    # Team Member Related Fields
    assign_task_team_member_id = Column(String(1000), nullable=True)
    team_member_ai_agent_for_assistance = Column(String(1000), nullable=True)
    team_member_instruction = Column(Text, nullable=True)
    team_member_output = Column(Text, nullable=True)

    # Colabi Member Related Fields
    assign_task_colabi_member_id = Column(String(1000), nullable=True)
    colabi_member_ai_agent_for_assistance = Column(String(1000), nullable=True)
    colabi_member_instruction = Column(Text, nullable=True)
    colabi_member_output = Column(Text, nullable=True)

    # Self Related Fields
    assign_task_my_self_id = Column(String(1000), nullable=True)
    my_self_ai_agent_for_assistance = Column(String(1000), nullable=True)
    my_self_instruction = Column(Text, nullable=True)
    my_self_output = Column(Text, nullable=True)

    # Client Related Fields
    assign_task_client_id = Column(String(1000), nullable=True)
    client_ai_agent_for_assistance = Column(String(1000), nullable=True)
    client_instruction = Column(Text, nullable=True)
    client_output = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, nullable=False)


class CompletedTaskDetailFiles(Base):
    __tablename__ = "completed_task_detail_files"

    # Primary and Foreign Keys
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    completed_task_detail_id = Column(Integer, nullable=False)

    # File Information
    file_name = Column(Text, nullable=False)

    # Timestamps
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class CompletedTaskDetails(Base):
    __tablename__ = "completed_task_details"

    # Primary and Foreign Keys
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    task_id = Column(Integer, nullable=False)

    # User Information
    from_user = Column(Integer, nullable=False)
    to_user = Column(Integer, nullable=False)
    from_user_role_id = Column(Integer, nullable=False)

    # Task Details
    output = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)

    # Status Fields
    status = Column(
        SmallInteger, nullable=False, default=0
    )  # 0 => pending, 1 => completed, 2 => failed
    mark_as = Column(
        SmallInteger, nullable=False, default=0
    )  # 0 => pending, 1 => completed, 2 => reassign

    # Timestamps
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
