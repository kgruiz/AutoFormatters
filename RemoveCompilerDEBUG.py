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
    def LogAffectedLines(pattern):
        """
        Logs the pattern being applied along with the sorted list of affected line numbers.

        Args:
            pattern (str): The regex pattern to search for.
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

            # Log the lines affected
            logging.debug(f"Removing compiler DEBUG section.")
            logging.debug(f"    Lines affected: {lineNumbers}.")

    # pattern = rf"(^\s*{keyword}\s*(?!.*\(.*).*:)(?=\n(?!\n))"

    # # Add spacing after class declarations unless followed by a comment or a newline
    # patternClassDocstring = r"(\bclass\s+\w+.*:)(\n\s*\"\"\")"
    # LogAffectedLines(patternClassDocstring, "Class declaration followed by docstring")
    # codeContent = re.sub(patternClassDocstring, r"\1\2", codeContent)

    pattern = r"(^\s*)"

    LogAffectedLines(pattern)
    codeContent = re.sub(pattern, r"\1\n", codeContent, flags=re.MULTILINE)

    with open(filePath, "w") as file:
        file.write(codeContent)


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("Usage: python RemoveCompilerDEBUG.py <filePath>")
        print(f"Received arguments: {sys.argv}")
        sys.exit(1)

    FormatNewlines(sys.argv[1])
