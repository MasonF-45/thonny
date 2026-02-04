# run_logger.py
import os
import time
from typing import Optional

from thonny import get_workbench
from thonny.misc_utils import get_thonny_user_dir


def _get_current_editor():
    wb = get_workbench()
    nb = wb.get_editor_notebook()
    if nb is None:
        return None
    return nb.get_current_editor()


def _sanitize_filename(name: str) -> str:
    # Remove characters that are illegal in filenames on common OSes
    bad_chars = r'\/:*?"<>|'
    return "".join(c for c in name if c not in bad_chars)


def _log_current_program(event=None) -> None:
    editor = _get_current_editor()
    if editor is None:
        return

    # Get full source code from the current editor
    try:
        source = editor.get_content(up_to_end=True)
    except Exception:
        return

    # Base Thonny user directory, eg:
    #   Windows: C:\Users\<you>\AppData\Roaming\Thonny
    #   Linux:   ~/.thonny
    #   macOS:   ~/Library/Application Support/Thonny
    base_dir = get_thonny_user_dir()

    # Our logs folder: <thonny_user_dir>/logs
    logs_dir = os.path.join(base_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Derive a base name from the file, or "untitled"
    if editor.is_untitled():
        base_name = "untitled"
    else:
        target_path: Optional[str] = editor.get_target_path()
        if target_path:
            base_name = os.path.splitext(os.path.basename(target_path))[0]
        else:
            base_name = "untitled"

    base_name = _sanitize_filename(base_name)

    # Timestamped filename so nothing gets overwritten
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{base_name}_{timestamp}.py"
    filename = _sanitize_filename(filename)

    full_path = os.path.join(logs_dir, filename)

    try:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(source)
    except Exception:
        # Silent failure: we don't want to break Run if logging fails
        return


def load_plugin() -> None:
    wb = get_workbench()
    # "Run" is emitted when the user presses the Run/Execute button
    wb.bind("Run", _log_current_program, add=True)
