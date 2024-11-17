# simple-file-org

A very simple tool to organize files into folders based on creation times.

## Usage

```bash
simple-file-org --help

Usage: simple-file-org [OPTIONS] SOURCE TARGET

Organizes files in the specified folder by year and date.
Args:     source (Path): The folder path where the files will be read from.     target (Path): The folder path where the files will be moved to.
Returns:     None

╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    source      DIRECTORY  The source directory where the files will be read from. [default: None] [required]                                                                                                                                                                                                                                                         │
│ *    target      DIRECTORY  The target directory where the files will be moved to. [default: None] [required]                                                                                                                                                                                                                                                          │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                                                                                                                                                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Installation

```bash
pip install simple-file-org
```

## Development

If you want to develop on this project, you can use the following instructions to setup your development environment.

### Requirements

- `rye 0.40.0+`

### Setup

```bash
rye sync
```

### Unit Tests

```bash
rye run unit
```
