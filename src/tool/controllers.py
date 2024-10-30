# Helper function to validate JSON parameters before saving
from datetime import datetime
import json

from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.tool.models import Tools


def validate_tool_parameters(parameters: str) -> bool:
    """
    Validates that the parameters string is valid JSON.
    Returns True if valid, False otherwise.
    """
    try:
        json.loads(parameters)
        return True
    except json.JSONDecodeError:
        return False


class ToolsController:
    @staticmethod
    def create_tool(
        db: Session, tool_data: dict
    ) -> Tools:  # Not using this in current logic
        """
        Helper function to create a new tool with parameter validation.
        """
        if not validate_tool_parameters(tool_data.get("parameters", "{}")):
            raise ValueError("Invalid JSON in parameters field")

        tool = Tools(**tool_data)
        db.add(tool)
        db.commit()
        db.refresh(tool)
        return tool

    @staticmethod
    def update_tools(db: Session, id: str, payload: dict) -> Tools:
        tool = ToolsController.get_tool_by_id(db, id)
        payload.update({"updated_at": datetime.now()})
        # update provided fields
        for field, value in payload.items():
            if value is not None:
                setattr(tool, field, value)

        db.commit()
        db.refresh(tool)

        return tool

    @staticmethod
    def get_all_tools(db: Session) -> list[Tools]:
        tools = db.query(Tools).all()

        if tools:
            return tools
        else:
            return []

    @staticmethod
    def get_tool_by_id(db: Session, id: str) -> Tools:
        tool = db.query(Tools).filter(Tools.uuid == id).first()

        if tool:
            return tool

        raise HTTPException(detail="Tool not found", status_code=404)
