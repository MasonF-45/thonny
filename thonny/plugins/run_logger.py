from thonny import get_workbench

def trace_runner(event=None):
    wb = get_workbench()
    runner = wb._runner

    print("\n=== TRACING RUNNER METHODS ===")
    for name in dir(runner):
        attr = getattr(runner, name)
        if callable(attr):
            def make_wrapper(n, fn):
                def wrapper(*args, **kwargs):
                    print(f"RUNNER METHOD CALLED: {n}")
                    return fn(*args, **kwargs)
                return wrapper

            setattr(runner, name, make_wrapper(name, attr))

    print("RUNNER TRACING ENABLED")

def load_plugin():
    print("RUN TRACE LOADED")
    get_workbench().bind("WorkbenchReady", trace_runner, True)
