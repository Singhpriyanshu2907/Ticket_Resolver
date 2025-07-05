import os
import pathlib


list_of_files = [

    "github/workflows/.gitkeep",
    "src/__init__.py",
    "src/classify_ticket.py",
    "src/generate_reply.py",
    "src/gmail_sender.py",
    "src/sheet_connectore.py",
    "src/logger.py",
    "src/custom_exception.py",
    ".env",
    "main.py",
    "register_ticket",
    "notebook/experiments.ipynb",
    "requirements.txt",
    "utils/__init__.py"
]

for files in list_of_files:
    filepath = pathlib.Path(files)

    if filepath.suffix:
        filedir = filepath.parent
        if filedir and not filedir.exists():
            os.makedirs(filedir, exist_ok = True)

        if not filepath.exists():
            with open(filepath, "w") as f:
                pass
            print (f"Created empty file at {filepath}")

        else:
            if not filepath.exists():
                os.makedirs(filepath, exist_ok = True)
                print(f"Created directory {filepath}")