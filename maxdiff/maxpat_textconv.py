"""Module to convert a maxpat file to a textual representation that can then be diffed."""

import sys
import json
import argparse
from patch_printer import print_patcher
from print_unicode import print_unicode_string


def parse(path: str) -> dict | str:
    """Parse a file and returns a textual representation of it."""
    with open(path, "r", encoding="utf-8") as file_obj:
        try:
            patcher_dict = json.load(file_obj)
        except Exception as e:
            file_obj.seek(0)
            file_string = file_obj.read()
            if (
                "=======" in file_string
                or "<<<<<<<" in file_string
                or ">>>>>>>" in file_string
            ):
                return "Patch file contains merge conflict markers. Please make sure to resolve merge conflicts."
            else:
                return f"Error parsing patch: {e}"

        return print_patcher(patcher_dict)


def main():
    """Entry point of the program."""
    parser = argparse.ArgumentParser(
        description="Convert a Max patch to a textual representation"
    )
    parser.add_argument("file", help="Path to the file to convert")
    args = parser.parse_args()

    try:
        result = parse(args.file)
        print_unicode_string(result)
    except RuntimeError as err:
        print("Error: ", *err.args)
        sys.exit(2)


if __name__ == "__main__":
    main()
