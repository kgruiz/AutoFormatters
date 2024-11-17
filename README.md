# Code Formatter & Cleaner Collection

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
- [Integration with VSCode](#integration-with-vscode)
  - [1. Install Extensions](#1-install-extensions)
  - [2. Configure `settings.json`](#2-configure-settingsjson)
  - [3. Set Up Keybindings](#3-set-up-keybindings)
  - [4. Specify the Python Interpreter Path (Optional)](#4-specify-the-python-interpreter-path-optional)
- [Warning](#warning)

## Features

- **C++ Code Formatting:** Automatically adds appropriate newlines after classes, structs, namespaces, functions, and control flow statements to enhance readability.
- **Python Code Formatting:** Ensures proper spacing after class and function declarations, docstrings, and control flow keywords.
- **Debug Code Removal:** Removes all code sections wrapped within `#ifdef DEBUG` and `#endif` directives in C++ files.
- **Debug Code Insertion:** Quickly inserts `#ifdef DEBUG` and `#endif` preprocessor directives to wrap debug-specific code blocks in C++ files.
- **Custom Clang-Format Configuration:** Provides a `.clang-format` file tailored to enforce specific coding styles based on the Google C++ style guide with custom adjustments.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/code-formatter-cleaner-collection.git
   cd code-formatter-cleaner-collection
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

### .clang-format

**Description:** A configuration file for `clang-format` to enforce a consistent C++ coding style based on the Google style guide with customized settings.

**Summary:** The `.clang-format` file sets indentation, line length, brace style, and other formatting rules to maintain code consistency.

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

The `.clang-format` file included in this repository is pre-configured with settings based on the Google C++ style guide, including custom adjustments for indentation, line length, brace placement, and more. Feel free to customize this file to better suit your project's coding standards.

## Logging

All scripts are equipped with logging functionality to provide detailed information about the formatting process. Logs include:

- **Debug Messages:** Information about which patterns are being applied and the lines affected.
- **Error Messages:** Alerts when the specified file is not found or incorrect usage is detected.
- **Info Messages:** Confirmation upon successful formatting.

Logs are output to the console. You can adjust the logging level by modifying the `logging.basicConfig` level in each script.

## Integration with VSCode

Integrate the **Code Formatter & Cleaner Collection** with Visual Studio Code (VSCode) to automate code formatting and cleaning.

### 1. Install Extensions

- **Run on Save** by emeraldwalk:
  - Open VSCode.
  - Go to the Extensions Marketplace (`Ctrl+Shift+X` or `Cmd+Shift+X`).
  - Search for "Run on Save" by emeraldwalk and install it.

- **Clang-Format** by Xaver Hellauer:
  - Search for "Clang-Format" by Xaver Hellauer and install it.

- **Black Formatter** for Python:
  - Install the **Black** extension by searching "Black Formatter" in the Extensions Marketplace.

- **Multi Command** by ryuta46:
  - Install the **multi-command** extension to allow defining and executing multiple commands via a single keybinding.

### 2. Configure `settings.json`

Open your `settings.json` in VSCode and add the following configurations:

```yaml
{
    # Set Clang-Format as the default formatter for C++
    "editor.defaultFormatter": "xaver.clang-format",
    "clang-format.style": "file:/path/to/.clang-format",

    # Configure Run on Save for Python and C++ scripts
    "emeraldwalk.runonsave": {
        "commands": [
            {
                "match": "\\.(cpp|h|hpp)$",
                "isAsync": true,
                "cmd": "python /path/to/CppSpaceLines.py ${file}"
            },
            {
                "match": "\\.py$",
                "isAsync": true,
                "cmd": "python /path/to/PythonSpaceLines.py ${file}"
            },
            {
                "match": "\\.(cpp|h|hpp)$",
                "isAsync": true,
                "cmd": "python /path/to/RemoveCompilerDEBUG.py ${file}"
            }
        ]
    },

    # Enable Black formatter for Python
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,

    # Configure multiCommand sequences
    "multiCommand.commands": [
        {
            "command": "multiCommand.RemoveAllCompilerDEBUG",
            "sequence": [
                {
                    "command": "command-runner.run",
                    "args": {
                        "command": "clear && /Users/kadengruizenga/anaconda3/envs/basic/bin/python -u /opt/homebrew/Cellar/clang-format/19.1.1/RemoveCompilerDEBUG.py \"${file}\""
                    }
                }
            ]
        },
        {
            "command": "multiCommand.CPPifdefDEBUG",
            "sequence": [
                "editor.action.insertLineAfter",
                {
                    "command": "type",
                    "args": {
                        "text": "\n#ifdef DEBUG\n#endif"
                    }
                },
                "cursorUp",
                "cursorEnd",
                "editor.action.insertLineAfter"
            ]
        }
    ]
}
```

**Note:** Replace `/path/to/` with the actual paths to your scripts and ensure the Python interpreter path is correct.

### 3. Set Up Keybindings

To streamline the usage of your scripts, set up custom keybindings in VSCode.

1. **Open `keybindings.json`:**

   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to open the Command Palette.
   - Type `Preferences: Open Keyboard Shortcuts (JSON)` and select it.

2. **Add the Following Keybindings:**

   ```yaml
   [
       {
           "key": "alt+shift+d",
           "command": "extension.multiCommand.execute",
           "args": { "command": "multiCommand.RemoveAllCompilerDEBUG" },
           "when": "(resourceExtname == .hpp || resourceExtname == .h || resourceExtname == .cpp) && editorTextFocus"
       },
       {
           "key": "alt+shift+i",
           "command": "extension.multiCommand.execute",
           "args": { "command": "multiCommand.CPPifdefDEBUG" },
           "when": "(resourceExtname == .hpp || resourceExtname == .h || resourceExtname == .cpp) && editorTextFocus"
       }
   ]
   ```

   - **`Alt+Shift+D`:** Executes the `RemoveAllCompilerDEBUG` command, which runs the `RemoveCompilerDEBUG.py` script on the current C++ file to remove debug sections.
   - **`Alt+Shift+I`:** Executes the `CPPifdefDEBUG` command, which inserts `#ifdef DEBUG` and `#endif` preprocessor directives into the current C++ file to wrap debug-specific code blocks.

### 4. Specify the Python Interpreter Path (Optional)

If your Python interpreter or virtual environment is located outside the workspace folder, update the `cmd` field with the absolute path to the Python executable.

**Example for a Virtual Environment:**

```ymal
{
    "emeraldwalk.runonsave": {
        "commands": [
            {
                "match": "\\.(cpp|h|hpp)$",
                "isAsync": true,
                "cmd": "/absolute/path/to/venv/bin/python /absolute/path/to/CppSpaceLines.py ${file}" # macOS/Linux
                # "cmd": "C:\\absolute\\path\\to\\venv\\Scripts\\python.exe C:\\absolute\\path\\to\\CppSpaceLines.py ${file}" # Windows
            }
        ]
    }
}
```

> **Tips:**
>
> - **Windows Paths:** Use double backslashes (`\\`) or forward slashes (`/`).
> - **macOS/Linux Paths:** Use forward slashes (`/`).
> - **Environment Variables:** If Python is added to your system's PATH, you can use `python` instead of the full path.

## Warning

**Use caution when using Python scripts to modify file formatting.** There is a risk of glitches or crashes that may result in lost or corrupted code. Always ensure you have backups or version control in place before enabling automated formatting.
