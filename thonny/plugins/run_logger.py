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

def patch_run_button(event=None):
    wb = get_workbench()

    # Find the Run button in the toolbar
    run_button = wb.get_toolbar().children.get("run_button")
    if not run_button:
        print("Run button not found")
        return

    original = run_button["command"]

    def wrapped():
        log_current_program()
        return original()

    run_button.config(command=wrapped)
    print("RUN LOGGER PATCHED RUN BUTTON SUCCESSFULLY")

def load_plugin():
    print("RUN LOGGER LOADED")
    get_workbench().bind("WorkbenchReady", patch_run_button, True)
