# thonny_log_runs.py
import os
import datetime
from thonny import get_workbench, get_thonny_user_dir


def _ensure_logs_dir() -> str:
    logs_dir = os.path.join(get_thonny_user_dir(), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    return logs_dir


def _get_current_source():
    wb = get_workbench()
    editor = wb.get_editor_notebook().get_current_editor()
    if editor is None:
        return None, None

    # Try to get a reasonable base name for the file
    filename = editor.get_filename() or "untitled.py"
    base = os.path.basename(filename)

    # Editor exposes its code via the code view
    try:
        source = editor.get_code_view().get_content()
    except Exception:
        # Fallback if API changes
        text = editor.get_text_widget()
        source = text.get("1.0", "end-1c")

    return base, source


def _log_current_program(event):
    # Only react to successful Run commands
    if getattr(event, "denied", False):
        return

    # Main run commands in Thonny
    if event.command_id not in (
        "run_current_script",
        "run_current_script_in_terminal",
        "run_current_script_custom",
    ):
        return

    base, source = _get_current_source()
    if source is None:
        return

    logs_dir = _ensure_logs_dir()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    log_name = f"{timestamp}_{base}"
    log_path = os.path.join(logs_dir, log_name)

    try:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(source)
    except Exception:
        # Don't break the run if logging fails
        pass


def load_plugin():
    wb = get_workbench()
    # Listen for all UI commands; filter to Run in handler
    wb.bind("UICommandDispatched", _log_current_program, True)

