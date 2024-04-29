import sys
from cx_Freeze import setup, Executable

# For .exe file conversion

build_exe_options = {
    "packages": [
        "customtkinter",
        "cv2",
        "datetime",
        "matplotlib",
        "numpy",
        "PIL",
        "qrcode",
        "random",
        "requests",
        "sqlite3",
        "string",
        "tkcalendar",
        "tkinter"
    ],
    # Add any additional packages your script depends on
    "include_files": [
        ("SQLite db", "SQLite db"),
        ("templates", "templates"),
        ("requirements.txt", "requirements.txt"),
        ("setup.txt", "setup.txt"),
    ],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this option if you want to hide the console window

executables = [Executable("gym.py", base=base)]

setup(
    name="D'Grit Gym",
    version="0.1",
    description="Capstone Project",
    options={"build_exe": build_exe_options},
    executables=executables,
)
