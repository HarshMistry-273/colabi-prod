from fastapi import APIRouter
import logging
from src.utils.logger import logger_set

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)

router = APIRouter()
