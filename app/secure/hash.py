
hash_dict = {
    "data" : "1",
    "dl_server" : "1"
}


def update_hash(
    data,
    hash_type : str = "data"
) -> None :
    return None

def get_hash(
    hash_type : str = "data"
) -> str :
    return hash_dict[hash_type]

def compare_hash(
    cur_hash : str,
    hash_type : str = "data"
) -> bool :
    return cur_hash == hash_dict[hash_type]