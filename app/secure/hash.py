from collections import OrderedDict
import hashlib 

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.queries.wanted import get_full_wanted_data

wanted_data_hash = ""

def to_hash(
    data
) -> dict:
    hash_object = hashlib.sha256(data.encode('utf-8'))
    return hash_object.hexdigest()

def to_str(
    data         
) -> str:
    data_str = ""

    if isinstance(data, list) :
        result_str = list()
        for _data in data :
            result_str.append(to_str(_data))
        result_str.sort()
        data_str = str(result_str)
        
    else :
        data_dict = data.__dict__  # 객체의 멤버변수를 딕셔너리로 변환
        sorted_dict = OrderedDict(sorted(data_dict.items(), key=lambda x: x[0]))
        for key, value in sorted_dict.items():
            if isinstance(value, list) : 
                data_str += to_str(value)
            elif key != '_sa_instance_state' :
                data_str += str(value)
    return data_str

def calculate_hash(
    data
) -> str:
    global wanted_data_hash
    wanted_data_hash = to_hash(to_str(data))
    return wanted_data_hash
    
def get_data_hash() -> str :
    return wanted_data_hash

def compare_data_hash(
    required_data_hash : str,
) -> bool :
    return required_data_hash==wanted_data_hash

async def generate_data_hash(
    db_session : AsyncSession,
) -> str :
    wanted_data = await get_full_wanted_data(db = db_session)
    return calculate_hash( wanted_data )