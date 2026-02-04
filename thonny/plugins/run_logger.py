from thonny import get_workbench

def probe(event=None):
    wb = get_workbench()
    print("\n=== WORKBENCH ATTRIBUTES ===")
    for name in dir(wb):
        if "run" in name.lower():
            print(name)

def load_plugin():
    print("RUN PROBE LOADED")
    get_workbench().bind("WorkbenchReady", probe, True)
