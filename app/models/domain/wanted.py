from typing import Optional, List

from fastapi import File
from pydantic import BaseModel, HttpUrl

from app.models.domain.base import BaseDomainModel

#    id:
#      - type: int
#      - description: 범죄자 식별 id(PK)
#     registered_address:
#      - type: string
#      - description: 주민등록지
#     residence:
#      - type: string
#      - description: 거주지 
#     wanted_type:
#      - type: int
#      - description: 수배 종별(긴급/종합)
#     name:
#      - type: string
#      - description: 이름
#     criminal:
#      - type: string
#      - description: 죄목
#     relational_link:
#      - type: string
#      - description: 범죄행위와 관련된 보도자료(영상)
#     characteristic:
#      - type: string
#      - description: 인상착의 및 특성 (신체적 특징, 방언, 공범)
#     image:
#      - type: string(path)
#      - description : DB에 저장된 범죄자 image 리소스 url
#     video:
#      - type: string(path)
#      - description : DB에 저장된 범죄자 video url

class WantedData(BaseDomainModel) :
    id : int
    registered_address : str
    residence : str
    wanted_type : int
    name : str
    criminal : str
    relational_link : Optional[HttpUrl]
    characteristic : str
    image : str
    video : str