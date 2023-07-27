from collections import OrderedDict
import hashlib 

wanted_data_hash = ""

def to_hash(
    data
) -> dict:
    hash_object = hashlib.sha256(data)
    return hash_object.hexdigest()

def to_str(
    data         
) -> str:
    data_str = ""
    data_dict = data.__dict__  # 객체의 멤버변수를 딕셔너리로 변환
    sorted_dict = OrderedDict(sorted(data_dict.items(), key=lambda x: x[0]))
    for key, value in sorted_dict.items():
        if not isinstance(value, (int, str, list, tuple, dict, set, float, bool)) and isinstance(value, object):
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