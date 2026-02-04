from thonny import get_workbench

def show_toolbar_children(event=None):
    wb = get_workbench()
    tb = wb.get_toolbar()
    print("\n=== TOOLBAR CHILDREN ===")
    for name, widget in tb.children.items():
        print(name, "->", widget)

def load_plugin():
    print("TOOLBAR PROBE LOADED")
    get_workbench().bind("WorkbenchReady", show_toolbar_children, True)

