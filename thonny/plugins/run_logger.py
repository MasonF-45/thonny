# run_logger.py
import os
import time
from thonny import get_workbench, get_runner
from thonny.misc_utils import get_thonny_user_dir


def _log_current_program():
    wb = get_workbench()
    editor = wb.get_editor_notebook().get_current_editor()
    if editor is None:
        return

    # Get the full in‑memory source code (works even if unsaved)
    try:
        source = editor.get_content(up_to_end=True)
    except Exception:
        return

    # Build logs directory
    logs_dir = os.path.join(get_thonny_user_dir(), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Determine a base name
    if editor.is_untitled():
        base = "untitled"
    else:
        path = editor.get_target_path()
        base = os.path.splitext(os.path.basename(path))[0] if path else "untitled"

    # Timestamped filename
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{base}_{timestamp}.py"

    # Full path
    full_path = os.path.join(logs_dir, filename)

    # Write the file
    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(source)
    except Exception:
        pass  # Never break Run if logging fails


def _install_patch(event=None):
    runner = get_runner()
    if runner is None:
        return

    # Prevent double‑patching
    if hasattr(runner, "_run_logger_patched"):
        return

    original = runner._cmd_run_current_script

    def wrapped_run(*args, **kwargs):
        _log_current_program()
        return original(*args, **kwargs)

    runner._cmd_run_current_script = wrapped_run
    runner._run_logger_patched = True


def load_plugin():
    # Patch AFTER Thonny is fully initialized
    get_workbench().bind("WorkbenchReady", _install_patch, True)
