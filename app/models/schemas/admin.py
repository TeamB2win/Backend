from pydantic import BaseModel,ConfigDict
from typing import List
from typing import Optional

# 범죄자 데이터 생성시 유저에게 요청사항
class CreateCriminalDataRequest(BaseModel):
    name: str
    wanted_type: int # 수배 종별
    criminal: str # 죄목
    registered_address: str # 주민등록지
    residence: str # 거주지
    characteristic: str # 특징
    relational_link: str # 관련 보도자료
    image: bytes # 이미지 

# 범죄자 데이터 구조
class CriminalDataSchema(BaseModel):
    id: Optional[int]
    name: str
    wanted_type: int # 수배 종별
    criminal: str # 죄목
    registered_address: str # 주민등록지
    residence: str # 거주지
    characteristic: str # 특징
    relational_link: str # 관련 보도자료
    image: bytes # 이미지
    #video_url: Optional[bytes]  # 비디오 영상
    model_config = ConfigDict(
    from_attributes = True,
    validate_assignment = True,
    populate_by_name = True,
    # json_encoders = {datetime.datetime: convert_datetime_to_realworld}
    )

# 범죄자 데이터 수정시 유저에게 요청
class UpdateCriminalData(BaseModel):
    id: Optional[int]
    registered_address: Optional[str]
    residence: Optional[str]
    wanted_type: Optional[int]
    name: Optional[str]
    criminal: Optional[str]
    relational_link: Optional[str]
    characteristic: Optional[str]
    image: Optional[bytes]
    
class ListCriminalDataResponse(BaseModel):
    CriminalData: List[CriminalDataSchema]
    model_config = ConfigDict(
    from_attributes = True,
    validate_assignment = True,
    populate_by_name = True,
        # json_encoders = {datetime.datetime: convert_datetime_to_realworld},    
    )

# 범죄자 비디오 데이터 DB에게 요청
class UpdateCriminalVideoData(BaseModel):
    video_url: Optional[bytes]
    from pydantic import BaseModel,ConfigDict
from typing import List
from typing import Optional

# 범죄자 데이터 생성시 유저에게 요청사항
class CreateCriminalDataRequest(BaseModel):
    name: str
    wanted_type: int # 수배 종별
    criminal: str # 죄목
    registered_address: str # 주민등록지
    residence: str # 거주지
    characteristic: str # 특징
    relational_link: str # 관련 보도자료
    image: bytes # 이미지 

# 범죄자 데이터 구조
class CriminalDataSchema(BaseModel):
    id: Optional[int]
    name: str
    wanted_type: int # 수배 종별
    criminal: str # 죄목
    registered_address: str # 주민등록지
    residence: str # 거주지
    characteristic: str # 특징
    relational_link: str # 관련 보도자료
    image: bytes # 이미지
    #video_url: Optional[bytes]  # 비디오 영상
    model_config = ConfigDict(
    from_attributes = True,
    validate_assignment = True,
    populate_by_name = True,
    # json_encoders = {datetime.datetime: convert_datetime_to_realworld}
    )

# 범죄자 데이터 수정시 유저에게 요청
class UpdateCriminalData(BaseModel):
    id: Optional[int]
    registered_address: Optional[str]
    residence: Optional[str]
    wanted_type: Optional[int]
    name: Optional[str]
    criminal: Optional[str]
    relational_link: Optional[str]
    characteristic: Optional[str]
    image: Optional[bytes]
    
class ListCriminalDataResponse(BaseModel):
    CriminalData: List[CriminalDataSchema]
    model_config = ConfigDict(
    from_attributes = True,
    validate_assignment = True,
    populate_by_name = True,
        # json_encoders = {datetime.datetime: convert_datetime_to_realworld},    
    )

# 범죄자 비디오 데이터 DB에게 요청
class UpdateCriminalVideoData(BaseModel):
    video_url: Optional[bytes]
    from pydantic import BaseModel,ConfigDict
from typing import List
from typing import Optional

# 범죄자 데이터 생성시 유저에게 요청사항
class CreateCriminalDataRequest(BaseModel):
    name: str
    wanted_type: int # 수배 종별
    criminal: str # 죄목
    registered_address: str # 주민등록지
    residence: str # 거주지
    characteristic: str # 특징
    relational_link: str # 관련 보도자료
    image: bytes # 이미지 

# 범죄자 데이터 구조
class CriminalDataSchema(BaseModel):
    id: Optional[int]
    name: str
    wanted_type: int # 수배 종별
    criminal: str # 죄목
    registered_address: str # 주민등록지
    residence: str # 거주지
    characteristic: str # 특징
    relational_link: str # 관련 보도자료
    image: bytes # 이미지
    #video_url: Optional[bytes]  # 비디오 영상
    model_config = ConfigDict(
    from_attributes = True,
    validate_assignment = True,
    populate_by_name = True,
    # json_encoders = {datetime.datetime: convert_datetime_to_realworld}
    )

