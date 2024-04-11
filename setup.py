import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["customtkinter",
                 "tkinter",
                 "PIL",
                 "tkcalendar",
                 "os",
                 "sqlite3",
                 "random",
                 "string",
                 "datetime",
                 "qrcode",
                 "pyzbar",
                 "cv2",
                 "numpy",
                 "matplotlib",
                 "pandas",
                 "requests",
                 "calendar",
                 ],  # Add any additional packages your script depends on
    "include_files": [
        ("employee_qrcodes", "employee_qrcodes"),
        ("frame_2_icons", "frame_2_icons"),
        ("frame_3_icons", "frame_3_icons"),
        ("frame_4_icons", "frame_4_icons"),
        ("frame_5_icons", "frame_5_icons"),
        ("frame_6_icons", "frame_6_icons"),
        ("frame_7_icons", "frame_7_icons"),
        ("member_qrcodes", "member_qrcodes"),
        ("test_images", "test_images"),
        ("trainer_qrcodes", "trainer_qrcodes"),
        # Add more include_files as needed
        ("attendance_records.db", "attendance_records.db"),
        ("employee_attendance_records.db", "employee_attendance_records.db"),
        ("pat.png", "pat.png"),
        ("README.md", "README.md"),
        ("register_employee.db", "register_employee.db"),
        ("register_equipment.db", "register_equipment.db"),
        ("register_trainer.db", "register_trainer.db"),
        ("registered_users.db", "registered_users.db"),
        ("registration_form.db", "registration_form.db"),
        ("requirements.txt", "requirements.txt"),
        ("trainer_attendance_records.db", "trainer_attendance_records.db"),
        ("visitors_log.db", "visitors_log.db"),
    ],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this option if you want to hide the console window

executables = [Executable("gym.py", base=base)]

setup(
    name="GymApplication",
    version="0.1",
    description="Your Gym Application Description",
    options={"build_exe": build_exe_options},
    executables=executables,
)
