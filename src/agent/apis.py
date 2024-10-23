import logging.config
from fastapi import HTTPException, Request
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from database import get_db_session
from src.agent.controllers import AgentController
from sqlalchemy.orm import Session
from src.utils.logger import logger_set
import logging
from src.agent.serializers import get_agent_serializer

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

router = APIRouter()


# @router.get("")
# async def get_agents(
#     request: Request, id: str = None, db: Session = Depends(get_db_session)
# ):
#     pass


# @router.post("")
# async def create_agent(
#     request: Request,
#     id: int,
#     file_url: str,
#     # name: str = Form(...),
#     # description: str = Form(...),
#     # key_feature: str = Form(...),
#     # personality: str = Form(...),
#     # cost: float = Form(...),
#     # tools: Optional[str] = Form(...),
#     # is_chatbot: Optional[bool] = Form(...),
#     # profile_image: Optional[str] = Form(...),
#     # video: Optional[str] = Form(...),
#     # focus_group_survey: Optional[str] = Form(...),
#     # own_data: Optional[str] = Form(...),
#     # top_idea: Optional[str] = Form(...),
#     # api_data: Optional[str] = Form(...),
#     # survey: Optional[str] = Form(...),
#     # group_id: Optional[str] = Form(...),
#     # created_by: Optional[str] = Form(...),
#     # file: UploadFile = File(...),
#     db: Session = Depends(get_db_session),
# ):
#     """
#     1. Authentication required for all api's if api's will expose to the server any one can create agents without authentication
#     """
#     logger.info("Agent listing endpoint")
#     payload = {
#         "id": id,
#         "file_url": file_url,
#         # "request" : request,
#         # "db" : db,
#         # "name" : name,
#         # "description" : description,
#         # "key_feature" : key_feature,
#         # "personality" : personality,
#         # "cost" : cost,
#         # "profile_image" : profile_image,
#         # "video" : video,
#         # "focus_group_survey" : json.loads(focus_group_survey),
#         # "own_data" : json.loads(own_data),
#         # "top_idea" : json.loads(top_idea),
#         # "api_data" : api_data,
#         # "survey" : survey,
#         # "group_id" : group_id,
#         # "created_by" : created_by
#     }
#     agent = await AgentController.create_agent_ctrl(
#         request=request,
#         db=db,
#         # name=name,
#         # role=description,
#         # goal=key_feature,
#         # backstory=personality,
#         # is_chatbot=is_chatbot,
#         # tools=tools.replace('"', "").split(","),
#         # payload=json.loads(payload),
#         # file=file,
#     )
#     logger_set.info(f"Agent creation successful, Agent Id : {agent[0]['id']}")
#     return JSONResponse(
#         status_code=200,
#         content={
#             "message": "Custom Agent created",
#             "data": {"agents": agent},
#             "error_msg": "",
#             "error": "",
#         },
#     )


@router.put("/custom/{id}")
def update_agent(
    request: Request,
    id: int,
    db: Session = Depends(get_db_session),
):
    payload = {"id": id}
    try:
        agent = AgentController.update_agent_ctrl(db=db, payload=payload)
        agent_dict = get_agent_serializer(agent)
        logger_set.info(f"Agent updation successful, agent Id : {id}")

        return JSONResponse(
            status_code=200,
            content={
                "message": "Custom agent updated",
                "data": {"agents": agent_dict},
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
        logger_set.error(f"Could not update agent : {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "data": {},
                "status": False,
                "error": str(e),
            },
        )


# @router.delete("/{id}")
# async def delete_agent(reuest: Request):
#     pass