# 범죄자 데이터 수정시 유저에게 요청
class UpdateCriminalData(BaseModel):
    id: Optional[int]
    registered_address: Optional[str]
    residence: Optional[str]
    wanted_type: Optional[int]
    name: Optional[str]
    criminal: Optional[str]
    relational_link: Optional[str]
    characteristic: Optional[str]
    image: Optional[bytes]
    
class ListCriminalDataResponse(BaseModel):
    CriminalData: List[CriminalDataSchema]
    model_config = ConfigDict(
    from_attributes = True,
    validate_assignment = True,
    populate_by_name = True,
        # json_encoders = {datetime.datetime: convert_datetime_to_realworld},    
    )

# 범죄자 비디오 데이터 DB에게 요청
class UpdateCriminalVideoData(BaseModel):
    video_url: Optional[bytes]
    from pydantic import BaseModel,ConfigDict
from typing import List
from typing import Optional

# 범죄자 데이터 생성시 유저에게 요청사항
class CreateCriminalDataRequest(BaseModel):
    name: str
    wanted_type: int # 수배 종별
    criminal: str # 죄목
    registered_address: str # 주민등록지
    residence: str # 거주지
    characteristic: str # 특징
    relational_link: str # 관련 보도자료
    image: bytes # 이미지 

# 범죄자 데이터 구조
class CriminalDataSchema(BaseModel):
    id: Optional[int]
    name: str
    wanted_type: int # 수배 종별
    criminal: str # 죄목
    registered_address: str # 주민등록지
    residence: str # 거주지
    characteristic: str # 특징
    relational_link: str # 관련 보도자료
    image: bytes # 이미지
    #video_url: Optional[bytes]  # 비디오 영상
    model_config = ConfigDict(
    from_attributes = True,
    validate_assignment = True,
    populate_by_name = True,
    # json_encoders = {datetime.datetime: convert_datetime_to_realworld}
    )

# 범죄자 데이터 수정시 유저에게 요청
class UpdateCriminalData(BaseModel):
    id: Optional[int]
    registered_address: Optional[str]
    residence: Optional[str]
    wanted_type: Optional[int]
    name: Optional[str]
    criminal: Optional[str]
    relational_link: Optional[str]
    characteristic: Optional[str]
    image: Optional[bytes]
    
class ListCriminalDataResponse(BaseModel):
    CriminalData: List[CriminalDataSchema]
    model_config = ConfigDict(
    from_attributes = True,
    validate_assignment = True,
    populate_by_name = True,
        # json_encoders = {datetime.datetime: convert_datetime_to_realworld},    
    )

# 범죄자 비디오 데이터 DB에게 요청
class UpdateCriminalVideoData(BaseModel):
    video_url: Optional[bytes]
    from pydantic import BaseModel,ConfigDict
from typing import List
from typing import Optional

# 범죄자 데이터 생성시 유저에게 요청사항
class CreateCriminalDataRequest(BaseModel):
    name: str
    wanted_type: int # 수배 종별
    criminal: str # 죄목
    registered_address: str # 주민등록지
    residence: str # 거주지
    characteristic: str # 특징
    relational_link: str # 관련 보도자료
    image: bytes # 이미지 

# 범죄자 데이터 구조
class CriminalDataSchema(BaseModel):
    id: Optional[int]
    name: str
    wanted_type: int # 수배 종별
    criminal: str # 죄목
    registered_address: str # 주민등록지
    residence: str # 거주지
    characteristic: str # 특징
    relational_link: str # 관련 보도자료
    image: bytes # 이미지
    #video_url: Optional[bytes]  # 비디오 영상
    model_config = ConfigDict(
    from_attributes = True,
    validate_assignment = True,
    populate_by_name = True,
    # json_encoders = {datetime.datetime: convert_datetime_to_realworld}
    )

# 범죄자 데이터 수정시 유저에게 요청
class UpdateCriminalData(BaseModel):
    id: Optional[int]
    registered_address: Optional[str]
    residence: Optional[str]
    wanted_type: Optional[int]
    name: Optional[str]
    criminal: Optional[str]
    relational_link: Optional[str]
    characteristic: Optional[str]
    image: Optional[bytes]
    
class ListCriminalDataResponse(BaseModel):
    CriminalData: List[CriminalDataSchema]
    model_config = ConfigDict(
    from_attributes = True,
    validate_assignment = True,
    populate_by_name = True,
        # json_encoders = {datetime.datetime: convert_datetime_to_realworld},    
    )

# 범죄자 비디오 데이터 DB에게 요청
class UpdateCriminalVideoData(BaseModel):
    video_url: Optional[bytes]
    