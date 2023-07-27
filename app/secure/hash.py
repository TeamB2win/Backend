from collections import OrderedDict
from typing import List
import hashlib 

from datetime import datetime

wanted_data_hash = ""

def to_hash(
    data
) -> dict:
    hash_object = hashlib.sha256(data)
    return hash_object.hexdigest()

def to_str(
    data         
) -> str:
    print(data)
    data_str = ""

    if isinstance(data, list) :
        for _data in sorted(data) :
            data_str += to_str(_data)
        data_str = data_str.encode('utf-8')
        
    else :
        data_dict = data.__dict__  # 객체의 멤버변수를 딕셔너리로 변환
        sorted_dict = OrderedDict(sorted(data_dict.items(), key=lambda x: x[0]))
        for key, value in sorted_dict.items():
            if isinstance(value, list) : 
                sorted_dict[key] = to_str(value)
        data_str = str(sorted_dict).encode('utf-8')
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