"""
drex.schema.models — Base Pydantic model shared across all services.
© 2025 swordenkisk — All Rights Reserved.
"""

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict


class BaseModel(PydanticBaseModel):
    """
    Drex base model.

    All shared Pydantic models should inherit from this class so that
    project-wide config (e.g. strict mode, alias generation) is applied
    consistently.
    """

    model_config = ConfigDict(
        populate_by_name=True,  # allow field name OR alias
        str_strip_whitespace=True,
        validate_default=True,
    )
