import logging
import re
import sys
from json import dump, dumps
from pathlib import Path

import black


def FormatPythonFile(filePath: Path) -> None:
    """
    Formats a Python file using the Black API.
    """

    fileContent = Path(filePath).read_text()

    formattedContent = black.format_str(fileContent, mode=black.Mode())

    Path(filePath).write_text(formattedContent)


def FormatNewlines(filePath: Path) -> None:

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

    if not filePath.is_file():

        logging.error(f"File not found - {filePath}")
        sys.exit(1)

    with open(filePath, "r") as file:

        codeContent = file.read()


def FormatFile(filePath: Path) -> None:

    FormatNewlines(filePath=filePath)

    FormatPythonFile(filePath=filePath)


if __name__ == "__main__":

    currentFilePath = Path(__file__).resolve()

    logging.debug(f"Current file path: {currentFilePath}")

    FormatFile(currentFilePath)

    raise SystemExit

    if len(sys.argv) != 2:

        print("Usage: python PythonSpaceLines.py <filePath>")
        print(f"Received arguments: {sys.argv}")
        sys.exit(1)

    FormatFile(sys.argv[1])
