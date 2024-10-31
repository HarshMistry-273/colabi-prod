import logging.config
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from database import get_db_session
from src.tool.controllers import ToolsController
from src.tool.serializers import UpdateToolSchema, get_tools_serializer
from src.utils.logger import logger_set
import logging
from src.crew.tools import ToolKit
from sqlalchemy.orm import Session

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.put("/{id}")
def update_tools(
    request: Request,
    payload: UpdateToolSchema,
    id: str,
    db: Session = Depends(get_db_session),
):
    try:
        tools = ToolsController.update_tools(db=db, id=id, payload=payload.model_dump())

        tools_json = get_tools_serializer(tools=tools)
        logger_set.info(f"Tool Updated: ID: {id}")

        return JSONResponse(
            status_code=200,
            content={
                "msg": "Tool updated",
                "data": {"tools": tools_json},
                "error_msg": "",
                "error": "",
            },
        )
    except HTTPException as e:
        logger_set.error(f"Error occured updating tool : {str(e)}, ToolID: {id}")
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
        logger_set.error(f"Error getting tool : {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "data": {},
                "status": False,
                "error": str(e),
            },
        )


@router.get("")
async def get_tools(request: Request, db: Session = Depends(get_db_session)):
    try:

        id = request.query_params.get("id")

        if id:
            tools = ToolsController.get_tool_by_uuid(db=db, id=id)
        else:
            tools = ToolsController.get_all_tools(db)

        tools_json = get_tools_serializer(tools=tools)
        logger_set.info(f"Tools listed")
        return JSONResponse(
            status_code=200,
            content={
                "msg": "Tool fetched",
                "data": {"tools": tools_json},
                "error_msg": "",
                "error": "",
            },
        )
    except HTTPException as e:
        logger_set.error(f"Error occured while fetching tool : {str(e)}")
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
        logger_set.error(f"Error getting tool : {e}")
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error",
                "data": {},
                "status": False,
                "error": str(e),
            },
        )
