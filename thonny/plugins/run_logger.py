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

def load_plugin():
    print("RUN LOGGER LOADED")

    wb = get_workbench()

    # Save original run function
    original_run = wb._cmd_run_current_script

    # Define wrapper
    def wrapped_run():
        log_current_program()
        return original_run()

    # Replace Thonny's run command with our wrapped version
    wb._cmd_run_current_script = wrapped_run
