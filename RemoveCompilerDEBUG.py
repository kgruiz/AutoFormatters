import logging
import os
import re
import sys


def FormatNewlines(filePath):

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

    if not os.path.isfile(filePath):

        logging.error(f"File not found - {filePath}")
        sys.exit(1)

    with open(filePath, "r") as file:

        codeContent = file.read()

    def LogAffectedLines(pattern):

        matches = list(
            re.finditer(pattern, codeContent, flags=re.MULTILINE | re.DOTALL)
        )

        if matches:

            lineRanges = []

            for match in matches:

                startLine = codeContent.count("\n", 0, match.start()) + 1
                endLine = codeContent.count("\n", 0, match.end()) + 1

                if startLine == endLine:

                    lineRanges.append(f"{startLine}")

                else:

                    lineRanges.append(f"{startLine}-{endLine}")

            logging.debug("Removing compiler DEBUG section.")
            logging.debug(f"    Lines affected: {', '.join(lineRanges)}.")

    pattern = r"(?s)(#ifdef DEBUG.*?#endif\n)"

    LogAffectedLines(pattern)
    codeContent = re.sub(pattern, r"", codeContent, flags=re.MULTILINE)

    with open(filePath, "w") as file:

        logging.info(f"File '{filePath}' has been formatted successfully.")
        file.write(codeContent)


if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("Usage: python RemoveCompilerDEBUG.py <filePath>")
        print(f"Received arguments: {sys.argv}")

        sys.exit(1)

    FormatNewlines(sys.argv[1])
