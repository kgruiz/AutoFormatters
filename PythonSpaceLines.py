import logging
import os
import re
import sys


def FormatNewlines(filePath):

    # Configure logging for debugging
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

    if not os.path.isfile(filePath):

        logging.error(f"File not found - {filePath}")
        sys.exit(1)

    with open(filePath, "r") as file:
        codeContent = file.read()

    # Function to log affected lines with specified format
    def LogAffectedLines(pattern, description):
        """
        Logs the pattern being applied along with the sorted list of affected line numbers.

        Args:
            pattern (str): The regex pattern to search for.
            description (str): Description of the substitution for logging.
        """
        # Find all matches
        matches = list(
            re.finditer(pattern, codeContent, flags=re.MULTILINE | re.DOTALL)
        )
        if matches:

            # Collect unique line numbers affected
            lineNumbers = sorted(
                set(codeContent.count("\n", 0, match.start()) + 1 for match in matches)
            )

            # Log the pattern and description
            logging.debug(f"Applying pattern for {description}: {pattern}")
            logging.debug(f"    Lines affected: {lineNumbers}")

    # Add spacing after class declarations unless followed by a comment or a newline
    patternClassDocstring = r"(\bclass\s+\w+.*:)(\n\s*\"\"\")"
    LogAffectedLines(patternClassDocstring, "Class declaration followed by docstring")
    codeContent = re.sub(patternClassDocstring, r"\1\2", codeContent)

    patternClassNewline = r"(\bclass\s+\w+.*:)\n(?!\s*\"\"\"|\n)"
    LogAffectedLines(patternClassNewline, "Added newline after class declaration")
    codeContent = re.sub(patternClassNewline, r"\1\n\n", codeContent)

    # Add spacing after function declarations unless followed by a comment or a newline
    patternDefDocstring = r"(\bdef\s+\w+.*:)(\n\s*\"\"\")"
    LogAffectedLines(patternDefDocstring, "Function declaration followed by docstring")
    codeContent = re.sub(patternDefDocstring, r"\1\2", codeContent)

    patternDefNewline = r"(\bdef\s+\w+.*:)\n(?!\s*\"\"\"|\n)"
    LogAffectedLines(patternDefNewline, "Added newline after function declaration")
    codeContent = re.sub(patternDefNewline, r"\1\n\n", codeContent)

    # Add spacing after comments ending in """ unless already followed by a newline
    patternDocstringNewline = r"(\"\"\".*?\"\"\")\n(?!\n)"
    LogAffectedLines(patternDocstringNewline, "Added newline after docstring")
    codeContent = re.sub(patternDocstringNewline, r"\1\n\n", codeContent)

    controlKeywords = [
        "if",
        "elif",
        "else",
        "while",
        "with",
        "try",
        "except",
        "finally",
        "return",
    ]

    # Add spacing after control flow keywords unless an opening parenthesis is present
    for keyword in controlKeywords:

        if keyword in ["if", "for"]:

            pattern = rf"(^\s*{keyword}\s*(?!.*\(.*).*:)(?=\n(?!\n))"
            description = (
                f"Added newline after '{keyword}' statement without parentheses"
            )
        else:

            pattern = rf"(^\s*{keyword}\s*(?!.*\(.*).*)(?=\n(?!\n))"
            description = (
                f"Added newline after '{keyword}' statement without parentheses"
            )

        LogAffectedLines(pattern, description)
        codeContent = re.sub(pattern, r"\1\n", codeContent, flags=re.MULTILINE)

    # Ensure blank lines are added after complete parentheses
    def InsertBlankAfterClosedParentheses(match):

        line = match.group(0)
        openingCount = line.count("(")
        closingCount = line.count(")")

        if openingCount == closingCount:  # Check if parentheses are balanced
            if not re.search(r"\n\s*\n", codeContent[match.end() :]):

                return line + "\n"

        return line

    patternParentheses = r"^.*\)$"
    # Log affected lines before substitution
    matchesParentheses = list(
        re.finditer(patternParentheses, codeContent, flags=re.MULTILINE)
    )

    if matchesParentheses:

        lineNumbers = sorted(
            set(
                codeContent.count("\n", 0, match.start()) + 1
                for match in matchesParentheses
            )
        )
        logging.debug(
            f"Applying pattern for Adding newline after closing parentheses: {patternParentheses}"
        )
        logging.debug(f"    Lines affected: {lineNumbers}")

    codeContent = re.sub(
        patternParentheses,
        InsertBlankAfterClosedParentheses,
        codeContent,
        flags=re.MULTILINE,
    )

    patternForIfNewline = r"(^\s*(for|if)\s*[^\(]*:\n)(?!\n)"
    LogAffectedLines(
        patternForIfNewline,
        "Added newline after 'for' or 'if' statement without parentheses",
    )
    codeContent = re.sub(patternForIfNewline, r"\1\n", codeContent, flags=re.MULTILINE)

    patternForIfComplex = r"(^\s*(for|if)\s*[^\(]*\(?(?!.*\(.*\(.*).*?\)?:\n)(?!\n)"
    LogAffectedLines(
        patternForIfComplex,
        "Added newline after complex 'for' or 'if' statement without nested parentheses",
    )
    codeContent = re.sub(patternForIfComplex, r"\1\n", codeContent, flags=re.MULTILINE)

    # Remove any added blank lines at the end of the file
    patternTrailingNewlines = r"\n+$"
    if re.search(patternTrailingNewlines, codeContent):

        logging.debug("Removed trailing blank lines at the end of the file.")
    codeContent = re.sub(patternTrailingNewlines, "\n", codeContent)

    with open(filePath, "w") as file:
        file.write(codeContent)


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("Usage: python PythonSpaceLines.py <filePath>")
        print(f"Received arguments: {sys.argv}")
        sys.exit(1)

    FormatNewlines(sys.argv[1])