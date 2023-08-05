# docpy

This package auto-generates Markdown documentation from Python files.

## Installation

This package is installed using pip:

```
pip install docpy
```

## Usage

This package is used from the command line:

```
docpy ...
```

The package help entry is given below.

```
usage: docpy [-h] [-a APPEND] [-o OUT] [-s SUB] [-t TEMP] ...

generate Markdown documentation for Python files

positional arguments:
  files                 files to be documented

optional arguments:
  -h, --help            show this help message and exit
  -a APPEND, --append APPEND
                        file to which to append generated Markdown
  -o OUT, --output OUT  file to save generated Markdown to
  -s SUB, --sub SUB     file with ::DOCUMENTATION:: tag to replace Markdown
  -t TEMP, --template TEMP
                        template file with ::DOCUMENTATION:: tag, needs OUT
                        argument
```

## Changelog

**v0.1.0:**

* Initial release