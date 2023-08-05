import argparse
from typing import List

from .converter.ConverterInterface import ConverterInterface

#--------------------
# Starting point
#--------------------

def start(args: argparse.Namespace, converter: List[ConverterInterface]) -> None:
    print("Available converter:\n")
    descriptions = list(map(lambda x: _describe(x), converter))
    for description in descriptions:
        print(description)

#--------------------
# private helper
#--------------------

def _describe(converter: ConverterInterface) -> str:
    content = "Identifier: {}\n".format(converter.identifier()) 
    content += "file extension: {}\n".format(converter.fileExtension())
    content += "import description: {}\n".format(converter.importDescription())
    content += "export description: {}\n".format(converter.exportDescription())
    return content