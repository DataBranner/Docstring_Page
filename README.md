## Docstring_Page

Python 3 program to prepare a Markdown page containing the names of all files, functions, classes, and methods and their Python docstrings. Such a page is suitable for immediate commital to a repository and display on GitHub.

This is not intended to replace more elaborate documentation tools such as Sphinx, but to provide a quick way to summarize the contents of test suites for reporting purposes.

Run as

    python docstring_page.py <directory>

All files in the optional `directory` will be indexed; this value defaults to the present working directory.

By default, only files and functions/methods beginning with `test_` will be treated; to treat all files and functions, run from an interpreter as

    import docstring_page
    docstring_page.main(tests_only=False)

This repository contains a sample file `list_of_functions.md` showing the output for this program itself.

[end]
