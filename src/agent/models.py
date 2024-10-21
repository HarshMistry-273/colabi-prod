from sqlalchemy import Column, String, Text, JSON, DateTime, Boolean, Float
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Agent(Base):
    __tablename__ = "agents"

    # Fields from both schemas with duplicates removed
    id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
    uuid = Column(String(255), unique=True)
    name = Column(String(255), nullable=False)
    cost = Column(Float, nullable=True)

    role = Column(Text, nullable=False)
    description = Column(Text, nullable=True)

    goal = Column(Text, nullable=False)
    key_feature = Column(Text, nullable=True)

    backstory = Column(Text, nullable=True)
    personality = Column(Text, nullable=True)

    tools = Column(JSON, nullable=True)

    focus_group_title = Column(String(255), nullable=True)
    focus_group_description = Column(Text, nullable=True)
    focus_group_objective = Column(Text, nullable=True)
    top_ideas = Column(JSON, nullable=True)
    validation_survey_title = Column(String(255), nullable=True)
    questions = Column(JSON, nullable=True)
    file_upload = Column(Boolean, nullable=True)
    file_url = Column(String(255), nullable=True)
    context = Column(String(255), nullable=True)
    focus_group_survey = Column(String(255), nullable=True)

    profile_image = Column(String(255), nullable=True)
    video = Column(String(255), nullable=True)
    comment = Column(Text, nullable=True)
    own_data = Column(String(20), nullable=True)
    top_idea = Column(String(20), nullable=True)
    ai_survey = Column(String(255), nullable=True)
    ai_plan_data = Column(String(20), nullable=True)
    survey = Column(String(255), nullable=True)
    group_id = Column(String(255), nullable=True)

    vector_id = Column(String(36), nullable=True)
    is_chatbot = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
