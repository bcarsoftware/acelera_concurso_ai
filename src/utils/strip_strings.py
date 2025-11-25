from typing import Dict, Any


async def strip_strings(data: Dict[str, Any]) -> Dict[str, Any]:
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.strip()

    return data
