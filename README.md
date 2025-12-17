# Unix Shell in Python

A Unix shell implemented from scratch in Python as part of the CodeCrafters “Build Your Own Shell” challenge.

The project focuses on understanding how real shells work, blending system design, advanced programming techniques, and core operating system concepts such as process management, pipes, and file descriptors.

The repository includes the original challenge scaffolding along with my complete shell implementation.

## Features

- Interactive shell prompt with a full REPL
- Shell parsing and tokenization of user input
- Built-in commands:
  - `echo`, `cd`, `pwd`, `type`, `exit`, `history`
- Process spawning and external command execution via `fork` + `execvp`
  - Executable lookup using `$PATH`
  - Environment variable support (e.g. `HISTFILE`)
- Pipelines (`|`) with proper file descriptor handling
- Output and error redirection:
  - `>`, `>>`, `1>`, `1>>`
  - `2>`, `2>>`
- Quoting and escaping:
  - Single quotes, double quotes, and backslash escaping
- Command history:
  - In-memory history using `readline` and persistent history via `HISTFILE`
  - History navigation via up/down arrow keys
  - Support for `history`, `history -r`, `history -w`, `history -a`
- Tab autocompletion for built-in commands and executables in `$PATH`

## How to Run

Clone the repository and run the shell using Python:

```bash
python3 app/main.py
```

## Key Concepts

- Process creation and management using `fork` and `execvp`
- Inter-process communication using pipes and file descriptors
- Shell parsing, tokenization, and command dispatch
- Managing in-memory vs persistent state (command history)
- Configuring shell behavior via environment variables

## Notes

This project is a learning-focused implementation of a Unix-like shell and is not intended to be a full replacement for `bash` or `zsh`.
