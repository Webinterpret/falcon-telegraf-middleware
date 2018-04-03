from typing import Dict, Any


def merge_and_normalize_tags(*dicts: Dict[Any, Any]):
    result = {}
    for d in dicts:
        if d:
            for k, v in d.items():
                try:
                    result[str(k)] = str(v)
                except:
                    pass  # don't care
    return result