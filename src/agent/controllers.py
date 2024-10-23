from src.agent.models import Agent
from fastapi import HTTPException, Request, UploadFile
from sqlalchemy.orm import Session
from src.agent.task import embedded_docs
from src.config import Config
from src.utils.utils import get_uuid


class AgentController:

    @staticmethod
    def get_agents_by_id_ctrl(db: Session, id: str) -> Agent:
        agent = db.query(Agent).filter(Agent.id == id).first()

        if agent:
            return agent
        else:
            raise HTTPException(detail="Agent not found", status_code=404)

    # @staticmethod
    # def create_agent_ctrl(
    #     request: Request,
    #     db: Session,
    #     name: str,
    #     role: str,
    #     goal: str,
    #     backstory: str,
    #     tools: str,
    #     is_chatbot: bool,
    #     payload: dict,
    #     file: UploadFile,
    # ) -> list[dict]:
    #     pass

    @staticmethod
    def update_agent_ctrl(
        db: Session,
        payload: dict = {},
    ) -> Agent:

        agent = AgentController.get_agents_by_id_ctrl(db=db, id=payload.get("id"))

        # Generate new namespace for vector store
        namespace = get_uuid()
        url_file_type = str(agent.own_data).rsplit(".")[-1]
        if url_file_type not in Config.SUPPORTED_FILE_TYPES:
            raise ValueError(
                f"Unsupported file type. Supported types: {Config.SUPPORTED_FILE_TYPES}"
            )
        # Schedule document embedding task
        embedded_docs.delay(
            api_key=Config.PINECONE_API_KEY,
            index_name=Config.PINECONE_INDEX_NAME,
            namespace=namespace,
            url=agent.own_data,
            url_file_type=url_file_type,
        )
        agent.vector_id = namespace

        db.commit()
        db.refresh(agent)

        return agent

    # @staticmethod
    # async def delete_agents_by_id_ctrl(
    #     request: Request, db: Session, id: str
    # ) -> list[dict]:
    #     """
    #     Do we have to hard delete or soft delete agent?
    #     Do we want to delete all the task perform by the agent if user deletes that agent?
    #     """
    #     pass
