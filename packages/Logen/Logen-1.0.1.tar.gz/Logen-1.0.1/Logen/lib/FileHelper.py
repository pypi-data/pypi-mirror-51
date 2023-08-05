import os
import shutil

from typing import List

#--------------------
# Files
#--------------------

def writeFile(filepath: str, content: str) -> None:
    textFile = open(filepath, "w")
    textFile.write(content)
    textFile.close()

def readFile(filepath: str) -> str:
    textFile = open(filepath, "r")
    content = textFile.read()
    textFile.close()
    return content

def readLines(filepath: str) -> List[str]:
    return readFile(filepath).split("\n")

def filename(filepath: str) -> str:
    return os.path.basename(filepath)

def directoryName(filepath: str) -> str:
    return os.path.dirname(filepath).split('/')[-1]

def directoryPath(filepath: str) -> str:
    return os.path.dirname(filepath)

def fileExtension(filepath: str) -> str:
    return os.path.splitext(filepath)[-1].lower()

def exists(filepath: str) -> bool:
    return os.path.exists(filepath)

#--------------------
# Direcories
#--------------------

def createDir(filepath: str) -> None:
    os.makedirs(filepath)

def removeDir(filepath: str) -> None:
    shutil.rmtree(filepath)