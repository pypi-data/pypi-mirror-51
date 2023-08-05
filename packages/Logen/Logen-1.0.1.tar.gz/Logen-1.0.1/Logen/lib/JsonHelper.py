import json
import os
from typing import Optional

def writeJSON(filepath: str, data: dict) -> None:
    textFile = open(filepath, "w")
    json.dump(data, textFile, indent=4, ensure_ascii=False)

def readJSON(filepath: str) -> Optional[dict]:
    with open(filepath) as file:
        try:
            data = json.load(file)
            return data
        except:
            return None

def isJSONFile(filepath: str) -> bool:
    ext = os.path.splitext(filepath)[-1].lower()
    return ext == ".json"

def dictToJSONString(dict: dict) -> str:
    return json.dumps(dict)