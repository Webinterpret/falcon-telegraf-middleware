from typing import Dict, Any


def merge_and_normalize(*dicts: Dict[Any, Any], cast: bool = True):
    result = {}
    for d in dicts:
        if d:
            for k, v in d.items():
                try:
                    result[str(k)] = str(v) if cast else v
                except:
                    pass  # don't care
    return result
