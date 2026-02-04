from thonny import get_workbench

def probe(event=None):
    wb = get_workbench()
    runner = wb._runner

    print("\n=== RUNNER METHODS ===")
    for name in dir(runner):
        if "run" in name.lower():
            print(name)

def load_plugin():
    print("RUNNER PROBE LOADED")
    get_workbench().bind("WorkbenchReady", probe, True)
