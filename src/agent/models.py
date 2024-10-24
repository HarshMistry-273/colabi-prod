from sqlalchemy import Boolean, Column, Integer, Numeric, String, Text, DateTime, BIGINT
from database import Base
from sqlalchemy.sql import func


# class Agent(Base):
#     __tablename__ = "agents"

#     # Fields from both schemas with duplicates removed
#     id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True, index=True)
#     uuid = Column(String(255), unique=True)

#     name = Column(String(255), nullable=True)
#     description = Column(Text, nullable=True)
#     key_feature = Column(Text, nullable=True)
#     personality = Column(Text, nullable=True)
#     tools = Column(JSON, nullable=True)

#     profile_image = Column(String(255), nullable=True)
#     video = Column(String(255), nullable=True)
#     cost = Column(Numeric(precision=10, scale=2), nullable=True)

#     # Focus Group Survey
#     focus_group_survey = Column(JSON, nullable=True)
#     # focus_group_survey = Column(String(255), nullable=True)
#     # questions = Column(JSON, nullable=True)

#     # Own Data
#     own_data = Column(JSON, nullable=True)
#     # {"file_upload" : True/False, "context" : ""}
#     # file_upload = Column(Boolean, nullable=True)
#     # context = Column(String(255), nullable=True)

#     # top_idea
#     top_ideas = Column(JSON, nullable=True)
#     # focus_group_title = Column(String(255), nullable=True)
#     # focus_group_description = Column(Text, nullable=True)
#     # focus_group_objective = Column(Text, nullable=True)
#     # top_ideas = Column(JSON, nullable=True)
#     # discussion_topic = Column()

#     file_url = Column(String(255), nullable=True)

#     # own_data = Column(String(20), nullable=True)
#     api_data = Column(String(255), nullable=True)
#     survey = Column(String(255), nullable=True)
#     group_id = Column(Text, nullable=True)

#     vector_id = Column(String(36), nullable=True)
#     is_chatbot = Column(Boolean, default=False)


#     created_by = Column(Integer, nullable=True, default=None)
#     created_at = Column(DateTime, default=datetime.now())
#     updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Agent(Base):
    __tablename__ = "ai_agents"

    id = Column(BIGINT, primary_key=True, autoincrement=True, index=True)
    uuid = Column(String(255), unique=True)
    name = Column(String(255), nullable=True)
    cost = Column(Numeric(precision=10, scale=2), nullable=True)
    description = Column(Text, nullable=True)
    profile_image = Column(String(255), nullable=True)
    video = Column(String(255), nullable=True)
    key_feature = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    personality = Column(Text, nullable=True)
    focus_group_survey = Column(String(255), nullable=True)
    own_data = Column(String(255), nullable=True)
    top_idea = Column(String(255), nullable=True)
    api_data = Column(String(255), nullable=True)
    survey = Column(String(255), nullable=True)
    group_id = Column(Text, nullable=True)
    vector_id = Column(String(36), nullable=True)
    tools = Column(String(255), nullable=True)
    is_chatbot = Column(Boolean, default=False)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=True, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=True, server_default=func.now(), onupdate=func.now()
    )
