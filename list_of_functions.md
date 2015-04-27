## Files, functions, and classes/methods in directory "."

**Date**: 2015-04-27 17:46:22.

### File: ./docstring_page.py

 1. **path**: `./docstring_page.py`
 > None

 1. **path**: `./docstring_page.py.Page.__init__`
 > None

 1. **path**: `./docstring_page.py.Page.list_nodes_and_docstrings`
 > Try to find class information in method.
 > 
 > Return tuple:
 > 
 >     (path, list of sublists:
 > 
 >         [node-path-name, node-docstring]
 > 
 >     )

 1. **path**: `./docstring_page.py.Page.format_markdown`
 > Format file_sequence as Markdown file.
 > 
 > Object file_sequence is list of tuples.
 > Each tuple contains a path and a list of sub-lists.
 > Sub-lists contain a node name (incorporating path) and docstring.

 1. **path**: `./docstring_page.py.Page.gather_node_sequence`
 > Parse file-contents and assign nodes to appropriate list.

 1. **path**: `./docstring_page.py.Page.collect_docstrings`
 > Collect list of paths + classes + methods/functions, and docstrings.
 > 
 > This function assumes that there are no classes or methods/functions
 > nested within others.

 1. **path**: `./docstring_page.py.main`
 > List all docstrings in Python files in a directory.
 > 
 > `tests_only=True` reports only
 > 
 >  * functions/methods whose names begin `test_`
 >  * in files whose names begin `test_`



[end]