import logging
import os
import re
import sys
from json import dump, dumps
from typing import List, Union


class CodeSection:
    def __init__(self, indentedLine: str, parent: "CodeSection" = None):
        self.children: List["CodeSection"] = []
        self.text: str = indentedLine.strip()
        if self.text in {"]", "}", ")"}:
            self.level = len(indentedLine) - len(indentedLine.lstrip())
        else:
            self.level: int = len(indentedLine) - len(indentedLine.lstrip())
        self.parent: "CodeSection" = parent
        self.prev: "CodeSection" = None

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
                child = nodes.pop(0)
                child.parent = self
                self.children.append(child)
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

    def FindNearestCommonAncestor(
        node1: "CodeSection", node2: "CodeSection"
    ) -> Union["CodeSection", None]:

        ancestors1 = set()
        current = node1
        while current:
            ancestors1.add(current)
            current = current.parent

        current = node2
        while current:
            if current in ancestors1:
                return current
            current = current.parent
        return None


def PrintTree(section: CodeSection, indent: int = 0):

    if section.text.strip() != "":

        print(f"{" " * indent}{section.text} (Level {section.level})")

    else:

        print()

    for child in section.children:

        PrintTree(child, indent + 4)


def TraverseTree(section: CodeSection):

    if section.prev and (
        section.text.strip() == ")"
        or section.text.strip() == "]"
        or section.text.strip() == "}"
    ):

        section.level = section.prev.level

        if section.parent:

            section.parent.children.remove(section)

        section.parent = section.prev.parent

        if section.parent:

            section.parent.children.append(section)

    for child in section.children:

        TraverseTree(child)


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
    previousNode = None
    prevLevel = 0
    for line in codeContent.strip().splitlines():
        if line.strip():
            node = CodeSection(line)
            node.prev = previousNode
            previousNode = node
            prevLevel = node.level
        else:
            node = CodeSection(" " * prevLevel)
            node.prev = previousNode
        nodes.append(node)

    # Create root section
    root = CodeSection("root")

    # Build the tree
    root.AddChildren(nodes)

    TraverseTree(root)

    # Convert the tree to a dictionary
    treeDict = root.AsDict()["root"]
    # print("Tree as Dictionary:")
    # print(dumps(treeDict, indent=4))

    # with open("out.json", "w") as file:

    #     dump(
    #         treeDict,
    #         file,
    #         indent=2,
    #     )

    # print("\nVisual Representation:")
    # PrintTree(root)

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
