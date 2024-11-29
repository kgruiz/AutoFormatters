import logging
import os
import re
import sys
from typing import List, Union


class CodeSection:
    def __init__(self, indentedLine: str, parent: "CodeSection" = None):
        self.children: List["CodeSection"] = []
        self.level: int = len(indentedLine) - len(indentedLine.lstrip())
        self.text: str = indentedLine.strip()
        self.parent: "CodeSection" = parent

    def AddChildren(self, nodes: List["CodeSection"]):
        if not nodes:
            return
        childLevel = nodes[0].level
        while nodes:
            node = nodes[0]
            if node.level < self.level:
                # Node belongs to a higher level; let the parent handle it
                return
            elif node.level == childLevel:
                self.children.append(nodes.pop(0))
            elif node.level > childLevel:
                if not self.children:
                    raise Exception("Cannot add child to a node without a parent.")
                self.children[-1].AddChildren(nodes)
            else:
                # node.level < childLevel
                return

    def AsDict(self) -> Union[dict, str]:
        if len(self.children) > 1:
            return {self.text: [child.AsDict() for child in self.children]}
        elif len(self.children) == 1:
            return {self.text: self.children[0].AsDict()}
        else:
            return self.text


def PrintTree(section: CodeSection, indent: int = 0):
    print(" " * indent + section.text)
    for child in section.children:
        PrintTree(child, indent + 4)


def FormatNewlines(filePath):

    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

    if not os.path.isfile(filePath):

        logging.error(f"File not found - {filePath}")
        sys.exit(1)

    with open(filePath, "r") as file:

        codeContent = file.read()

    def LogAffectedLines(pattern, description):

        matches = list(
            re.finditer(pattern, codeContent, flags=re.MULTILINE | re.DOTALL)
        )

        if matches:

            lineNumbers = sorted(
                set(codeContent.count("\n", 0, match.start()) + 1 for match in matches)
            )

            logging.debug(f"Applying pattern for {description}: {pattern}")
            logging.debug(f"    Lines affected: {lineNumbers}")

    patternClassDocstring = r"(\bclass\s+\w+.*:)(\n\s*\"\"\")"
    LogAffectedLines(patternClassDocstring, "Class declaration followed by docstring")
    codeContent = re.sub(patternClassDocstring, r"\1\2", codeContent)

    splitLines = codeContent.splitlines()

    nodes = []
    prevLevel = 0
    for line in codeContent.strip().splitlines():
        if line.strip():
            node = CodeSection(line)
            prevLevel = node.level
        else:
            node = CodeSection(" " * prevLevel)
        nodes.append(node)

    # Create root section
    root = CodeSection("root")

    # Build the tree
    root.AddChildren(nodes)

    # Convert the tree to a dictionary
    treeDict = root.AsDict()["root"]
    print("Tree as Dictionary:")
    print(treeDict)

    print("\nVisual Representation:")
    PrintTree(root)

    insertLineAfterKeywords = [
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

    patternTrailingNewlines = r"\n+$"

    if re.search(patternTrailingNewlines, codeContent):

        logging.debug("Removed trailing blank lines at the end of the file.")

    codeContent = re.sub(patternTrailingNewlines, "\n", codeContent)

    with open(filePath, "w") as file:

        file.write(codeContent)


if __name__ == "__main__":

    filePath = os.path.abspath(__file__)

    # if len(sys.argv) != 2:

    #     print("Usage: python PythonSpaceLines.py <filePath>")
    #     print(f"Received arguments: {sys.argv}")
    #     sys.exit(1)

    # FormatNewlines(sys.argv[1])

    FormatNewlines(filePath)
