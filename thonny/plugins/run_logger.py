# run_logger.py
import os
import datetime
from thonny import get_workbench, get_runner, get_thonny_user_dir


def _ensure_logs_dir():
    logs = os.path.join(get_thonny_user_dir(), "logs")
    os.makedirs(logs, exist_ok=True)
    return logs


def _get_editor_source():
    wb = get_workbench()
    editor = wb.get_editor_notebook().get_current_editor()
    if not editor:
        return None, None

    # filename for naming the log file
    name = editor.get_filename() or "untitled.py"
    base = os.path.basename(name)

    # safest way to get code across Thonny versions
    try:
        source = editor.get_code_view().get_content()
    except Exception:
        text = editor.get_text_widget()
        source = text.get("1.0", "end-1c")

    return base, source


def _patched_run(original_run_method):
    def wrapper(*args, **kwargs):
        # Log BEFORE running
        base, source = _get_editor_source()
        if source:
            logs = _ensure_logs_dir()
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            path = os.path.join(logs, f"{ts}_{base}")
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(source)
            except Exception:
                pass  # never break Run

        # Call the real run method
        return original_run_method(*args, **kwargs)

    return wrapper


def _install_patch(event=None):
    runner = get_runner()
    if not runner:
        return

    # Patch only once
    if hasattr(runner, "_run_logger_patched"):
        return

    original = runner._cmd_run_current_script
    runner._cmd_run_current_script = _patched_run(original)
    runner._run_logger_patched = True


def load_plugin():
    # Install patch AFTER Thonny is fully initialized
    get_workbench().bind("WorkbenchReady", _install_patch, True)


