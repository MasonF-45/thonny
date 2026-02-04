import os
import time
from thonny import get_workbench

def log_current_program():
    editor = get_workbench().get_editor_notebook().get_current_editor()
    if editor is None:
        return

    source = editor.get_code_view().get_text()

    logs_dir = os.path.join(get_workbench().get_thonny_user_dir(), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"run_{timestamp}.py"
    filepath = os.path.join(logs_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(source)

    print("LOGGED PROGRAM TO:", filepath)

def patch_start_runner(event=None):
    wb = get_workbench()

    # This is the function your Run button actually calls
    original = wb._start_runner

    def wrapped_start_runner(*args, **kwargs):
        log_current_program()
        return original(*args, **kwargs)

    wb._start_runner = wrapped_start_runner
    print("RUN LOGGER PATCHED _start_runner SUCCESSFULLY")

def load_plugin():
    print("RUN LOGGER LOADED")
    get_workbench().bind("WorkbenchReady", patch_start_runner, True)
