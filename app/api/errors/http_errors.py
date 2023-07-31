import os
from typing import Dict, Literal, Optional, Callable
from fastapi import HTTPException
from app.models.schemas.errors import ErrorResponse

class HTTP_Exception :
    def __init__(self,
                 status_code : Literal, 
                 description : Literal,
                 detail : Literal,
                 action : Optional[Callable] = None
                ) -> None :
        self.status_code = status_code
        self.description = description
        self.detail = detail
        self.action = action
    
    @property
    def responses(self) -> Dict[str, Dict[str, ErrorResponse]] :
        return {
            self.status_code : {
                'description' : self.description,
                'model' : ErrorResponse
            }
        }
    
    def error_raise(self, **kwargs) :
        if self.action is not None :
            self.action( **kwargs )
        raise HTTPException(
            status_code = self.status_code,
            detail = self.detail
        )
    
def image_remove( image_path : str) :
    if os.path.exists(image_path):
        os.remove(image_path)