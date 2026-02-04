from thonny import get_workbench

def walk(widget, indent=0):
    pad = " " * indent
    cls = widget.winfo_class()
    print(f"{pad}{widget} -> {cls}")

    # If this is a customtoolbutton, inspect its label
    if "customtoolbutton" in str(widget):
        for child in widget.children.values():
            if child.winfo_class() == "Label":
                print(f"{pad}  LABEL TEXT: {child.cget('text')}")
                print(f"{pad}  LABEL IMAGE: {child.cget('image')}")

    for child in widget.children.values():
        walk(child, indent + 2)

def show_toolbar_tree(event=None):
    wb = get_workbench()
    tb = wb.get_toolbar()
    print("\n=== FINDING RUN BUTTON ===")
    walk(tb)

def load_plugin():
    print("RUN BUTTON FINDER LOADED")
    get_workbench().bind("WorkbenchReady", show_toolbar_tree, True)
