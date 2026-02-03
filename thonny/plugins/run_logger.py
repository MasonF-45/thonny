import os
import time
from thonny import get_workbench

def log_current_program(event=None):
    # Get the active editor
    editor = get_workbench().get_editor_notebook().get_current_editor()
    if editor is None:
        return

    # Get the full program text (even if unsaved)
    source = editor.get_code_view().get_text()

    # Create logs directory inside Thonny's user directory
    logs_dir = os.path.join(get_workbench().get_thonny_user_dir(), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Timestamped filename
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"run_{timestamp}.py"
    filepath = os.path.join(logs_dir, filename)

    # Write the program source to the file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(source)

def load_plugin():
    # Bind to Thonny's Run event
    get_workbench().bind("Run", log_current_program, True)
