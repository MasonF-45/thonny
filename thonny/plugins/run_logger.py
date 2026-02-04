from thonny import get_workbench

def walk(widget, indent=0):
    pad = " " * indent
    print(f"{pad}{widget}  ->  {widget.winfo_class()}")
    for child in widget.children.values():
        walk(child, indent + 2)

def show_toolbar_tree(event=None):
    wb = get_workbench()
    tb = wb.get_toolbar()
    print("\n=== FULL TOOLBAR WIDGET TREE ===")
    walk(tb)

def load_plugin():
    print("TOOLBAR PROBE 2 LOADED")
    get_workbench().bind("WorkbenchReady", show_toolbar_tree, True)
