# Code Formatter & Cleaner Suite

This is a collection of Python scripts and configuration files designed to help you maintain clean, well-formatted C++ and Python codebases. This collection automates the process of formatting code according to best practices, along with some personal adjustments, ensuring consistency and readability across your projects.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [CppSpaceLines.py](#cppspacelinespy)
  - [PythonSpaceLines.py](#pythonspacelinespy)
  - [RemoveCompilerDEBUG.py](#removecompilerdebugpy)
  - [.clang-format](#clang-format)
- [Configuration](#configuration)
- [Logging](#logging)
- [License](#license)

## Features

- **C++ Code Formatting:** Automatically adds appropriate newlines after classes, structs, namespaces, functions, and control flow statements to enhance readability.
- **Python Code Formatting:** Ensures proper spacing after class and function declarations, docstrings, and control flow keywords.
- **Debug Code Removal:** Removes all code sections wrapped within `#ifdef DEBUG` and `#endif` directives in C++ files.
- **Custom Clang-Format Configuration:** Provides a `.clang-format` file tailored to enforce specific coding styles based on the Google C++ style guide with custom adjustments.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/code-formatter-cleaner-suite.git
   cd code-formatter-cleaner-suite
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   The scripts rely on Python's standard library, so no additional packages are required.

## Usage

Each script is designed to be run from the command line, taking the target file path as an argument.

### CppSpaceLines.py

**Description:** Formats C++ source files by adding newlines after specific code constructs such as classes, structs, namespaces, functions, and control flow statements.

**Usage:**

```bash
python CppSpaceLines.py <filePath>
```

**Example:**

```bash
python CppSpaceLines.py src/main.cpp
```

### PythonSpaceLines.py

**Description:** Formats Python source files by adding newlines after class and function declarations, docstrings, and control flow keywords to improve code readability.

**Usage:**

```bash
python PythonSpaceLines.py <filePath>
```

**Example:**

```bash
python PythonSpaceLines.py scripts/utils.py
```

### RemoveCompilerDEBUG.py

**Description:** Removes all sections of C++ code enclosed within `#ifdef DEBUG` and `#endif` directives, including the content within these blocks.

**Usage:**

```bash
python RemoveCompilerDEBUG.py <filePath>
```

**Example:**

```bash
python RemoveCompilerDEBUG.py src/debug.cpp
```

> **Note:** The regex pattern for removing debug sections is yet to be implemented. Ensure to define the appropriate pattern in the script before usage.

### .clang-format

**Description:** A configuration file for `clang-format` to enforce a consistent C++ coding style based on the Google style guide with customized settings.

**Usage:**

1. **Install clang-format**

   ```bash
   # On macOS
   brew install clang-format

   # On Ubuntu
   sudo apt-get install clang-format

   # On Windows
   choco install clang-format
   ```

2. **Format Your C++ Files**

   ```bash
   clang-format -i <filePath>
   ```

   **Example:**

   ```bash
   clang-format -i src/main.cpp
   ```

   The provided `.clang-format` file will be automatically detected and applied.

## Configuration

The `.clang-format` file included in this repository is pre-configured with the following settings:

```yaml
Language: Cpp
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 90
AccessModifierOffset: 0
AlignAfterOpenBracket: Align
AlignConsecutiveAssignments: false
AlignConsecutiveDeclarations: false
AlignEscapedNewlinesLeft: true
AlignOperands: true
AlignTrailingComments: true
AllowAllParametersOfDeclarationOnNextLine: false
AllowShortBlocksOnASingleLine: false
AllowShortCaseLabelsOnASingleLine: false
AllowShortFunctionsOnASingleLine: None
AllowShortIfStatementsOnASingleLine: false
AllowShortLoopsOnASingleLine: false
AlwaysBreakAfterDefinitionReturnType: None
AlwaysBreakAfterReturnType: None
AlwaysBreakBeforeMultilineStrings: false
AlwaysBreakTemplateDeclarations: true
EmptyLineAfterAccessModifier: Always
EmptyLineBeforeAccessModifier: Always
FixNamespaceComments: true
IncludeBlocks: Regroup
IndentCaseLabels: true
InsertBraces: true
NamespaceIndentation: All
PackConstructorInitializers: NextLineOnly
ReferenceAlignment: Right
RemoveParentheses: MultipleParentheses
SeparateDefinitionBlocks: Always
SortIncludes: CaseSensitive
SpaceAfterCStyleCast: false
SortUsingDeclarations: LexicographicNumeric
SpaceBeforeAssignmentOperators: true
PointerAlignment: Right
SpaceBeforeParens: Custom
SpaceBeforeParensOptions:
    AfterControlStatements: true
    AfterFunctionDefinitionName: false
    AfterForeachMacros: true
    AfterFunctionDeclarationName: false
    AfterIfMacros: true
    AfterOverloadedOperator: false
    AfterPlacementOperator: true
    AfterRequiresInClause: true
    AfterRequiresInExpression: true
SpaceBeforeSquareBrackets: false
SpaceBeforeRangeBasedForLoopColon: true
SpaceInEmptyBlock: false
KeepEmptyLines:
  AtEndOfFile: false
  AtStartOfBlock: true
  AtStartOfFile: false
IndentPPDirectives: BeforeHash
```

Feel free to customize this file to better suit your project's coding standards.

## Logging

All scripts are equipped with logging functionality to provide detailed information about the formatting process. Logs include:

- **Debug Messages:** Information about which patterns are being applied and the lines affected.
- **Error Messages:** Alerts when the specified file is not found or incorrect usage is detected.
- **Info Messages:** Confirmation upon successful formatting.

Logs are output to the console. You can adjust the logging level by modifying the `logging.basicConfig` level in each script.

---
