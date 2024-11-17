import logging
import os
import re
import sys


def FormatNewlines(filePath):

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

    if not os.path.isfile(filePath):

        logging.error(f"File not found - {filePath}")
        sys.exit(1)

    with open(filePath, "r", encoding="utf-8") as file:

        codeContent = file.read()

    lines = codeContent.split("\n")

    def GetLineNumber(matchStart):

        cumulative = 0
        for i, line in enumerate(lines, start=1):

            cumulative += len(line) + 1

            if matchStart < cumulative:

                return i

        return -1

    patterns = [
        (r"(class\s+\w+.*\{)\n(?!\n)", r"\1\n\n", "class declarations"),
        (r"(struct\s+\w+.*\{)\n(?!\n)", r"\1\n\n", "struct declarations"),
        (r"(namespace\s+\w+\s*\{)\n(?!\n)", r"\1\n\n", "namespace declarations"),
        (
            r"^(?!\s*return\s)((?:\w+\s+)+\w+\s*\([^)]*\)\s*(?:\{|\;))\n(?!\n)",
            r"\1\n\n",
            "function declarations/definitions",
        ),
        (r"(if\s*\(.*\)\s*\{)\n(?!\n)", r"\1\n\n", "if statements"),
        (r"(else\s+if\s*\(.*\)\s*\{)\n(?!\n)", r"\1\n\n", "else if statements"),
        (r"(else\s*\{)\n(?!\n)", r"\1\n\n", "else statements"),
        (r"(for\s*\(.*\)\s*\{)\n(?!\n)", r"\1\n\n", "for loops"),
        (r"(while\s*\(.*\)\s*\{)\n(?!\n)", r"\1\n\n", "while loops"),
        (r"(switch\s*\(.*\)\s*\{)\n(?!\n)", r"\1\n\n", "switch statements"),
        (
            r"(?<!\n)\n((?:\w+\s+)+\w+\s*\([^)]*\)\s*\{)",
            r"\n\n\1",
            "function implementation spacing",
        ),
        (r"(?<!\n)(^\s*return\b)", r"\n\1", "return statement spacing"),
    ]

    for pattern, replacement, description in patterns:

        matches = list(re.finditer(pattern, codeContent, re.MULTILINE))
        lineNumbers = []

        for match in matches:

            lineNumber = GetLineNumber(match.start())

            if lineNumber != -1:

                lineNumbers.append(lineNumber)

        if matches:

            logging.debug(f"Applying pattern for {description}: {pattern}")
            logging.debug(f"    Lines affected: {sorted(lineNumbers)}")
            codeContent = re.sub(pattern, replacement, codeContent, flags=re.MULTILINE)

        else:

            logging.debug(f"No matches found for pattern: {pattern}")

    with open(filePath, "w", encoding="utf-8") as file:

        file.write(codeContent)
        logging.info(f"File '{filePath}' has been formatted successfully.")


if __name__ == "__main__":

    if len(sys.argv) != 2:

        logging.error("Usage: python CppSpaceLines.py <filePath>")
        logging.error(f"Received arguments: {sys.argv}")
        sys.exit(1)

    FormatNewlines(sys.argv[1])
