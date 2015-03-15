#! /usr/bin/env python
# docstring_page.py
# 20150314
# David Branner

import os
import ast
import re
import sys
import datetime

class Page():
    def __init__(self, directory, tests_only=True):
        self.tests_only = tests_only
        self.directory = directory
        self.node_sequence = None

    def list_nodes_and_docstrings(self):
        """Try to find class information in method.
        
        Return tuple: 
            (path, list of sublists:
                [node-path-name, node-docstring]
            )
        """
        self.file_sequence = []
        for filename in os.listdir(self.directory):
            if filename[-3:] == '.py':
                if self.tests_only and filename[:5] != 'test_':
                    continue
                self.path = os.path.join(self.directory, filename)
                with open(self.path, 'r') as f:
                    self.contents = f.read()
                self.gather_node_sequence()
                self.file_sequence.append((self.path, self.node_sequence))
    
    def format_markdown(self):
        """Format file_sequence as Markdown file.
        
        Object file_sequence is list of tuples.
        Each tuple contains a path and a list of sub-lists.
        Sub-lists contain a node name (incorporating path) and docstring.
        """
        # Make page-header.
        current_datetime = datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S')
        page_header = (
                '## Files, functions, and classes/methods in directory "{}"'
                '\n\n**Date**: {}.'.
                format(self.directory, current_datetime))
        # Iterate through tuples.
        report_for_all_files = [[]]
        initial_report = [[]]
        for file_tuple in self.file_sequence:
            # Top-level file_tuple[0] becomes first-level header, has path.
            first_level_header = '### File: {}'.format(file_tuple[0])
            # For each element of list file_tuple[1],
            # add name to numbered list and follow with docstring as quote.
            # Docstrings containing \n must be formatted for multiline quote.
            numbered_items = []
            for item in file_tuple[1]:
                if item[1]:
                    item[1] = re.sub(r'\n', r'\n > ', item[1])
                numbered_items.append(
                    ' 1. **path**: {}\n > {}'.format(item[0], item[1])
                    )
            numbered_items = '\n\n'.join(numbered_items)
            report_for_one_file = '\n\n'.join(
                    [first_level_header, numbered_items])
            report_for_all_files.append(report_for_one_file)
        if report_for_all_files == initial_report:
            page_header +=(
                    '\n\nNo docstrings were found in the `.py` files '
                    'in this directory.')
        elif self.tests_only:
            page_header += (
                '\n\nFull paths and docstrings are populated below.'
                '\n\n"None" indicates no docstring found.'
                '\n\nOnly files and functions/methods beginning '
                '`test_` are included here.')
        report_for_all_files[0] = page_header
        report_for_all_files.append('\n\n[end]')
        # Concatenate page-items and return page.
        return '\n\n'.join(report_for_all_files)
    
    def gather_node_sequence(self):
        """Parse file-contents and assign nodes to appropriate list."""
        self.module = ast.parse(self.contents)
        self.class_defs = []
        self.func_defs = []
        for node in self.module.body:
            if isinstance(node, ast.ClassDef):
                self.class_defs.append(node)
            if isinstance(node, ast.FunctionDef):
                self.func_defs.append(node)
        self.collect_docstrings()    
    
    def collect_docstrings(self):
        """Collect list of paths + classes + methods/functions, and docstrings.
        
        This function assumes that there are no classes or methods/functions
        nested within others.
        """
        self.node_sequence = []
        # Module-level docstrings.
        self.node_sequence.append([self.path, ast.get_docstring(self.module)])
        # Class-level doc-strings
        # Function-level doc-strings
        for class_def in self.class_defs:
            for node in class_def.body:
                if isinstance(node, ast.ClassDef):
                    self.node_sequence.append(
                            [self.path + '.' + node.name,
                             ast.get_docstring(node)]
                            )
                elif isinstance(node, ast.FunctionDef):
                    if self.tests_only and node.name[:5] != 'test_':
                        continue
                    self.node_sequence.append(
                            [self.path + '.' + class_def.name + '.' + node.name,
                             ast.get_docstring(node)]
                            )
        for func_def in self.func_defs:
            if isinstance(func_def, ast.FunctionDef):
                if self.tests_only and func_def.name[:5] != 'test_':
                    continue
                self.node_sequence.append(
                        [self.path + '.' + func_def.name,
                         ast.get_docstring(func_def)]
                        )
    
def main(argv=None, directory='.', tests_only=True):
    """List all docstrings in Python files in a directory.
    
    `tests_only=True` reports only 
    
     * functions/methods whose names begin `test_`
     * in files whose names begin `test_`
    """
    print('Run from top-level directory as\n\n'
        '    python docstring_page.py tests\n\n'
        'Output file will be saved to specified directory (here "tests").')
    if len(argv) > 1:
        directory = argv[1]
    p = Page(directory, tests_only)
    p.list_nodes_and_docstrings()
    md_content = p.format_markdown()
    path = os.path.join(directory, 'list_of_functions.md')
    with open(path, 'w') as f:
        f.write(md_content)
    print('\nFile {} saved.'.format(path))

if __name__ == '__main__':
    main(sys.argv)