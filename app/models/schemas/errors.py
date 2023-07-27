from app.models.schemas.base import BaseSchemaModel

class ErrorResponse(BaseSchemaModel) :
    detail : str