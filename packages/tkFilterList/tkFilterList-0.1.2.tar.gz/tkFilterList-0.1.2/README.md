**tkFilterList** is a combination of the Tkinter Listbox and Entry widgets that updates to display matching items as you type.


## Usage

tkFilterList consists of a single module, `tkfilterlist` (note the module name is lowercase), which exports a single class, `FilterList`.

A brief example program:

```python
#!/usr/bin/env python3

from tkinter import *
from tkinter.messagebox import showinfo
from tkfilterlist import FilterList
import operator

# Source items for the FilterList
# Format: display_text, symbol, operator
source = [("Addition", "+", operator.add),
          ("Subtraction", "-", operator.sub),
          ("Multiplication", "*", operator.mul),
          ("Division", "/", operator.floordiv)]

# Create a root window
root = Tk()

# Create a FilterList widget
fl = FilterList(root,
                source=source,
                display_rule=lambda item: item[0],
                filter_rule=lambda item, text:
                            item[0].lower().startswith(text.lower()))
fl.pack(side="top", expand=1, fill="both")

def show_result(event=None):
    a, b = 42, 7
    item = fl.selection()
    if item:
        showinfo("Result",
                 "{0} {1} {2} = {3}".format(a, item[1], b, item[2](a, b)),
                 parent=root)

# Show the result of the calculation on Return or double-click
fl.bind("<Return>", show_result)
fl.bind("<Double-Button-1>", show_result)

# Focus on the FilterList widget
fl.focus_set()

# Start Tk's event loop
root.mainloop()
```

For detailed documentation, try `python -m pydoc tkfilterlist`.


## Customization

You can customize the item display and filtering behavior by setting its `display_rule` and `filter_rule` options, respectively, to your own custom functions. This allows tkFilterList to process lists containing complex datatypes, including nested lists, tuples, and even entire classes. The functions are defined as follows:

Function | Description
-------- | -----------
`display_rule(item)` | Returns the display text for the specified `item`.
`filter_rule(item, text)` | Returns `True` if the `text` argument matches the specified `item`, `False` otherwise.

The default display rule is available as `FilterList.default_display_rule`. It returns the string value of `item`, matching the behavior of a standard Listbox widget.

The default filter rule is available as `FilterList.default_filter_rule`. It returns `True` if an `item` starts with the specified `text` using a case-insensitive match.
