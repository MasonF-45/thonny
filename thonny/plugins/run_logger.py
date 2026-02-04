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
    tb = wb.get_toolbar()

    # The Run button label you identified
    run_label = tb.nametowidget(".!frame.!frame.!frame2.!customtoolbutton.!label")

    # Get existing click binding
    original = run_label.bind("<Button-1>")

    def wrapped(event):
        log_current_program()
        if original:
            return original(event)

    run_label.bind("<Button-1>", wrapped)

    print("RUN LOGGER PATCHED RUN LABEL SUCCESSFULLY")

def load_plugin():
    print("RUN LOGGER LOADED")
    get_workbench().bind("WorkbenchReady", patch_run_button, True)

