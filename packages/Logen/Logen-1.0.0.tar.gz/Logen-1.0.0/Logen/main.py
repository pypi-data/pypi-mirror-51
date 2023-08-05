import argparse
import sys

from typing import List

from .converter.AndroidConverter import AndroidConverter
from .converter.JSONConverter import JSONConverter
from .converter.iOSConverter import iOSConverter
from .converter.iOSEnumConverter import iOSEnumConverter

from . import main_subcommand_convert
from . import main_subcommand_list

#--------------------
# properties
#--------------------

registeredConverter = [
        iOSConverter(),
        iOSEnumConverter(),
        AndroidConverter(),
        JSONConverter()
]

#--------------------
# Setup CLI
#--------------------

def createParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description = "Description")
    subparsers = parser.add_subparsers(help = "Subparser")

    parser_convert = subparsers.add_parser("convert", help = "Lists all available converter.")
    parser_convert.add_argument("source", help = "Path to source file")
    parser_convert.add_argument("destination", help = "Path at which destination directory will be created")
    parser_convert.add_argument("importConverter", help = "Identifier of the converter to be used to import content of the given file.")
    parser_convert.add_argument("exportConverter", help = "Identifier of the converter to be used to export content with a specific format.")
    parser_convert.add_argument("-f", "--force", action = "store_true", help = "If true, destination directory will be overwritten if it already exists.")
    parser_convert.add_argument("-d", "--dryRun", action = "store_true", help = "If true, result will be printed to the console and not saved.")
    parser_convert.add_argument("-v", "--verbose", action = "store_true", help = "If true, additional information will be written to the console.")
    parser_convert.set_defaults(func = subcommandConvert)

    parser_list = subparsers.add_parser("list", help = "Lists all available converter.")
    parser_list.set_defaults(func = subcommandList)
    return parser

def parse(args: List[str]) -> argparse.Namespace:
    parser = createParser()
    parsedArgs = parser.parse_args(args)
    return parsedArgs

def subcommandList(args: argparse.Namespace) -> None:
    main_subcommand_list.start(args, registeredConverter)

def subcommandConvert(args: argparse.Namespace) -> None:
    main_subcommand_convert.start(args, registeredConverter)

#--------------------
# Main
#--------------------

def main():
    parsedArgs = parse(sys.argv[1:])
    parsedArgs.func(parsedArgs)


if __name__ == "__main__":
    main()
