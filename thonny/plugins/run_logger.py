def log_current_program():
    editor = get_workbench().get_editor_notebook().get_current_editor()
    if editor is None:
        print("No editor found")
        return

    cv = editor.get_code_view()

    # The correct way to get text in your Thonny build
    try:
        source = cv.text.get("1.0", "end-1c")
    except Exception as e:
        print("Failed to read editor text:", e)
        return

    logs_dir = os.path.join(get_workbench().get_thonny_user_dir(), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"run_{timestamp}.py"
    filepath = os.path.join(logs_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(source)

    print("LOGGED PROGRAM TO:", filepath)
