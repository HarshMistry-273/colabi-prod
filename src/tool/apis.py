import logging.config
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from database import get_db_session
from sqlalchemy.orm import Session
from src.utils.logger import logger_set
import logging
from src.crew.tools import ToolKit

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("")
async def get_tools(request: Request):
    try:
        tools = [tool_name.name for tool_name in ToolKit]

        logger_set.info(f"Tools listed")

        return JSONResponse(
            status_code=200,
            content={
                "msg": "Tool fetched",
                "data": {"tools": tools},
                "error_msg": "",
                "error": "",
            },
        )
    except Exception as e:
        logger_set.error(f"Error getting tool : {e}")
        return JSONResponse(
            status_code=500,
            content={
                "msg": "",
                "data": {},
                "error_msg": "Invalid request",
                "error": str(e),
            },
        )
