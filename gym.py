import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import os
import sqlite3
import random
import string
import qrcode
import cv2
import datetime
import requests
import calendar
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


def change_appearance_mode_event(new_appearance_mode):
    ctk.set_appearance_mode(new_appearance_mode)


def send_sms_notification(to_phone_number, message):
    print("PHONE NUMBER", to_phone_number)
    print("MESSAGE", message)

    # Use environment variables or a configuration file to manage API keys
    api_key=''

    # Change this URL based on your requirements
    url='https://api.semaphore.co/api/v4/priority'

    payload={
        'apikey': api_key,
        'number': to_phone_number,
        'message': message
    }

    # Handle specific exceptions
    try:
        response=requests.post(url, data=payload)

        if response.status_code == 200:
            print("SEND MESSAGE SUCCESS")
            print(response.json())
        else:
            print(response.text)
            print("ERROR SENDING MESSAGE")
            print("STATUS CODE", response.status_code)
    except requests.exceptions.RequestException as req_exc:
        print("Request Exception:", req_exc)
    except Exception as e:
        print("Failed to send message", e)


def check_date():
    current_date=datetime.now()

    # Get all instances in the registration table
    conn=sqlite3.connect('registration_form.db')
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM registration")
    registrations=cursor.fetchall()

    for registration in registrations:
        # Get the end_date and contact_no from the registration
        end_date=registration[15]
        contact_no=registration[9]
        print("Testing: ", end_date)
        if datetime.strptime(end_date, '%Y-%m-%d') < current_date:
            print("Expired")
            # Update the status of the registration to "Expired"
            cursor.execute("UPDATE registration SET status=? WHERE id=?", ("Expired", registration[0]))
            conn.commit()

            # Send SMS to the member
            sms_message="Your gym membership has expired. Renew your subscription to continue accessing D'GRIT GYM."
            send_sms_notification(contact_no, sms_message)


class MainApp(ctk.CTk):
    check_date()

    def __init__(self):
        super().__init__()

        # Fixed size of the window, and cannot be resized
        self.resizable(False, False)
        self.title("D'Grit Gym Management System")
        self.geometry("1240x600")

        # Calculate the screen width and height
        screen_width=self.winfo_screenwidth()
        screen_height=self.winfo_screenheight()

        # Calculate the position to center the window
        x=(screen_width - 1240) // 2
        y=(screen_height - 600) // 2.5

        # Set the window's position
        self.geometry(f"1240x600+{x}+{y}")

        # Set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path=os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image=ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "gym_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "gym_dark.png")),
            size=(150, 60))
        self.gym_image=ctk.CTkImage(
            Image.open(os.path.join(image_path, "gym_cover.png")),
            size=(500, 150))
        self.image_icon_image=ctk.CTkImage(
            Image.open(os.path.join(image_path, "image_icon_light.png")),
            size=(20, 20))
        self.home_image=ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "home_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image=ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image=ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.add_equipment_image=ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "dumbell_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "dumbell_light.png")), size=(20, 20))
        self.visitor_image=ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "visitor_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "visitor_light.png")), size=(20, 20))
        self.employee_image=ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "employee_black.png")),
            dark_image=Image.open(os.path.join(image_path, "employee_white.png")), size=(20, 20))
        self.trainer_image=ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "trainer_black.png")),
            dark_image=Image.open(os.path.join(image_path, "trainer_white.png")), size=(20, 20))
        self.attendance_image=ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "scan_black.png")),
            dark_image=Image.open(os.path.join(image_path, "scan_white.png")), size=(20, 20))

        # # Load the large image you want to insert
        # large_image=Image.open("test_images/gym_cover.png")
        # large_image=ImageTk.PhotoImage(large_image)

        # create navigation frame
        self.navigation_frame=ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(12, weight=1)

        self.navigation_frame_label=ctk.CTkLabel(
            self.navigation_frame, text="", image=self.logo_image,
            compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=50, border_spacing=10,
            text="Home",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=50, border_spacing=10,
            text="Membership",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_user_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=50, border_spacing=10,
            text="Take Attendance",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.attendance_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=50, border_spacing=10,
            text="Gym Equipment",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_equipment_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.frame_5_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=50, border_spacing=10,
            text="Trainers",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.trainer_image, anchor="w", command=self.frame_5_button_event)
        self.frame_5_button.grid(row=5, column=0, sticky="ew")

        self.frame_6_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=50, border_spacing=10,
            text="Gymers",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.visitor_image, anchor="w", command=self.frame_6_button_event)
        self.frame_6_button.grid(row=6, column=0, sticky="ew")

        self.frame_7_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=50, border_spacing=10,
            text="Employees",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.employee_image, anchor="w", command=self.frame_7_button_event)
        self.frame_7_button.grid(row=7, column=0, sticky="ew")

        self.frame_8_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=50, border_spacing=10,
            text="Create User Account",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_user_image, anchor="w", command=self.frame_8_button_event)
        self.frame_8_button.grid(row=8, column=0, sticky="ew")

        self.appearance_mode_menu=ctk.CTkOptionMenu(
            self.navigation_frame, values=["Dark", "Light", "System"],
            command=change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=10, column=0, padx=20, pady=10, sticky="s")

        self.logout_button=ctk.CTkButton(
            self.navigation_frame,
            text="Logout",
            fg_color="Red", text_color=("gray10", "gray90"),
            hover_color=("red3", "red4"),
            command=self.logout)
        self.logout_button.grid(row=11, column=0, padx=20, pady=5, sticky="ew")

        # create home frame
        self.home_frame=ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        # self.large_image_label=ctk.CTkLabel(self.home_frame, text="", image=large_image)
        # self.large_image_label.grid(row=4, column=0, padx=20, pady=10)

        # create frames
        # 2
        self.second_frame=ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # 3
        self.third_frame=ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # 4
        self.fourth_frame=ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # 5
        self.fifth_frame=ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # 6
        self.sixth_frame=ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # 7
        self.seventh_frame=ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        # 8
        self.eighth_frame=ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")
        create_home_frame(self.home_frame)  # Call the function to create home frame
        create_gym_membership_frame(self.second_frame)  # Call the function to create gym membership frame
        create_take_attendance_frame(self.third_frame)
        create_gym_equipment_frame(self.fourth_frame)
        create_trainers_frame(self.fifth_frame)
        create_visitors_frame(self.sixth_frame)
        create_employee_frame(self.seventh_frame)
        create_account_management_frame(self.eighth_frame)

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")
        self.frame_5_button.configure(fg_color=("gray75", "gray25") if name == "frame_5" else "transparent")
        self.frame_6_button.configure(fg_color=("gray75", "gray25") if name == "frame_6" else "transparent")
        self.frame_7_button.configure(fg_color=("gray75", "gray25") if name == "frame_7" else "transparent")
        self.frame_8_button.configure(fg_color=("gray75", "gray25") if name == "frame_8" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()
        if name == "frame_5":
            self.fifth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fifth_frame.grid_forget()
        if name == "frame_6":
            self.sixth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.sixth_frame.grid_forget()
        if name == "frame_7":
            self.seventh_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.seventh_frame.grid_forget()
        if name == "frame_8":
            self.eighth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.eighth_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def frame_5_button_event(self):
        self.select_frame_by_name("frame_5")

    def frame_6_button_event(self):
        self.select_frame_by_name("frame_6")

    def frame_7_button_event(self):
        self.select_frame_by_name("frame_7")

    def frame_8_button_event(self):
        self.select_frame_by_name("frame_8")

    # Add a logout method to the MainApp class
    def logout(self):
        # Close the main application window
        self.destroy()

        # Reopen the login window
        create_login_window()


# ------------HOME FRAME----------------------#

def create_home_frame(home):
    dashboard_frame=ctk.CTkScrollableFrame(home)
    dashboard_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # label frame
    label_frame=ctk.CTkFrame(dashboard_frame)
    label_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # dashboard label align left
    dashboard_label=ctk.CTkLabel(label_frame, text="Dashboard | Overview", font=("Arial bold", 30))
    dashboard_label.pack(pady=5, padx=10, side=tk.LEFT)

    # Display the current time on the left side of the dashboard label
    current_time=datetime.now().strftime("%I:%M:%S %p")
    current_time_label=ctk.CTkLabel(label_frame, text=current_time, font=("Agency FB bold", 46))
    current_time_label.pack(pady=5, padx=10, side=tk.RIGHT)

    # Function to update the clock
    def update_clock():
        current_time=datetime.now().strftime("%I:%M:%S %p")
        current_time_label.configure(text=current_time)
        home.after(1000, update_clock)  # Schedule the next update after 1000 milliseconds (1 second)

    # Start the clock update
    update_clock()

    # frame
    panel_frame=ctk.CTkFrame(dashboard_frame)
    panel_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # member panel frame
    member_panel_frame=ctk.CTkFrame(panel_frame, fg_color="#00C957")
    member_panel_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # create a small rectangular label to display the no. of members
    members_label=ctk.CTkLabel(member_panel_frame, text="Members", font=("Arial bold", 14))
    members_label.pack(pady=5, padx=60, anchor="w")

    # create a counter label to display the no. of members
    members_counter_label=ctk.CTkLabel(member_panel_frame, text="", font=("Arial bold", 50))
    members_counter_label.pack(pady=10, padx=10, anchor="center")

    def get_members_count():
        # get the no. of members from the database
        conn=sqlite3.connect('registration_form.db')
        cursor=conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM registration")
        members_count=cursor.fetchone()[0]
        members_counter_label.configure(text=members_count)
        conn.close()
        home.after(1000, get_members_count)

    get_members_count()

    # visitor panel frame
    visitors_panel_frame=ctk.CTkFrame(panel_frame, fg_color="orange")
    visitors_panel_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # create a small rectangular label to display the no. of members
    visitors_label=ctk.CTkLabel(visitors_panel_frame, text="Visitors", font=("Arial bold", 14))
    visitors_label.pack(pady=5, padx=65, anchor="w")

    # create a counter label to display the no. of members
    visitor_counter_label=ctk.CTkLabel(visitors_panel_frame, text="", font=("Arial bold", 50))
    visitor_counter_label.pack(pady=10, padx=10, anchor="center")

    def get_visitors_count():
        # get the no. of members from the database
        conn=sqlite3.connect('visitors_log.db')
        cursor=conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM visitors")
        visitors_count=cursor.fetchone()[0]
        visitor_counter_label.configure(text=visitors_count)
        conn.close()
        home.after(1000, get_visitors_count)

    get_visitors_count()

    # employee panel frame
    employee_panel_frame=ctk.CTkFrame(panel_frame, fg_color="blue")
    employee_panel_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    # create a small rectangular label to display the no. of employees
    employee_label=ctk.CTkLabel(employee_panel_frame, text="Employees", font=("Arial bold", 14))
    employee_label.pack(pady=5, padx=50, anchor="w")

    # create a counter label to display the no. of employees
    employee_counter_label=ctk.CTkLabel(employee_panel_frame, text="", font=("Arial bold", 50))
    employee_counter_label.pack(pady=10, padx=10, anchor="center")

    def get_employee_count():
        # get the no. of members from the database
        conn=sqlite3.connect('register_employee.db')
        cursor=conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM employees")
        employee_count=cursor.fetchone()[0]
        employee_counter_label.configure(text=employee_count)
        conn.close()
        home.after(1000, get_employee_count)

    get_employee_count()

    # trainer panel frame
    trainer_panel_frame=ctk.CTkFrame(panel_frame, fg_color="purple")
    trainer_panel_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

    # create a small rectangular label to display the no. of trainers
    trainer_label=ctk.CTkLabel(trainer_panel_frame, text="Trainers", font=("Arial bold", 14))
    trainer_label.pack(pady=5, padx=60, anchor="w")

    # create a counter label to display the no. of trainers
    trainer_counter_label=ctk.CTkLabel(trainer_panel_frame, text="", font=("Arial bold", 50))
    trainer_counter_label.pack(pady=10, padx=10, anchor="center")

    def get_trainer_count():
        # get the no. of members from the database
        conn=sqlite3.connect('register_trainer.db')
        cursor=conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM trainer")
        trainer_count=cursor.fetchone()[0]
        trainer_counter_label.configure(text=trainer_count)
        conn.close()
        home.after(1000, get_trainer_count)

    get_trainer_count()

    # gym equipment panel frame
    gym_equipment_panel_frame=ctk.CTkFrame(panel_frame, fg_color="red")
    gym_equipment_panel_frame.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

    # create a small rectangular label to display the no. of gym equipment
    gym_equipment_label=ctk.CTkLabel(gym_equipment_panel_frame, text="Gym Equipment", font=("Arial bold", 14))
    gym_equipment_label.pack(pady=5, padx=30, anchor="w")

    # create a counter label to display the no. of gym equipment
    gym_equipment_counter_label=ctk.CTkLabel(gym_equipment_panel_frame, text="", font=("Arial bold", 50))
    gym_equipment_counter_label.pack(pady=10, padx=10, anchor="center")

    def get_gym_equipment_count():
        # get the no. of members from the database
        conn=sqlite3.connect('register_equipment.db')
        cursor=conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM equipment")
        gym_equipment_count=cursor.fetchone()[0]
        gym_equipment_counter_label.configure(text=gym_equipment_count)
        conn.close()
        home.after(1000, get_gym_equipment_count)

    get_gym_equipment_count()

    # -------------------FRAME 1 ----------------------#
    graph_frame=ctk.CTkFrame(dashboard_frame)
    graph_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Monthly Income Report Graph
    income_frame=ctk.CTkFrame(graph_frame)
    income_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

    # Create a small rectangular label for the income report
    income_label=ctk.CTkLabel(income_frame, text="Monthly Income (PHP)", font=("Arial bold", 16))
    income_label.pack(pady=5, padx=10, anchor="w")

    # Create a figure and axis for the income report graph
    fig, ax=plt.subplots(figsize=(6, 4), dpi=100)
    canvas=FigureCanvasTkAgg(fig, master=income_frame)
    canvas_widget=canvas.get_tk_widget()
    canvas_widget.pack(fill="both", expand=True)

    # Update the income report graph
    update_income_report(home, ax, canvas)
    canvas.draw()

    # Make the rows and columns resizable
    for i in range(5):
        panel_frame.grid_columnconfigure(i, weight=1)

    panel_frame.grid_rowconfigure(0, weight=1)

    # ------------FRAME 2----------------------#
    graph_frame2=ctk.CTkFrame(graph_frame)
    graph_frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    sub_frame=ctk.CTkFrame(graph_frame2)
    sub_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # COUNT FRAME 1
    counter_frame=ctk.CTkFrame(sub_frame)
    counter_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # total membership income label
    total_membership_income_label=ctk.CTkLabel(counter_frame, text="Total Membership Income (PHP)",
                                               font=("Arial bold", 12))
    total_membership_income_label.pack(pady=10, padx=10, anchor="w")

    # count label frame 1
    count_frame1=ctk.CTkFrame(counter_frame, fg_color="#00C957")
    count_frame1.pack(pady=10, padx=10, fill="both", expand=True)

    # create a counter label 1
    count_label1=ctk.CTkLabel(count_frame1, text="", font=("Arial bold", 30))
    count_label1.pack(pady=10, padx=30, anchor="center")

    def get_total_membership_income():
        # get the no. of members from the database
        conn=sqlite3.connect('registration_form.db')
        cursor=conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM registration")
        members_count=cursor.fetchone()[0]
        total_membership_income=members_count * 700
        count_label1.configure(text=f"{total_membership_income}")
        conn.close()
        home.after(1000, get_total_membership_income)

    get_total_membership_income()

    # COUNT FRAME 2
    counter_frame2=ctk.CTkFrame(sub_frame)
    counter_frame2.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # total visitor income label
    total_visitor_income_label=ctk.CTkLabel(counter_frame2, text="Total Visitor Income (PHP)", font=("Arial bold", 12))
    total_visitor_income_label.pack(pady=10, padx=10, anchor="w")

    # count label frame 2
    count_frame2=ctk.CTkFrame(counter_frame2, fg_color="orange")
    count_frame2.pack(pady=10, padx=10, fill="both", expand=True)

    # count label 2
    count_label2=ctk.CTkLabel(count_frame2, text="", font=("Arial bold", 30))
    count_label2.pack(pady=10, padx=30, anchor="center")

    def get_total_visitor_income():
        # get the no. of members from the database
        conn=sqlite3.connect('visitors_log.db')
        cursor=conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM visitors")
        visitors_count=cursor.fetchone()[0]
        total_visitor_income=visitors_count * 50
        count_label2.configure(text=f"{total_visitor_income}")
        conn.close()
        home.after(1000, get_total_visitor_income)

    get_total_visitor_income()

    # -------------------FRAME 3 ----------------------#
    graph_frame3=ctk.CTkFrame(graph_frame)
    graph_frame3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
    sub_frame2=ctk.CTkFrame(graph_frame3)
    sub_frame2.pack(pady=10, padx=10, fill="both", expand=True)

    # COUNT FRAME 3
    counter_frame3=ctk.CTkFrame(sub_frame2)
    counter_frame3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    # total membership income label
    total_time_in_label=ctk.CTkLabel(counter_frame3, text="Total Attendance Time In:",
                                     font=("Arial bold", 14))
    total_time_in_label.pack(pady=10, padx=10, anchor="w")

    # count label frame 3
    count_frame3=ctk.CTkFrame(counter_frame3, fg_color="#007FFF")
    count_frame3.pack(pady=10, padx=10, fill="both", expand=True)
    # count label 3
    count_label3=ctk.CTkLabel(count_frame3, text="", font=("Arial bold", 30))
    count_label3.pack(pady=10, padx=50, anchor="center")

    # COUNT FRAME 4
    counter_frame4=ctk.CTkFrame(sub_frame2)
    counter_frame4.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
    # total visitor income label
    total_time_out_label=ctk.CTkLabel(counter_frame4, text="Total Time Out:", font=("Arial bold", 14))
    total_time_out_label.pack(pady=10, padx=10, anchor="w")

    # count label frame 4
    count_frame4=ctk.CTkFrame(counter_frame4, fg_color="#FF0000")
    count_frame4.pack(pady=10, padx=10, fill="both", expand=True)
    # count label 4
    count_label4=ctk.CTkLabel(count_frame4, text="", font=("Arial bold", 30))
    count_label4.pack(pady=10, padx=50, anchor="center")

    def get_time_in_and_out():
        # Update count of time-in and time-out for membership
        conn=sqlite3.connect('attendance_records.db')
        cursor=conn.cursor()
        cursor.execute("SELECT COUNT(time_in), COUNT(time_out) FROM attendance_records")
        count_time_in, count_time_out=cursor.fetchone()
        conn.close()

        # Update count labels for time-in and time-out
        count_label3.configure(text=f"{count_time_in}")
        count_label4.configure(text=f"{count_time_out}")
        home.after(1000, get_time_in_and_out)

    get_time_in_and_out()


# Graph
def update_income_report(root, ax, canvas):
    # Get the current month
    current_month=datetime.now().strftime('%Y-%m')

    # Connect to the visitors database
    conn_visitors=sqlite3.connect('visitors_log.db')
    cursor_visitors=conn_visitors.cursor()

    # Retrieve monthly visitor count
    cursor_visitors.execute("SELECT strftime('%Y-%m', time) as month, COUNT(*) FROM visitors GROUP BY month")
    visitors_data=cursor_visitors.fetchall()

    conn_visitors.close()

    # Connect to the members database
    conn_members=sqlite3.connect('registration_form.db')
    cursor_members=conn_members.cursor()

    # Retrieve monthly member count
    cursor_members.execute("SELECT strftime('%Y-%m', start_date) as month, COUNT(*) FROM registration GROUP BY month")
    members_data=cursor_members.fetchall()

    conn_members.close()

    # Merge the data for common months
    merged_data={}
    for month, visitors_count in visitors_data:
        merged_data[month]={'visitors': visitors_count * 50, 'members': 0}

    for month, members_count in members_data:
        if month in merged_data:
            merged_data[month]['members']=members_count * 700
        else:
            merged_data[month]={'visitors': 0, 'members': members_count * 700}

    # Extract month labels and total income values
    months, visitor_incomes, member_incomes=zip(
        *[(month if month != 'None' else 'Visitors', data['visitors'], data['members']) for month, data in
          merged_data.items()])

    # Convert months to a NumPy array with a specific data type (e.g., float)
    months_array=np.array(months, dtype=str)

    # Plot the monthly income report with inverted colors
    ax.clear()
    visitors_bar=ax.bar(months_array, visitor_incomes, color='orange', alpha=0.7, label='Visitors')
    members_bar=ax.bar(months_array, member_incomes, bottom=visitor_incomes, color='#00C957', alpha=0.7,
                       label='Members')
    ax.set_ylabel('Income (PHP)')

    # Update the title based on the current month
    ax.set_title(
        f'Monthly Income Report ({calendar.month_name[int(current_month.split("-")[1])]} {current_month.split("-")[0]})')

    # Show legend to distinguish between visitors and members
    ax.legend()

    # Annotate each bar with the total income value
    for bar, visitors_income, members_income in zip(visitors_bar, visitor_incomes, member_incomes):
        total_income=visitors_income + members_income
        ax.text(bar.get_x() + bar.get_width() / 2, total_income,
                f'{total_income} PHP', ha='center', va='bottom', color='black', fontweight='bold')

    ax.grid(True)

    # Redraw the canvas
    canvas.draw()

    # Schedule the next update
    root.after(1000, update_income_report, root, ax, canvas)


# ------------FRAME_2----------------------#

def create_gym_membership_frame(frame_2):
    # Define the desired button width and height
    button_width=300
    button_height=300

    # Define the path to the directory containing your image files
    frame_2_icons=os.path.join(os.path.dirname(os.path.realpath(__file__)), "frame_2_icons")

    # Load and resize the images
    register_image=Image.open(os.path.join(frame_2_icons, 'register_black.png'))
    register_image=register_image.resize((button_width, button_height), Image.LANCZOS)

    view_image=Image.open(os.path.join(frame_2_icons, 'list_black.png'))
    view_image=view_image.resize((button_width, button_height), Image.LANCZOS)

    def register_member():
        # When the "Register Members" button is clicked, create and show the registration frame
        registration_frame=RegistrationFrame(frame_2)
        registration_frame.pack(fill='both', expand=True)

    def view_member():
        # When the "View Members" button is clicked, create and show the view members frame
        view_member_frame=ViewFrame(frame_2)
        view_member_frame.pack(fill='both', expand=True)

    # Create the buttons with the resized images
    register_member_button=ctk.CTkButton(
        master=frame_2,
        text="Register Members",
        image=ImageTk.PhotoImage(register_image),
        compound=tk.TOP,
        command=register_member,  # Call the function to open the frame
        width=button_width,
        height=button_height,
        fg_color="#00C957",
        text_color=("gray10", "gray90")
    )
    register_member_button.place(x=150, y=150)

    view_member_button=ctk.CTkButton(
        master=frame_2,
        text="View Members",
        image=ImageTk.PhotoImage(view_image),
        compound=tk.TOP,
        command=view_member,
        width=button_width,
        height=button_height,
        fg_color="#00C957",
        text_color=("gray10", "gray90"),
    )
    view_member_button.place(x=600, y=150)


class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create a connection to the database
        self.conn=sqlite3.connect('registration_form.db')
        self.cursor=self.conn.cursor()

        # STEP 1: PERSONAL INFORMATION
        # Define and configure widgets within the frame
        label=ctk.CTkLabel(self, text="D'Grit Gym Membership Registration", font=("Arial bold", 26))
        label.pack(pady=20, padx=10)

        # outer frame
        outer_frame=ctk.CTkFrame(self)
        outer_frame.pack(pady=20, padx=10)

        # create frame to hold all the widget frames
        widget_frames=ctk.CTkFrame(outer_frame)
        widget_frames.pack(pady=10, padx=10)

        # Create a frame to hold the form fields
        first_frame=ctk.CTkFrame(widget_frames)
        first_frame.grid(row=0, column=0, padx=10, pady=10)
        personal_info_frame=ctk.CTkFrame(first_frame)
        personal_info_frame.pack(pady=10, padx=10)

        # Create a custom font for labels
        label_font=ctk.CTkFont(family="Arial bold", size=16)  # Adjust the size as

        # Name
        first_name_label=ctk.CTkLabel(personal_info_frame, text="First Name:", font=label_font)
        first_name_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        first_name_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your first name")
        first_name_entry.grid(row=2, column=1, padx=20, pady=5)

        middle_name_label=ctk.CTkLabel(personal_info_frame, text="Middle Name:", font=label_font)
        middle_name_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")
        middle_name_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your middle name")
        middle_name_entry.grid(row=3, column=1, padx=20, pady=5)

        last_name_label=ctk.CTkLabel(personal_info_frame, text="Last Name:", font=label_font)
        last_name_label.grid(row=4, column=0, padx=20, pady=5, sticky="w")
        last_name_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your last name")
        last_name_entry.grid(row=4, column=1, padx=20, pady=5)

        # Age
        age_label=ctk.CTkLabel(personal_info_frame, text="Age:", font=label_font)
        age_label.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        age_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your age")
        age_entry.grid(row=6, column=1, padx=20, pady=5)

        # Sex
        sex_label=ctk.CTkLabel(personal_info_frame, text="Sex:", font=label_font)
        sex_label.grid(row=7, column=0, padx=20, pady=5, sticky="w")
        sex_entry=ctk.CTkComboBox(personal_info_frame, values=["Male", "Female", "Other"])
        sex_entry.grid(row=7, column=1, padx=20, pady=5)

        # Create a DateEntry widget for the birthdate
        birth_date_label=ctk.CTkLabel(personal_info_frame, text="Date of Birth:", font=label_font)
        birth_date_label.grid(row=5, column=0, padx=20, pady=5, sticky="w")

        # Use the existing birth_date_entry you created
        self.birth_date_entry=DateEntry(personal_info_frame, width=20, date_pattern="yyyy-mm-dd")
        self.birth_date_entry.grid(row=5, column=1, padx=20, pady=15, sticky="w")

        # Bind the function to the <<DateEntrySelected>> event
        self.birth_date_entry.bind("<<DateEntrySelected>>", self.calculate_age)

        # Address
        address_label=ctk.CTkLabel(personal_info_frame, text="Address:", font=label_font)
        address_label.grid(row=8, column=0, padx=20, pady=5, sticky="w")
        address_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your address")
        address_entry.grid(row=8, column=1, padx=20, pady=5)

        second_frame=ctk.CTkFrame(widget_frames)
        second_frame.grid(row=0, column=1, padx=10, pady=10)
        contact_frame=ctk.CTkFrame(second_frame)
        contact_frame.pack(pady=10, padx=10)

        # Create a custom font for labels
        label_font=ctk.CTkFont(family="Arial bold", size=16)  # Adjust the size as

        # Assuming you have a list of nationalities
        nationalities_list=["Select Nationality", "Filipino", "American", "Chinese", "Japanese", "Korean", "Other"]

        # Nationality Label
        nationality_label=ctk.CTkLabel(contact_frame, text="Nationality:", font=label_font)
        nationality_label.pack(pady=5, padx=10, anchor="w")

        # Create a CTkComboBox widget for nationalities
        nationality_combo=ctk.CTkComboBox(contact_frame, values=nationalities_list)
        nationality_combo.pack(pady=5, padx=10, fill="x")
        nationality_combo.set("Select Nationality")  # Set a default selection

        # Contact No
        contact_no_label=ctk.CTkLabel(contact_frame, text="Contact No:", font=label_font)
        contact_no_label.pack(pady=3, padx=10, anchor="w")
        contact_no_entry=ctk.CTkEntry(contact_frame, placeholder_text="+63 9123456789")
        contact_no_entry.pack(pady=0, padx=10, fill="x")

        # Email Address
        email_label=ctk.CTkLabel(contact_frame, text="Email Address:", font=label_font)
        email_label.pack(pady=0, padx=10, anchor="w")
        email_entry=ctk.CTkEntry(contact_frame, placeholder_text="example@gmail.com")
        email_entry.pack(pady=0, padx=10, fill="x")

        # Emergency Contact No
        emergency_contact_label=ctk.CTkLabel(contact_frame, text="Emergency Contact No:", font=label_font)
        emergency_contact_label.pack(pady=0, padx=10, anchor="w")
        emergency_contact_entry=ctk.CTkEntry(contact_frame, placeholder_text="+63 9123456789")
        emergency_contact_entry.pack(pady=10, padx=10, fill="x")

        # Create a frame to hold the form fields
        third_frame=ctk.CTkFrame(widget_frames)
        third_frame.grid(row=0, column=2, padx=10, pady=10)
        subscription_frame=ctk.CTkFrame(third_frame)
        subscription_frame.pack(pady=10, padx=10)

        # Create a custom font for labels
        label_font=ctk.CTkFont(family="Arial bold", size=16)  # Adjust the size as needed

        # Subscription ID
        subscription_id_label=ctk.CTkLabel(subscription_frame, text="Subscription ID:", font=label_font)
        subscription_id_label.grid(row=1, column=0, padx=20, pady=15, sticky="w")

        # Subscription ID entry (read-only)
        self.subscription_id_entry=ctk.CTkEntry(subscription_frame, placeholder_text="DG-XXXXXXXX")
        self.subscription_id_entry.grid(row=1, column=1, padx=20, pady=15)

        self.subscription_id_entry.configure(state="disabled")

        # Set the subscription ID based on the last inserted ID
        self.set_subscription_id()

        # Create the widgets for subscription plan, start date, and end date
        subscription_plan_label=ctk.CTkLabel(subscription_frame, text="Subscription Plan:", font=label_font)
        subscription_plan_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        subscription_plan_options=["Weekly", "Monthly", "Yearly"]
        self.subscription_plan_entry=ctk.CTkComboBox(subscription_frame, values=subscription_plan_options)

        # Set "Monthly" as the default value
        self.subscription_plan_entry.set("Monthly")

        self.subscription_plan_entry.grid(row=2, column=1, padx=20, pady=15)

        # Bind the function to the <<ComboboxSelected>> event
        self.subscription_plan_entry.bind("<<ComboboxSelected>>", self.update_dates_on_subscription_change)

        start_timestamp_label=ctk.CTkLabel(subscription_frame, text="Start:", font=label_font)
        start_timestamp_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        # Use the existing start_timestamp_entry you created
        self.start_timestamp_entry=DateEntry(subscription_frame, width=20, date_pattern="yyyy-mm-dd")
        self.start_timestamp_entry.grid(row=3, column=1, padx=20, pady=15, sticky="w")

        end_timestamp_label=ctk.CTkLabel(subscription_frame, text="End:", font=label_font)
        end_timestamp_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        # Use the existing end_timestamp_entry you created
        self.end_timestamp_entry=DateEntry(subscription_frame, width=20, date_pattern="yyyy-mm-dd")
        self.end_timestamp_entry.grid(row=4, column=1, padx=20, pady=15, sticky="w")

        # disable the start and end date
        self.start_timestamp_entry.configure(state="disabled")
        self.end_timestamp_entry.configure(state="disabled")

        # Reference to the user who owns the subscription
        user_reference_label=ctk.CTkLabel(subscription_frame, text="User Reference:", font=label_font)
        user_reference_label.grid(row=5, column=0, padx=20, pady=15, sticky="w")
        user_reference_entry=ctk.CTkEntry(subscription_frame, placeholder_text="User ID or Name")
        user_reference_entry.grid(row=5, column=1, padx=20, pady=15)

        # Create a "Register" button
        register_button=ctk.CTkButton(outer_frame, text="Register", fg_color="Green",
                                      text_color=("gray10", "gray90"),
                                      hover_color=("green3", "green4"),
                                      command=self.register_subscription)
        register_button.pack(pady=20, side=tk.TOP)

        # create a back button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.place(x=450, y=550)

        # Store the Entry fields and other widgets as instance attributes
        self.first_name_entry=first_name_entry
        self.middle_name_entry=middle_name_entry
        self.last_name_entry=last_name_entry
        self.age_entry=age_entry
        self.sex_entry=sex_entry
        self.address_entry=address_entry
        self.nationality_combo=nationality_combo
        self.contact_no_entry=contact_no_entry
        self.email_entry=email_entry
        self.emergency_contact_entry=emergency_contact_entry
        self.subscription_id_entry=self.subscription_id_entry
        self.start_timestamp_entry=self.start_timestamp_entry
        self.end_timestamp_entry=self.end_timestamp_entry
        self.user_reference_entry=user_reference_entry

        with sqlite3.connect('registration_form.db') as conn:
            cursor=conn.cursor()

        # Create a table to store registration information
        cursor.execute('''
                   CREATE TABLE IF NOT EXISTS registration (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       first_name TEXT,
                       middle_name TEXT,
                       last_name TEXT,
                       age INTEGER,
                       sex TEXT,
                       birth_date DATE,
                       address TEXT,
                       nationality TEXT,
                       contact_no TEXT,
                       email TEXT,
                       emergency_contact_no TEXT,
                       subscription_id TEXT,
                       subscription_plan TEXT,
                       start_date DATE,
                       end_date DATE,
                       user_reference TEXT,
                       status TEXT DEFAULT 'Ongoing'
                   )
               ''')

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

    def calculate_age(self, event):
        # Get the selected birthdate
        birth_date_str=self.birth_date_entry.get()

        try:
            # Extract the date part without the time
            birth_date_str=birth_date_str.split()[0]

            # Convert the birthdate string to a datetime object
            birth_date_obj=datetime.strptime(birth_date_str, '%Y-%m-%d')

            # Calculate the age based on the birthdate
            current_date=datetime.now()
            age=current_date.year - birth_date_obj.year - (
                    (current_date.month, current_date.day) < (birth_date_obj.month, birth_date_obj.day)
            )

            # Update the age entry
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, str(age))
        except ValueError:
            # Handle invalid date format
            messagebox.showerror("Invalid Date", "Please enter a valid date in the format YYYY-MM-DD.")

    def update_dates_on_subscription_change(self, event):
        subscription_plan=self.subscription_plan_entry.get()

        # Calculate start and end dates based on the selected subscription plan
        current_date=datetime.now()

        if subscription_plan == "Weekly":
            start_date=current_date
            end_date=start_date + timedelta(weeks=1)
        elif subscription_plan == "Monthly":
            start_date=current_date
            end_date=start_date + timedelta(weeks=4)
        elif subscription_plan == "Yearly":
            start_date=current_date
            end_date=start_date + timedelta(weeks=52)
        else:
            return  # Do nothing for invalid plans

        # Update the DateEntry widgets
        self.start_timestamp_entry.set_date(start_date.strftime('%Y-%m-%d'))
        self.end_timestamp_entry.set_date(end_date.strftime('%Y-%m-%d'))

    @staticmethod
    def set_subscription_id():
        # generate random string of length 5
        letters=string.ascii_uppercase + string.digits
        result_str="DG-" + ''.join(random.choice(letters) for i in range(8))
        return result_str

    def send_sms(self, to_phone_number, message):

        print("PHONE NUMBER", to_phone_number)
        print("MESSAGE", message)

        # delete this one kapag magpupush sa github
        api_key=''

        # # you can change this one kung gusto mo maging priority or bulk. read the docs
        # url='https://api.semaphore.co/api/v4/messages'

        # change to this one if you want na maging priority ang message kaso mas mahal ang credits
        # 2 credits per 160 characters
        url='https://api.semaphore.co/api/v4/priority'

        payload={
            'apikey': api_key,
            'number': to_phone_number,
            'message': message
        }

        # this code will connect with the API and send the data
        try:
            response=requests.post(url, data=payload)

            if response.status_code == 200:

                print("SEND MESSAGE SUCCESS")
                print(response.json())
            else:
                print(response.text)
                print("ERROR SENDING MESSAGE")
                print("STATUS CODE", response.status_code)
        except Exception as e:
            print("failed to send message", e)

    def register_subscription(self):
        # Gather data from the form fields
        first_name=self.first_name_entry.get()
        middle_name=self.middle_name_entry.get()
        last_name=self.last_name_entry.get()
        age=self.age_entry.get()
        sex=self.sex_entry.get()
        birth_date=self.birth_date_entry.get()
        address=self.address_entry.get()
        nationality=self.nationality_combo.get()
        contact_no=self.contact_no_entry.get()
        email=self.email_entry.get()
        emergency_contact_no=self.emergency_contact_entry.get()
        subscription_id=self.set_subscription_id()
        subscription_plan=self.subscription_plan_entry.get()
        start_date=self.start_timestamp_entry.get()
        end_date=self.end_timestamp_entry.get()
        user_reference=self.user_reference_entry.get()

        # Validate the data
        if not (first_name and last_name and age and sex and birth_date and address and
                nationality and contact_no and email and emergency_contact_no and
                subscription_plan and start_date and end_date and user_reference):
            messagebox.showerror("Validation Error", "All fields are required.")
            return

        try:
            age=int(age)
        except ValueError:
            messagebox.showerror("Validation Error", "Age must be a valid integer.")
            return
        # create validation for the contact no. it must be started with no 0 for example: 09123456789
        try:
            contact_no=int(contact_no)
        except ValueError:
            messagebox.showerror("Validation Error", "Contact No must be 11-digit number.")

        # Calculate the age based on the provided birthdate
        birth_date_obj=datetime.strptime(birth_date, '%Y-%m-%d')
        current_date=datetime.now()
        age=current_date.year - birth_date_obj.year - (
                (current_date.month, current_date.day) < (birth_date_obj.month, birth_date_obj.day))

        # Create a connection to the database
        conn=sqlite3.connect('registration_form.db')
        cursor=conn.cursor()

        # Calculate the expiration date
        expiration_date=datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

        # Check if the end date is before the current date
        current_date=datetime.now()
        if expiration_date and expiration_date <= current_date:
            status="Expired"
        else:
            status="Ongoing"

        try:
            age=int(age)
        except ValueError:
            messagebox.showerror("Validation Error", "Age must be a valid integer.")
            return

        try:
            contact_no=int(contact_no)
        except ValueError:
            messagebox.showerror("Validation Error", "Contact No must be an 11-digit number.")
            return

        # Calculate the expiration date based on the subscription plan
        if subscription_plan == "Weekly":
            duration=timedelta(days=7)
        elif subscription_plan == "Monthly":
            duration=timedelta(weeks=4)  # Assuming 4 weeks in a month for simplicity
        elif subscription_plan == "Yearly":
            duration=timedelta(weeks=52)  # Assuming 52 weeks in a year for simplicity
        else:
            messagebox.showerror("Validation Error", "Invalid subscription plan.")
            return

        start_date=datetime.strptime(start_date, '%Y-%m-%d')
        end_date=start_date + duration

        # Format the date to include only the date part
        start_date_str=start_date.strftime('%Y-%m-%d')
        end_date_str=end_date.strftime('%Y-%m-%d')

        # Insert the data into the database
        cursor.execute('''
            INSERT INTO registration (first_name, middle_name, last_name, age, sex, birth_date, address,
                                    nationality, contact_no, email, emergency_contact_no, subscription_id,
                                    subscription_plan, start_date, end_date, user_reference)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (first_name, middle_name, last_name, age, sex, birth_date, address, nationality, contact_no,
              email, emergency_contact_no, subscription_id, subscription_plan, start_date_str, end_date_str,
              user_reference))

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        # Combine all the data entries into a single string
        data_string=f"{first_name},{middle_name},{last_name},{contact_no},{subscription_id}"

        # Create a folder if it doesn't exist
        folder_path="member_qrcodes"
        os.makedirs(folder_path, exist_ok=True)

        # Create a QR code containing all the data entries
        qr=qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_string)
        qr.make(fit=True)
        qr_img=qr.make_image(fill_color="black", back_color="white")

        # Specify the file path to save the QR code in the folder
        file_path=os.path.join(folder_path, f"dgrit_{last_name}.png")
        qr_img.save(file_path)

        # After successful registration, send an SMS
        formatted_contact_no=self.contact_no_entry.get()  # Assuming contact_no_entry contains the formatted phone number
        sms_message=f"Hello {first_name}!, You have Successfully Subscribed for {subscription_plan} Plan. Subscription ID:{subscription_id}. Start Date: {start_date} End Date: {end_date}, - D'GRIT GYM"
        self.send_sms(formatted_contact_no, sms_message)

        # Show a success message
        messagebox.showinfo("Registration Successful", "User registered successfully!")

        # Clear all form fields
        for entry in [self.first_name_entry, self.middle_name_entry, self.last_name_entry, self.age_entry,
                      self.address_entry, self.contact_no_entry, self.email_entry,
                      self.emergency_contact_entry, self.subscription_id_entry,
                      self.user_reference_entry]:
            entry.delete(0, tk.END)

    def back_button_event(self):
        self.destroy()


def back_button_event(self):
    # Switch back to the previous frame (e.g., the gym membership frame)
    self.destroy()


class ViewFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Define and configure widgets within the frame
        label=ctk.CTkLabel(self, text="Gym Members' Information", font=("Arial bold", 28))
        label.pack(pady=20, padx=10)

        # Create a connection to the database
        conn=sqlite3.connect('registration_form.db')
        cursor=conn.cursor()

        # Get only the specific columns from the database
        cursor.execute(
            "SELECT id, first_name, middle_name, last_name, contact_no, subscription_id, start_date, end_date, status FROM registration")
        records=cursor.fetchall()

        # Create a frame that holds the table
        table_frame=ctk.CTkFrame(self)
        table_frame.pack(pady=10, padx=10)

        style=ttk.Style()

        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=50,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=5,
                        anchor="center")
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="groove")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        # Create a table to display the records
        self.table=ttk.Treeview(table_frame, columns=(
            "ID", "First Name", "Middle Name", "Last Name", "Contact No", "Subscription ID",
            "Start Date", "End Date", "Status"), show="headings", height=10)
        self.table.pack(side=tk.LEFT)

        self.scrollbar=ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table.configure(yscrollcommand=self.scrollbar.set)

        # Configure the columns
        self.table.heading("ID", text="ID")
        self.table.heading("First Name", text="First Name")
        self.table.heading("Middle Name", text="Middle Name")
        self.table.heading("Last Name", text="Last Name")
        self.table.heading("Contact No", text="Contact No")
        self.table.heading("Subscription ID", text="Subscription ID")
        self.table.heading("Start Date", text="Start Date")
        self.table.heading("End Date", text="End Date")
        self.table.heading("Status", text="Status")

        # Define the column headings and their alignment
        columns=[
            ("ID", "center"),
            ("First Name", "center"),
            ("Middle Name", "center"),
            ("Last Name", "center"),
            ("Contact No", "center"),
            ("Subscription ID", "center"),
            ("Start Date", "center"),
            ("End Date", "center"),
            ("Status", "center")
        ]

        for col, align in columns:
            self.table.heading(col, text=col, anchor=align)
            self.table.column(col, anchor=align)

        self.table.pack(side=tk.LEFT)

        # column width
        columns=[
            ("ID", 50),
            ("First Name", 150),
            ("Middle Name", 150),
            ("Last Name", 150),
            ("Contact No", 150),
            ("Subscription ID", 150),
            ("Start Date", 150),
            ("End Date", 150),
            ("Status", 150)
        ]

        for col, width in columns:
            self.table.column(col, width=width)
            self.table.column("#0", width=0)

        # Add the records to the table
        for record in records:
            self.table.insert("", tk.END, values=record)

        # create a frame to hold sub-frames
        button_frames=ctk.CTkFrame(self)
        button_frames.pack(pady=10, padx=10)

        # Create a frame to hold the edit button
        view_button_frame=ctk.CTkFrame(button_frames)
        view_button_frame.grid(row=0, column=1, padx=10, pady=10)
        # Create an "Edit" button in the second column
        view_button=ctk.CTkButton(view_button_frame, text="View", command=self.edit_record)
        view_button.pack(padx=10, pady=10)

        # Create a "Back" button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.pack(pady=5, side=tk.TOP)

    def back_button_event(self):
        # Switch back to the previous frame (e.g., the gym membership frame)
        self.destroy()

    def edit_record(self):
        selected_item=self.table.selection()
        if selected_item:
            record_data=self.table.item(selected_item)["values"]

            if record_data:
                # Assuming 'id' is the first element and 'first_name' is the second element in the 'values' list
                id_value=record_data[0]
                first_name=record_data[1]
                edit_form=EditForm(self, first_name, id_value, self.table)


class EditForm(ctk.CTkToplevel):
    def __init__(self, master, first_name, id_value, table_reference):
        super().__init__(master)

        # Set the title for the edit form
        self.resizable(False, False)
        self.title("Edit Info")
        self.geometry("500x550")

        # Center-align the window
        window_width=self.winfo_reqwidth()
        window_height=self.winfo_reqheight()
        screen_width=self.winfo_screenwidth()
        screen_height=self.winfo_screenheight()
        x=(screen_width - window_width) // 2
        y=(screen_height - window_height) // 5
        self.geometry(f"+{x}+{y}")

        # Create a connection to the database
        self.conn=sqlite3.connect('registration_form.db')
        self.cursor=self.conn.cursor()

        # Fetch data for the specified member using the provided 'id_value'
        self.cursor.execute("SELECT * FROM registration WHERE id=?", (id_value,))
        self.member_data=self.cursor.fetchone()

        if self.member_data is None:
            messagebox.showerror("Member Not Found", "Member not found in the database.")
            self.destroy()
            return

        # Create and configure widgets within the edit form
        label=ctk.CTkLabel(self, text="Edit Member Information", font=("Arial bold", 20))
        label.pack(pady=10)

        # Create a frame to hold edit form frames
        main_frame=ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)

        # Create a frame to hold the form fields with custom width and height
        edit_frame=ctk.CTkScrollableFrame(main_frame, width=450, height=300)
        edit_frame.pack(pady=10, padx=20)

        # Define a custom font style for entry labels
        label_font=ctk.CTkFont(family="Arial", size=16, weight="bold")

        # Create labels and entry fields for editing the record
        labels=["First Name:", "Middle Name:", "Last Name:", "Age:", "Sex:", "Date of Birth:", "Address:",
                "Nationality:", "Contact No:", "Email Address:", "Emergency Contact No:", "Subscription ID:",
                "Subscription Plan:", "Start Date:", "End Date:", "User Reference:", "Status:"]
        self.entry_fields=[]

        for i, label_text in enumerate(labels):
            label=ctk.CTkLabel(edit_frame, text=label_text, font=label_font)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry=ctk.CTkEntry(edit_frame)
            entry.grid(row=i, column=1, padx=10, pady=5, ipadx=10, ipady=3)
            entry.insert(0, self.member_data[i + 1])  # Fill with data from the database
            self.entry_fields.append(entry)

        # Display the qr code of the member inside the edit form
        qr_code_frame=ctk.CTkFrame(edit_frame)
        qr_code_frame.grid(row=17, column=1, rowspan=16, padx=10, pady=10)

        label=ctk.CTkLabel(edit_frame, text="QR Code:", font=("Arial bold", 16))
        label.grid(row=17, column=0, padx=10, pady=10, sticky="w")

        download_button_frame=ctk.CTkFrame(edit_frame)
        download_button_frame.grid(row=50, column=1, rowspan=50, padx=10, pady=10)

        # create a download button to download the qr code
        download_button=ctk.CTkButton(download_button_frame, text="Download", command=self.download_qr_code)
        download_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Display the qr code from the member_qrcodes folder based on the last name of the member
        qr_code_path=os.path.join("member_qrcodes", f"dgrit_{self.member_data[3]}.png")
        qr_code_image=Image.open(qr_code_path)
        qr_code_image=qr_code_image.resize((200, 200), Image.LANCZOS)
        qr_code_image=ImageTk.PhotoImage(qr_code_image)
        qr_code_label=ctk.CTkLabel(qr_code_frame, text="", image=qr_code_image)
        qr_code_label.image=qr_code_image
        qr_code_label.pack(pady=10, padx=10)

        frame_buttons=ctk.CTkFrame(main_frame)
        frame_buttons.pack(pady=10, padx=10)

        # create frame to hold the buttons
        update_button_frame=ctk.CTkFrame(frame_buttons)
        update_button_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create an "Update" button
        update_button=ctk.CTkButton(update_button_frame, text="Update", command=self.update_record)
        update_button.grid(row=0, column=0, padx=10, pady=10)

        # create a frame to hold the delete button
        delete_button_frame=ctk.CTkFrame(frame_buttons)
        delete_button_frame.grid(row=0, column=1, padx=10, pady=10)

        # Create Red Delete button
        delete_button=ctk.CTkButton(delete_button_frame, text="Delete", fg_color="Red",
                                    text_color=("gray10", "gray90"),
                                    hover_color=("red3", "red4"), command=self.delete_record)
        delete_button.grid(row=0, column=0, padx=10, pady=10)

        # renew button
        renew_button_frame=ctk.CTkFrame(main_frame)
        renew_button_frame.pack(pady=10, padx=10)

        # Create a "Renew" button blue
        renew_button=ctk.CTkButton(renew_button_frame, text="Renew", fg_color="Blue",
                                   text_color=("gray10", "gray90"),
                                   hover_color=("blue3", "blue4"), command=self.renew_membership)
        renew_button.pack(pady=10, padx=10)

        # Store the reference to the 'table' in EditForm
        self.table=table_reference

    def renew_membership(self):
        # Hide the current EditForm
        self.withdraw()

        # Create an instance of RenewSubscriptionFrame
        renew_subscription_frame=RenewSubscriptionFrame(self, self.member_data[0], self.table)

    # Download qr code
    def download_qr_code(self):
        # Download the displayed QR code and save it to the Downloads folder in file explorer
        qr_code_path=os.path.join("member_qrcodes", f"dgrit_{self.member_data[3]}.png")
        qr_code_image=Image.open(qr_code_path)

        # Assuming self.member_data[3] is the unique identifier for the member
        save_path=os.path.join(os.path.expanduser("~"), "Downloads", f"dgrit_{self.member_data[3]}.png")
        qr_code_image.save(save_path)

        # show a success message
        messagebox.showinfo("Download Successful", "QR Code downloaded successfully.")

    def send_sms(self, to_phone_number, message):

        print("PHONE NUMBER", to_phone_number)
        print("MESSAGE", message)

        # delete this one kapag magpupush sa github
        api_key=''

        # # you can change this one kung gusto mo maging priority or bulk. read the docs
        # url='https://api.semaphore.co/api/v4/messages'

        # change to this one if you want na maging priority ang message kaso mas mahal ang credits
        # 2 credits per 160 characters
        url='https://api.semaphore.co/api/v4/priority'

        payload={
            'apikey': api_key,
            'number': to_phone_number,
            'message': message
        }

        # this code will connect with the API and send the data
        try:
            response=requests.post(url, data=payload)

            if response.status_code == 200:

                print("SEND MESSAGE SUCCESS")
                print(response.json())
            else:
                print(response.text)
                print("ERROR SENDING MESSAGE")
                print("STATUS CODE", response.status_code)
        except Exception as e:
            print("failed to send message", e)

    def update_record(self):
        # Get the updated data from the entry fields
        updated_data=[entry.get() for entry in self.entry_fields]

        # Print the updated data to check if the end_date is being updated correctly
        print(f"Updated data: {updated_data}")

        # Validate the updated data
        if not all(updated_data):
            messagebox.showerror("Validation Error", "All fields are required.")
            return

        try:
            # Update the data in the database
            self.cursor.execute('''
                UPDATE registration SET 
                first_name=?, middle_name=?, last_name=?, age=?, sex=?, birth_date=?, address=?, nationality=?,
                contact_no=?, email=?, emergency_contact_no=?, subscription_id=?, subscription_plan=?, start_date=?,
                end_date=?, user_reference=?, status=?
                WHERE id=?
            ''', (*updated_data, self.member_data[0]))

            # Print the updated end_date to check if it's changed
            print(f"Updated end_date: {updated_data[14]}")

            # If end_date is set to the expiration day, update status to "Expired"
            end_date=datetime.strptime(updated_data[14], '%Y-%m-%d').date()
            current_date=datetime.now().date()

            print(f"end_date: {end_date}")
            print(f"current_date: {current_date}")

            if end_date <= current_date:
                print("Updating status to 'Expired'")
                self.cursor.execute("UPDATE registration SET status=? WHERE id=?", ("Expired", self.member_data[0]))
                # SMS for expired
                # get the formatted contact no of the edit form
                formatted_contact_no=self.entry_fields[8].get()
                sms_message="Your gym membership has expired. Renew your subscription to continue accessing D'GRIT GYM."
                self.send_sms(formatted_contact_no, sms_message)

            elif end_date > current_date:
                print("Updating status to 'Ongoing'")
                self.cursor.execute("UPDATE registration SET status=? WHERE id=?", ("Ongoing", self.member_data[0]))

            self.conn.commit()  # Commit the changes to the database
            messagebox.showinfo("Update Successful", "Record updated successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error updating record: {e}")
        finally:
            # Note: Do not close the cursor here to avoid the "Cannot operate on a closed database" error

            # Fetch the updated data from the database
            conn=sqlite3.connect('registration_form.db')
            cursor=conn.cursor()

            try:
                cursor.execute(
                    "SELECT id, first_name, middle_name, last_name, contact_no, subscription_id, start_date, end_date, status FROM registration")
                updated_records=cursor.fetchall()

                # Clear the existing table data
                for item in self.table.get_children():
                    self.table.delete(item)

                # Repopulate the table with the updated records
                for record in updated_records:
                    self.table.insert("", tk.END, values=record)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error fetching updated records: {e}")
            finally:
                # Close the cursor and connection
                cursor.close()
                conn.close()

            # Close the edit form
            self.destroy()

    def delete_record(self):
        # Get the selected item (record) from the Treeview
        selected_item=self.table.selection()
        if selected_item:
            # Prompt the user for confirmation
            confirm=messagebox.askyesno("Delete Record", "Are you sure you want to delete this record?")
            if confirm:
                # Retrieve the data of the selected record from the Treeview
                record_data=self.table.item(selected_item)['values']

                # Delete the selected record from the database based on the 'ID' column
                if record_data:
                    id_value=record_data[0]  # Assuming 'ID' is the first column in the 'values' list
                    conn=sqlite3.connect('registration_form.db')
                    cursor=conn.cursor()
                    try:
                        cursor.execute("DELETE FROM registration WHERE id=?", (id_value,))
                        conn.commit()  # Commit the changes to the database
                        print("Record deleted successfully.")
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"Error deleting record: {e}")
                        print(f"Error deleting record: {e}")
                    finally:
                        cursor.close()
                        conn.close()

                    # Remove the selected item from the Treeview
                    self.table.delete(selected_item)

                    # Fetch the updated data from the database
                    conn=sqlite3.connect('registration_form.db')
                    cursor=conn.cursor()
                    cursor.execute(
                        "SELECT id, first_name, middle_name, last_name, contact_no, subscription_id, start_date, end_date, status FROM registration")
                    updated_records=cursor.fetchall()

                    # Clear the existing table data
                    for item in self.table.get_children():
                        self.table.delete(item)

                    # Repopulate the table with the updated records
                    for record in updated_records:
                        self.table.insert("", tk.END, values=record)

                    # Close the cursor and connection
                    cursor.close()
                    conn.close()

                    self.destroy()


class RenewSubscriptionFrame(ctk.CTkToplevel):
    def __init__(self, master, id_value, table_reference):
        super().__init__(master)

        # Set the title for the edit form
        self.resizable(False, False)
        self.title("Membership Renewal")
        self.geometry("500x500")

        # Center-align the window
        window_width=self.winfo_reqwidth()
        window_height=self.winfo_reqheight()
        screen_width=self.winfo_screenwidth()
        screen_height=self.winfo_screenheight()
        x=(screen_width - window_width) // 2
        y=(screen_height - window_height) // 5
        self.geometry(f"+{x}+{y}")

        # Create and configure widgets within the edit form
        label=ctk.CTkLabel(self, text="Renew Membership", font=("Arial bold", 20))
        label.pack(pady=10)

        # Create a frame to hold edit form frames
        main_frame=ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)

        # Create a frame to hold the form fields with custom width and height
        edit_frame=ctk.CTkFrame(main_frame, width=450, height=450)
        edit_frame.pack(pady=20, padx=20)

        # Define a custom font style for entry labels
        label_font=ctk.CTkFont(family="Arial", size=16, weight="bold")

        # Create labels and entry fields for editing the record
        labels=["ID:", "Contact No:", "Subscription ID:", "Subscription Plan:", "Start Date:", "End Date:"]
        self.entry_fields=[]

        # Create a connection to the database
        self.conn=sqlite3.connect('registration_form.db')
        self.cursor=self.conn.cursor()

        # Fetch data for the specified member using the provided 'id_value'
        self.cursor.execute(
            "SELECT id, contact_no, subscription_id, subscription_plan, start_date, end_date FROM registration WHERE id=?",
            (id_value,))
        self.member_data=self.cursor.fetchone()

        if self.member_data is None:
            messagebox.showerror("Member Not Found", "Member not found in the database.")
            self.destroy()
            return

        for i, label_text in enumerate(labels):
            label=ctk.CTkLabel(edit_frame, text=label_text, font=label_font)
            label.grid(row=i, column=0, padx=10, pady=10, sticky="w")
            entry=ctk.CTkEntry(edit_frame)
            entry.grid(row=i, column=1, padx=10, pady=10, ipadx=10, ipady=3)
            entry.insert(0, self.member_data[i])  # Fill with data from the database
            self.entry_fields.append(entry)

        # Add a member variable to store the reference to the table
        self.table=table_reference

        # Add label and entry for Renew button
        renew_button_frame=ctk.CTkFrame(main_frame)
        renew_button_frame.pack(pady=10, padx=10)

        renew_button=ctk.CTkButton(renew_button_frame, text="Renew", fg_color="Blue",
                                   text_color=("gray10", "gray90"),
                                   hover_color=("blue3", "blue4"), command=self.renew_membership)
        renew_button.pack(pady=10, padx=10)

    def renew_membership(self):
        # Gather data from the form fields
        updated_data=[entry.get() for entry in self.entry_fields]

        # Validate the updated data
        if not all(updated_data):
            messagebox.showerror("Validation Error", "All fields are required.")
            return

        # Update the data in the database
        conn=sqlite3.connect('registration_form.db')
        cursor=conn.cursor()

        try:
            # Logic to renew subscription
            # Set the start date to the current date
            start_date=datetime.now().strftime('%Y-%m-%d')

            # Get the end date and add 1 month
            end_date=self.member_data[4]
            end_date=datetime.strptime(end_date, '%Y-%m-%d')
            end_date=end_date + relativedelta(months=1)
            end_date=end_date.strftime('%Y-%m-%d')

            # Check if subscription is expiring soon and send SMS
            expiration_threshold=datetime.now() + relativedelta(weeks=2)
            print("End Date:", end_date)
            print("Expiration Threshold:", expiration_threshold.strftime('%Y-%m-%d'))

            # Check if the end date is reached and send SMS
            if end_date <= datetime.now().strftime('%Y-%m-%d'):
                print("Sending SMS for expiration (End Date Reached)")
                self.send_sms_expiration(self.member_data[1], start_date, end_date)

            # Update the start_date and end_date in the database
            cursor.execute("UPDATE registration SET start_date=?, end_date=? WHERE id=?",
                           (start_date, end_date, self.member_data[0]))

            # Update the status to 'Ongoing'
            cursor.execute("UPDATE registration SET status=? WHERE id=?", ('Ongoing', self.member_data[0]))

            # Send an SMS to the member for renewal
            formatted_contact_no=self.member_data[1]
            sms_message=f"Hello {self.member_data[2]}!, Your Subscription has been Renewed. Start Date: {start_date} End Date: {end_date}"
            self.send_sms(formatted_contact_no, sms_message)

            conn.commit()

            # Fetch the updated data from the database
            cursor.execute(
                "SELECT id, first_name, middle_name, last_name, contact_no, subscription_id, start_date, end_date, status FROM registration")
            updated_records=cursor.fetchall()

            # Clear the existing table data
            for item in self.table.get_children():
                self.table.delete(item)

            # Repopulate the table with the updated records
            for record in updated_records:
                self.table.insert("", tk.END, values=record)

            print("Subscription renewed successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error renewing subscription: {e}")
            print(f"Error renewing subscription: {e}")
        finally:
            cursor.close()
            messagebox.showinfo("Renewal Successful", "Subscription renewed successfully.")

            self.destroy()

    def send_sms_expiration(self, contact_no, start_date, end_date):
        # Send an SMS to the member for subscription expiration
        formatted_contact_no=contact_no
        sms_message=f"Hello {self.member_data[2]}!, Your subscription is expiring soon. Expiration date: {end_date}."
        self.send_sms(formatted_contact_no, sms_message)

    def send_sms(self, to_phone_number, message):

        print("PHONE NUMBER", to_phone_number)
        print("MESSAGE", message)

        # delete this one kapag magpupush sa github
        api_key=''

        # # you can change this one kung gusto mo maging priority or bulk. read the docs
        # url='https://api.semaphore.co/api/v4/messages'

        # change to this one if you want na maging priority ang message kaso mas mahal ang credits
        # 2 credits per 160 characters
        url='https://api.semaphore.co/api/v4/priority'

        payload={
            'apikey': api_key,
            'number': to_phone_number,
            'message': message
        }

        # this code will connect with the API and send the data
        try:
            response=requests.post(url, data=payload)

            if response.status_code == 200:

                print("SEND MESSAGE SUCCESS")
                print(response.json())
            else:
                print(response.text)
                print("ERROR SENDING MESSAGE")
                print("STATUS CODE", response.status_code)
        except Exception as e:
            print("failed to send message", e)


# ------------- FRAME 3 -----------------------#


def create_take_attendance_frame(frame_3):
    # Define the desired button width and height
    button_width=300
    button_height=300

    # Define the path to the directory containing your image files
    frame_3_icons=os.path.join(os.path.dirname(os.path.realpath(__file__)), "frame_3_icons")

    # Load and resize the images
    register_image=Image.open(os.path.join(frame_3_icons, 'scan_black.png'))
    register_image=register_image.resize((button_width, button_height), Image.LANCZOS)

    view_image=Image.open(os.path.join(frame_3_icons, 'record_black.png'))
    view_image=view_image.resize((button_width, button_height), Image.LANCZOS)

    def scan_qr():
        # When the "Register Members" button is clicked, create and show the registration frame
        scan_qr_frame=ScanFrame(frame_3)
        scan_qr_frame.pack(fill='both', expand=True)

    def view_records():
        # When the "View Members" button is clicked, create and show the view members frame
        view_records_frame=RecordsFrame(frame_3)
        view_records_frame.pack(fill='both', expand=True)

    # Create the buttons with the resized images
    scan_qr_button=ctk.CTkButton(
        master=frame_3,
        text="Scan QR Code",
        image=ImageTk.PhotoImage(register_image),
        compound=tk.TOP,
        command=scan_qr,  # Call the function to open the frame
        width=button_width,
        height=button_height,
        fg_color="#00C957",
        text_color=("gray10", "gray90"),
    )
    scan_qr_button.place(x=150, y=150)

    view_records_button=ctk.CTkButton(
        master=frame_3,
        text="Attendance Records",
        image=ImageTk.PhotoImage(view_image),
        compound=tk.TOP,
        command=view_records,
        width=button_width,
        height=button_height,
        fg_color="#00C957",
        text_color=("gray10", "gray90"),
    )
    view_records_button.place(x=600, y=150)


class ScanFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_ui_elements()

    def create_ui_elements(self):
        # Create and configure UI elements within frame
        label=ctk.CTkLabel(self, text="", font=("Arial bold", 8))
        label.pack(pady=5, padx=10)

        # Define the desired button width and height
        button_width=200
        button_height=200

        # Define the path to the directory containing your image files
        frame_3_icons=os.path.join(os.path.dirname(os.path.realpath(__file__)), "frame_3_icons")

        # Load and resize the images
        time_in_image=Image.open(os.path.join(frame_3_icons, 'time_in.png'))
        time_in_image=time_in_image.resize((button_width, button_height), Image.LANCZOS)

        time_out_image=Image.open(os.path.join(frame_3_icons, 'time_out.png'))
        time_out_image=time_out_image.resize((button_width, button_height), Image.LANCZOS)

        # Create the buttons with the resized images
        time_in_button=ctk.CTkButton(
            master=self,
            text="Time In",
            image=ImageTk.PhotoImage(time_in_image),
            compound=tk.TOP,
            command=self.scan_qr_code_time_in,  # Call the function to open the frame
            width=button_width,
            height=button_height,
            fg_color="#00C957",
            text_color=("gray10", "gray90"),
        )
        time_in_button.place(x=300, y=150)

        time_out_button=ctk.CTkButton(
            master=self,
            text="Time Out",
            image=ImageTk.PhotoImage(time_out_image),
            compound=tk.TOP,
            command=self.scan_qr_code_time_out,
            width=button_width,
            height=button_height,
            fg_color="#00C957",
            text_color=("gray10", "gray90"),
        )
        time_out_button.place(x=550, y=150)

        # create a back button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.place(x=450, y=550)

    def scan_qr_code_time_in(self):
        qr_code_data=self.scan_qr_code()
        if qr_code_data:
            self.record_attendance(qr_code_data, "Time In")

    def scan_qr_code_time_out(self):
        qr_code_data=self.scan_qr_code()
        if qr_code_data:
            self.record_attendance(qr_code_data, "Time Out")

    def send_sms(self, to_phone_number, message):

        print("PHONE NUMBER", to_phone_number)
        print("MESSAGE", message)

        # delete this one kapag magpupush sa github
        api_key=''

        # # you can change this one kung gusto mo maging priority or bulk. read the docs
        # url='https://api.semaphore.co/api/v4/messages'

        # change to this one if you want na maging priority ang message kaso mas mahal ang credits
        # 2 credits per 160 characters
        url='https://api.semaphore.co/api/v4/priority'

        payload={
            'apikey': api_key,
            'number': to_phone_number,
            'message': message
        }

        # this code will connect with the API and send the data
        try:
            response=requests.post(url, data=payload)

            if response.status_code == 200:

                print("SEND MESSAGE SUCCESS")
                print(response.json())
            else:
                print(response.text)
                print("ERROR SENDING MESSAGE")
                print("STATUS CODE", response.status_code)
        except Exception as e:
            print("failed to send message", e)

    @staticmethod
    def record_attendance(member_data, attendance_type):
        try:
            first_name, middle_name, last_name, contact_no, subscription_id=member_data.split(',')
            current_datetime=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

            with sqlite3.connect('attendance_records.db') as conn:
                cursor=conn.cursor()

                if attendance_type == "Time In":
                    cursor.execute('''
                           INSERT INTO attendance_records (first_name, middle_name, last_name, contact_no, subscription_id, time_in)
                           VALUES (?, ?, ?, ?, ?, ?)
                       ''', (first_name, middle_name, last_name, contact_no, subscription_id, current_datetime))

                    send_sms(contact_no,
                             f"Hello {first_name}!, You have Successfully Time In. Subscription ID:{subscription_id}. Time In: {current_datetime}, - D'GRIT GYM")

                elif attendance_type == "Time Out":
                    cursor.execute('''
                           UPDATE attendance_records
                           SET time_out = ?
                           WHERE subscription_id = ? AND time_out IS NULL
                       ''', (current_datetime, subscription_id))

                    send_sms(contact_no,
                             f"Hello {first_name}!, Thank you for coming. See you again! Subscription ID:{subscription_id}. Time Out: {current_datetime}, - D'GRIT GYM")

                conn.commit()
                messagebox.showinfo("Attendance Recorded",
                                    f"{attendance_type} recorded successfully for Subscription ID: {subscription_id}")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error interacting with the database: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    @staticmethod
    def scan_qr_code():
        cap=cv2.VideoCapture(0)

        while True:
            ret, frame=cap.read()
            cv2.imshow('QR Code Scanner', frame)

            detector=cv2.QRCodeDetector()
            data, _, _=detector.detectAndDecode(frame)

            if data:
                cap.release()
                cv2.destroyAllWindows()
                return data

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def back_button_event(self):
        self.destroy()


class RecordsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_ui_elements()

    def create_ui_elements(self):
        # Create a frame to hold the attendance records table
        records_table_frame=ctk.CTkFrame(self)
        records_table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        label=ctk.CTkLabel(records_table_frame, text="Members' Attendance Records", font=("Arial bold", 28))
        label.pack(pady=20, padx=10)

        table_frame=ctk.CTkFrame(records_table_frame)
        table_frame.pack(pady=10, padx=10)

        style=ttk.Style()

        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=50,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=5,
                        anchor="center")
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="groove")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        # Create a Treeview widget to display the attendance records
        self.records_table=ttk.Treeview(table_frame, columns=(
            "First Name", "M.I", "Last Name", "Contact No", "Subscription ID", "Time In", "Time Out"),
                                        show="headings", height=10)
        self.records_table.pack(padx=10, pady=10, side=tk.LEFT)

        # Create a scrollbar for the Treeview
        scrollbar=ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.records_table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.records_table.configure(yscrollcommand=scrollbar.set)

        # Configure the columns
        self.records_table.heading("First Name", text="First Name")
        self.records_table.heading("M.I", text="M.I")
        self.records_table.heading("Last Name", text="Last Name")
        self.records_table.heading("Contact No", text="Contact No")
        self.records_table.heading("Subscription ID", text="Subscription ID")
        self.records_table.heading("Time In", text="Time In")
        self.records_table.heading("Time Out", text="Time Out")

        # Define the column headings and their alignment
        columns=[
            ("First Name", "center"),
            ("M.I", "center"),
            ("Last Name", "center"),
            ("Contact No", "center"),
            ("Subscription ID", "center"),
            ("Time In", "center"),
            ("Time Out", "center")
        ]

        for col, align in columns:
            self.records_table.heading(col, text=col, anchor=align)
            self.records_table.column(col, anchor=align)

        # column width
        columns=[
            ("First Name", 150),
            ("M.I", 100),
            ("Last Name", 150),
            ("Contact No", 150),
            ("Subscription ID", 150),
            ("Time In", 300),
            ("Time Out", 300),
        ]

        for col, width in columns:
            self.records_table.column(col, width=width)
            self.records_table.column("#0", width=0)

        # Fetch attendance records from the database
        self.load_attendance_records()

        # Create attendance record sqlite database if it doesn't exist
        conn=sqlite3.connect('attendance_records.db')
        cursor=conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance_records (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                middle_name TEXT,
                last_name TEXT,
                contact_no TEXT,
                subscription_id TEXT,
                time_in TEXT,
                time_out TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def load_attendance_records(self):
        # Fetch attendance records from the database and populate the Treeview
        conn=sqlite3.connect('attendance_records.db')
        cursor=conn.cursor()

        try:
            cursor.execute('''
                    SELECT first_name, middle_name, last_name, contact_no, subscription_id, time_in, time_out
                    FROM attendance_records
                    ORDER BY DATETIME(time_in) DESC
                ''')
            records=cursor.fetchall()

            for record in records:
                self.records_table.insert("", tk.END, values=record)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching attendance records: {e}")

        finally:
            cursor.close()
            conn.close()

            # create a back button to return to the previous frame
            back_button=ctk.CTkButton(
                self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                hover_color=("red3", "red4"), command=self.back_button_event
            )
            back_button.pack(pady=20, side=tk.BOTTOM)

    def back_button_event(self):
        # Switch back to the previous frame
        self.destroy()


# -------------------------- FRAME 4 ----------------------#

def create_gym_equipment_frame(frame_4):
    # Define the desired button width and height
    button_width=300
    button_height=300

    # Define the path to the directory containing your image files
    frame_4_icons=os.path.join(os.path.dirname(os.path.realpath(__file__)), "frame_4_icons")

    # Load and resize the images
    register_image=Image.open(os.path.join(frame_4_icons, 'dumbell_dark.png'))
    register_image=register_image.resize((button_width, button_height), Image.LANCZOS)

    view_image=Image.open(os.path.join(frame_4_icons, 'list_black.png'))
    view_image=view_image.resize((button_width, button_height), Image.LANCZOS)

    def register_equipment():
        # When the "Register Equipment" button is clicked, create and show the registration frame
        registration_frame=RegistrationEquipment(frame_4)
        registration_frame.pack(fill='both', expand=True)

    def view_member():
        # When the "View Members" button is clicked, create and show the view members frame
        view_equipment_frame=EquipmentRecords(frame_4)
        view_equipment_frame.pack(fill='both', expand=True)

    # Create the buttons with the resized images
    register_equipment_button=ctk.CTkButton(
        master=frame_4,
        text="Register Equipment",
        image=ImageTk.PhotoImage(register_image),
        compound=tk.TOP,
        command=register_equipment,  # Call the function to open the frame
        width=button_width,
        height=button_height,
        fg_color="#00C957",
        text_color=("gray10", "gray90")
    )
    register_equipment_button.place(x=150, y=150)

    view_equipment_button=ctk.CTkButton(
        master=frame_4,
        text="View Equipment Records",
        image=ImageTk.PhotoImage(view_image),
        compound=tk.TOP,
        command=view_member,
        width=button_width,
        height=button_height,
        fg_color="#00C957",
        text_color=("gray10", "gray90")
    )
    view_equipment_button.place(x=600, y=150)


class RegistrationEquipment(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create frame to hold all the widget frames
        outer_frame=ctk.CTkFrame(self)
        outer_frame.pack(padx=10, pady=10)

        widget_frames=ctk.CTkFrame(outer_frame)
        widget_frames.pack(pady=10, padx=10)

        first_frame=ctk.CTkFrame(widget_frames)
        first_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create a frame to hold the form fields
        equipment_info_frame=ctk.CTkFrame(first_frame)
        equipment_info_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create a custom font for labels
        label_font=ctk.CTkFont(family="Arial bold", size=18)  # Adjust the size as
        # Equipment details label
        equipment_details_label=ctk.CTkLabel(equipment_info_frame, text="Equipment Details", font=label_font)
        equipment_details_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        # Name
        equipment_name_label=ctk.CTkLabel(equipment_info_frame, text="Equipment Name:", font=label_font)
        equipment_name_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        equipment_name_entry=ctk.CTkEntry(equipment_info_frame, placeholder_text="Description")
        equipment_name_entry.grid(row=1, column=1, padx=10, pady=10)

        # Brand
        equipment_brand_label=ctk.CTkLabel(equipment_info_frame, text="Brand:", font=label_font)
        equipment_brand_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        equipment_brand_entry=ctk.CTkEntry(equipment_info_frame, placeholder_text="Brand/Manufacturer")
        equipment_brand_entry.grid(row=2, column=1, padx=10, pady=10)

        # Model
        equipment_model_label=ctk.CTkLabel(equipment_info_frame, text="Model:", font=label_font)
        equipment_model_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        equipment_model_entry=ctk.CTkEntry(equipment_info_frame, placeholder_text="Model/Year")
        equipment_model_entry.grid(row=3, column=1, padx=10, pady=10)

        # Serial Number
        equipment_serial_number_label=ctk.CTkLabel(equipment_info_frame, text="Serial No:", font=label_font)
        equipment_serial_number_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        equipment_serial_number_entry=ctk.CTkEntry(equipment_info_frame, placeholder_text="Serial Number")
        equipment_serial_number_entry.grid(row=4, column=1, padx=10, pady=10)

        # quantity
        equipment_quantity_label=ctk.CTkLabel(equipment_info_frame, text="Quantity:", font=label_font)
        equipment_quantity_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        equipment_quantity_entry=ctk.CTkEntry(equipment_info_frame, placeholder_text="Quantity")
        equipment_quantity_entry.grid(row=5, column=1, padx=10, pady=10)

        second_frame=ctk.CTkFrame(widget_frames)
        second_frame.grid(row=0, column=1, padx=10, pady=10)

        second_info_frame=ctk.CTkFrame(second_frame)
        second_info_frame.grid(row=0, column=1, padx=10, pady=10)

        # Create a custom font for labels
        label_font=ctk.CTkFont(family="Arial bold", size=16)  # Adjust the size as

        # Condition
        equipment_condition_label=ctk.CTkLabel(second_info_frame, text="Condition:", font=label_font)
        equipment_condition_label.pack(padx=10, pady=5)
        equipment_condition_options=["New", "Used", "Damaged"]
        equipment_condition_entry=ctk.CTkComboBox(second_info_frame, values=equipment_condition_options)
        equipment_condition_entry.pack(padx=10, pady=5)

        # Equipment type
        equipment_type_label=ctk.CTkLabel(second_info_frame, text="Type:", font=label_font)
        equipment_type_label.pack(padx=10, pady=5)
        equipment_type_options=["Cardio", "Strength", "Endurance", "Flexibility", "Others"]
        equipment_type_entry=ctk.CTkComboBox(second_info_frame, values=equipment_type_options)
        equipment_type_entry.pack(padx=10, pady=5)

        # Equipment Status
        equipment_status_label=ctk.CTkLabel(second_info_frame, text="Status:", font=label_font)
        equipment_status_label.pack(padx=10, pady=5)
        equipment_status_options=["Available", "Unavailable", "Under Maintenance"]
        equipment_status_entry=ctk.CTkComboBox(second_info_frame, values=equipment_status_options)
        equipment_status_entry.pack(padx=10, pady=5)

        # Location
        equipment_location_label=ctk.CTkLabel(second_info_frame, text="Location:", font=label_font)
        equipment_location_label.pack(padx=10, pady=5)
        equipment_location_options=["First Floor", "Second Floor", "Third Floor"]
        equipment_location_entry=ctk.CTkComboBox(second_info_frame, values=equipment_location_options)
        equipment_location_entry.pack(padx=10, pady=5)

        # Training required
        equipment_training_required_label=ctk.CTkLabel(second_info_frame, text="Training Required:", font=label_font)
        equipment_training_required_label.pack(padx=10, pady=5)
        equipment_training_required_options=["Yes", "No"]
        equipment_training_required_entry=ctk.CTkComboBox(second_info_frame, values=equipment_training_required_options)
        equipment_training_required_entry.pack(padx=10, pady=5)

        # Create a "Register" button
        register_button=ctk.CTkButton(outer_frame, text="Register", fg_color="Green",
                                      text_color=("gray10", "gray90"),
                                      hover_color=("green3", "green4"),
                                      command=self.register_equipment_info)
        register_button.pack(pady=15, side=tk.TOP)

        # create a back button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.place(x=450, y=550)

        # Store the Entry fields and other widgets as instance attributes
        self.equipment_name_entry=equipment_name_entry
        self.equipment_brand_entry=equipment_brand_entry
        self.equipment_model_entry=equipment_model_entry
        self.equipment_serial_number_entry=equipment_serial_number_entry
        self.equipment_quantity_entry=equipment_quantity_entry
        self.equipment_condition_entry=equipment_condition_entry
        self.equipment_type_entry=equipment_type_entry
        self.equipment_status_entry=equipment_status_entry
        self.equipment_location_entry=equipment_location_entry
        self.equipment_training_required_entry=equipment_training_required_entry

        # Create a connection to the database (or create it if it doesn't exist)
        conn=sqlite3.connect('register_equipment.db')

        # Create a cursor object to interact with the database
        cursor=conn.cursor()

        # Create a table to store registration information
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS equipment (
                           id INTEGER PRIMARY KEY,
                            equipment_name TEXT NOT NULL,
                            equipment_brand TEXT NOT NULL,
                            equipment_model TEXT NOT NULL,
                            equipment_serial_number TEXT NOT NULL,
                            equipment_quantity TEXT NOT NULL,
                            equipment_condition TEXT NOT NULL,
                            equipment_type TEXT NOT NULL,
                            equipment_status TEXT NOT NULL,
                            equipment_location TEXT NOT NULL,
                            equipment_training_required TEXT NOT NULL
                       )
                   ''')

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

    def register_equipment_info(self):
        # Gather data from the form fields
        equipment_name=self.equipment_name_entry.get()
        equipment_brand=self.equipment_brand_entry.get()
        equipment_model=self.equipment_model_entry.get()
        equipment_serial_number=self.equipment_serial_number_entry.get()
        equipment_quantity=self.equipment_quantity_entry.get()
        equipment_condition=self.equipment_condition_entry.get()
        equipment_type=self.equipment_type_entry.get()
        equipment_status=self.equipment_status_entry.get()
        equipment_location=self.equipment_location_entry.get()
        equipment_training_required=self.equipment_training_required_entry.get()

        # Create a connection to the database
        conn=sqlite3.connect('register_equipment.db')
        cursor=conn.cursor()

        # Insert the data into the database
        cursor.execute('''
                       INSERT INTO equipment (equipment_name, equipment_brand, equipment_model, equipment_serial_number, 
                       equipment_quantity, equipment_condition, equipment_type, equipment_status, equipment_location, equipment_training_required)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ''', (equipment_name, equipment_brand, equipment_model, equipment_serial_number, equipment_quantity,
                         equipment_condition, equipment_type, equipment_status, equipment_location,
                         equipment_training_required))

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        # Show a success message
        messagebox.showinfo("Registration Successful", "equipment registered successfully!")

        # Clear all form fields
        for entry in [self.equipment_name_entry, self.equipment_brand_entry, self.equipment_model_entry,
                      self.equipment_serial_number_entry, self.equipment_quantity_entry, self.equipment_condition_entry,
                      self.equipment_type_entry, self.equipment_status_entry, self.equipment_location_entry,
                      self.equipment_training_required_entry]:
            entry.delete(0, tk.END)

        # Set ComboBox and DateEntry widgets to default or empty values
        self.equipment_condition_entry.set("")
        self.equipment_type_entry.set("")
        self.equipment_status_entry.set("")
        self.equipment_location_entry.set("")
        self.equipment_training_required_entry.set("")
        self.equipment_name_entry.focus()

    def back_button_event(self):
        self.destroy()


class EquipmentRecords(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Define and configure widgets within the frame
        label=ctk.CTkLabel(self, text="Gym Equipment Inventory", font=("Arial bold", 28))
        label.pack(pady=20, padx=10)

        # Create a connection to the database
        conn=sqlite3.connect('register_equipment.db')
        cursor=conn.cursor()

        # Get only the specific columns from the database
        cursor.execute(
            "SELECT id, equipment_name, equipment_quantity, equipment_type, equipment_status, equipment_training_required FROM equipment")
        records=cursor.fetchall()

        # Create a frame that holds the table
        table_frame=ctk.CTkFrame(self)
        table_frame.pack(pady=10, padx=20)

        style=ttk.Style()

        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=50,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=10,
                        anchor="center")
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="groove")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        # Create a table to display the records
        self.table=ttk.Treeview(table_frame, columns=(
            "ID", "Equipment Name", "Quantity", "Type", "Status",
            "Training Required"), show="headings", height=10)
        self.table.pack(side=tk.LEFT)

        self.scrollbar=ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table.configure(yscrollcommand=self.scrollbar.set)

        # Configure the columns
        self.table.heading("ID", text="ID")
        self.table.heading("Equipment Name", text="Equipment Name")
        self.table.heading("Quantity", text="Quantity")
        self.table.heading("Type", text="Type")
        self.table.heading("Status", text="Status")
        self.table.heading("Training Required", text="Training Required")

        # Define the column headings and their alignment
        columns=[
            ("ID", "center"),
            ("Equipment Name", "center"),
            ("Quantity", "center"),
            ("Type", "center"),
            ("Status", "center"),
            ("Training Required", "center")
        ]

        for col, align in columns:
            self.table.heading(col, text=col, anchor=align)
            self.table.column(col, anchor=align)

        # Column width
        columns=[
            ("ID", 100),
            ("Equipment Name", 200),
            ("Quantity", 200),
            ("Type", 200),
            ("Status", 200),
            ("Training Required", 300)
        ]

        for col, width in columns:
            self.table.column(col, width=width)
            self.table.column("#0", width=0)

        self.table.pack(side=tk.LEFT)

        # Add the records to the table
        for record in records:
            self.table.insert("", tk.END, values=record)

        # create a frame to hold sub-frames
        button_frames=ctk.CTkFrame(self)
        button_frames.pack(pady=10, padx=10)

        # Create a frame to hold the edit button
        view_button_frame=ctk.CTkFrame(button_frames)
        view_button_frame.grid(row=0, column=1, padx=10, pady=10)
        # Create an "Edit" button in the second column
        view_button=ctk.CTkButton(view_button_frame, text="View", command=self.edit_record)
        view_button.pack(padx=10, pady=10)

        # create a back button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.place(x=450, y=550)

    def back_button_event(self):
        # Switch back to the previous frame (e.g., the gym membership frame)
        self.destroy()

    def edit_record(self):
        selected_item=self.table.selection()
        if selected_item:
            record_data=self.table.item(selected_item)["values"]

            if record_data:
                # Assuming 'id' is the first element and 'first_name' is the second element in the 'values' list
                id_value=record_data[0]
                equipment_name=record_data[1]
                edit_record=EditRecord(self, equipment_name, id_value, self.table)

    def delete_record(self):
        # Get the selected item (record) from the Treeview
        selected_item=self.table.selection()
        if selected_item:
            # Prompt the user for confirmation
            confirm=messagebox.askyesno("Delete Record", "Are you sure you want to delete this record?")
            if confirm:
                # Retrieve the data of the selected record from the Treeview
                record_data=self.table.item(selected_item)['values']

                # Delete the selected record from the database based on the 'First Name' column
                if record_data:
                    id=record_data[0]  # Assuming 'First Name' is the first column in the 'values' list
                    conn=sqlite3.connect('register_equipment.db')
                    cursor=conn.cursor()
                    try:
                        cursor.execute("DELETE FROM equipment WHERE id=?", (id,))
                        conn.commit()  # Commit the changes to the database
                        print("Record deleted successfully.")
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"Error deleting record: {e}")
                        print(f"Error deleting record: {e}")
                    finally:
                        cursor.close()  # Close the cursor
                        conn.close()  # Close the database connection

                    # Remove the selected item from the Treeview
                    self.table.delete(selected_item)


class EditRecord(ctk.CTkToplevel):
    def __init__(self, master, first_name, id_value, table_reference):
        super().__init__(master)

        # Set the title for the edit form
        self.resizable(False, False)
        self.title("Edit Info")
        self.geometry("500x550")

        # Center-align the window
        window_width=self.winfo_reqwidth()
        window_height=self.winfo_reqheight()
        screen_width=self.winfo_screenwidth()
        screen_height=self.winfo_screenheight()
        x=(screen_width - window_width) // 2
        y=(screen_height - window_height) // 5
        self.geometry(f"+{x}+{y}")

        # Create a connection to the database
        self.conn=sqlite3.connect('register_equipment.db')
        self.cursor=self.conn.cursor()

        # Fetch data for the specified member using the provided 'id_value'
        self.cursor.execute("SELECT * FROM equipment WHERE id=?", (id_value,))
        self.member_data=self.cursor.fetchone()

        if self.member_data is None:
            messagebox.showerror("Member Not Found", "Member not found in the database.")
            self.destroy()
            return

        # Create and configure widgets within the edit form
        label=ctk.CTkLabel(self, text="Edit Equipment Information", font=("Arial bold", 20))
        label.pack(pady=10)

        # Create a frame to hold edit form frames
        main_frame=ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)

        # Create a frame to hold the form fields with custom width and height
        edit_frame=ctk.CTkScrollableFrame(main_frame, width=450, height=300)
        edit_frame.pack(pady=20, padx=20)

        # Define a custom font style for entry labels
        label_font=ctk.CTkFont(family="Arial", size=16, weight="bold")

        # Create labels and entry fields for editing the record
        labels=["Equipment Name:", "Equipment Brand:", "Equipment Model:", "Equipment Serial Number:",
                "Equipment Quantity:", "Equipment Condition:", "Equipment Type:", "Equipment Status:",
                "Equipment Location:",
                "Equipment Training Required:"]
        self.entry_fields=[]

        for i, label_text in enumerate(labels):
            label=ctk.CTkLabel(edit_frame, text=label_text, font=label_font)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry=ctk.CTkEntry(edit_frame)
            entry.grid(row=i, column=1, padx=10, pady=5, ipadx=10, ipady=3)
            entry.insert(0, self.member_data[i + 1])  # Fill with data from the database
            self.entry_fields.append(entry)

        # Create a frame to hold the buttons
        frame_buttons=ctk.CTkFrame(main_frame)
        frame_buttons.pack(pady=20, padx=20)

        # create frame to hold the buttons
        update_button_frame=ctk.CTkFrame(frame_buttons)
        update_button_frame.grid(row=0, column=0, padx=20, pady=20)

        # Create an "Update" button
        update_button=ctk.CTkButton(update_button_frame, text="Update", command=self.update_record)
        update_button.grid(row=0, column=0, padx=20, pady=20)

        # create a frame to hold the delete button
        delete_button_frame=ctk.CTkFrame(frame_buttons)
        delete_button_frame.grid(row=0, column=1, padx=20, pady=20)

        # Create Red Delete button
        delete_button=ctk.CTkButton(delete_button_frame, text="Delete", fg_color="Red",
                                    text_color=("gray10", "gray90"),
                                    hover_color=("red3", "red4"), command=self.delete_record)
        delete_button.grid(row=0, column=0, padx=20, pady=20)

        # Store the reference to the 'table' in EditForm
        self.table=table_reference

    def refresh_table(self):
        # Clear existing records from the table
        for item in self.table.get_children():
            self.table.delete(item)

        # Fetch and add the updated records to the table
        conn=sqlite3.connect('register_equipment.db')
        cursor=conn.cursor()
        cursor.execute(
            "SELECT id, equipment_name, equipment_quantity, equipment_type, equipment_status, equipment_training_required FROM equipment")
        records=cursor.fetchall()
        for record in records:
            self.table.insert("", tk.END, values=record)

        cursor.close()
        conn.close()

    def update_record(self):
        # Get the updated data from the entry fields
        updated_data=[entry.get() for entry in self.entry_fields]

        # Validate the updated data
        if not all(updated_data):
            messagebox.showerror("Validation Error", "All fields are required.")
            return

        # Continue with the update logic
        try:
            self.cursor.execute('''
                    UPDATE equipment SET 
                    equipment_name=?, equipment_brand=?, equipment_model=?, equipment_serial_number=?, equipment_quantity=?,
                     equipment_condition=?, equipment_type=?, equipment_status=?, equipment_location=?, equipment_training_required=?
                ''', tuple(updated_data))

            self.conn.commit()  # Commit the changes to the database
            messagebox.showinfo("Update Successful", "Record updated successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error updating record: {e}")
        finally:
            self.cursor.close()  # Close the cursor
            self.conn.close()  # Close the database connection

        # Call the refresh_table method in the main frame to update the table
        self.refresh_table()

        # Close the edit form
        self.destroy()

    def delete_record(self):
        selected_item=self.table.selection()
        if selected_item:
            confirm=messagebox.askyesno("Delete Record", "Are you sure you want to delete this record?")
            if confirm:
                # Retrieve the data of the selected record from the Treeview
                record_data=self.table.item(selected_item)['values']

                # Delete the selected record from the database based on the 'First Name' column
                if record_data:
                    id_value=record_data[0]  # Assuming 'ID' is the first column in the 'values' list
                    conn=sqlite3.connect('register_equipment.db')
                    cursor=conn.cursor()
                    try:
                        cursor.execute("DELETE FROM equipment WHERE id=?", (id_value,))
                        conn.commit()  # Commit the changes to the database
                        print("Record deleted successfully.")
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"Error deleting record: {e}")
                        print(f"Error deleting record: {e}")
                    finally:
                        cursor.close()
                        conn.close()

            # Call the refresh_table method in the main frame to update the table
            self.refresh_table()

            # Close the edit form
            self.destroy()


# --------------------------FRAME 5 -----------------------------------------#

def create_trainers_frame(frame_5):
    # Define the desired button width and height
    button_width=250
    button_height=250

    # Define the path to the directory containing your image files
    frame_5_icons=os.path.join(os.path.dirname(os.path.realpath(__file__)), "frame_5_icons")

    # Load and resize the images
    register_image=Image.open(os.path.join(frame_5_icons, 'trainer_black.png'))
    register_image=register_image.resize((button_width, button_height), Image.LANCZOS)

    view_image=Image.open(os.path.join(frame_5_icons, 'list_black.png'))
    view_image=view_image.resize((button_width, button_height), Image.LANCZOS)

    take_attendance=Image.open(os.path.join(frame_5_icons, 'scan_black.png'))
    take_attendance=take_attendance.resize((button_width, button_height), Image.LANCZOS)  # Fix this line

    def register_trainer():
        # When the "Register Members" button is clicked, create and show the registration frame
        registration_frame=TrainerFrame(frame_5)
        registration_frame.pack(fill='both', expand=True)

    def view_trainer():
        # When the "View Members" button is clicked, create and show the view members frame
        view_trainer_frame=ViewTrainerFrame(frame_5)
        view_trainer_frame.pack(fill='both', expand=True)

    def trainer_attendance():
        trainer_attendance_frame=TrainerAttendanceFrame(frame_5)
        trainer_attendance_frame.pack(fill='both', expand=True)

    # Create the buttons with the resized images
    register_trainer_button=ctk.CTkButton(
        master=frame_5,
        text="Register Trainer",
        image=ImageTk.PhotoImage(register_image),
        compound=tk.TOP,
        command=register_trainer,  # Call the function to open the frame
        width=button_width,
        height=button_height,
        fg_color="#00C957",
        text_color=("gray10", "gray90")
    )
    register_trainer_button.place(x=100, y=180)

    view_trainer_button=ctk.CTkButton(
        master=frame_5,
        text="View Trainer Records",
        image=ImageTk.PhotoImage(view_image),
        compound=tk.TOP,
        command=view_trainer,
        width=button_width,
        height=button_height,
        fg_color="#00C957",
        text_color=("gray10", "gray90")
    )
    view_trainer_button.place(x=400, y=180)

    trainer_attendance_button=ctk.CTkButton(
        master=frame_5,
        text="Trainer Attendance",
        image=ImageTk.PhotoImage(take_attendance),
        compound=tk.TOP,
        command=trainer_attendance,
        width=button_width,
        height=button_height,
        fg_color="#00C957",
        text_color=("gray10", "gray90")
    )
    trainer_attendance_button.place(x=700, y=180)


class TrainerFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # STEP 1: PERSONAL INFORMATION
        # Define and configure widgets within the frame
        label=ctk.CTkLabel(self, text="Register Trainer", font=("Arial bold", 26))
        label.pack(pady=20, padx=10)

        # outer frame
        outer_frame=ctk.CTkFrame(self)
        outer_frame.pack(pady=20, padx=10)

        # create frame to hold all the widget frames
        widget_frames=ctk.CTkFrame(outer_frame)
        widget_frames.pack(pady=10, padx=10)

        # Create a frame to hold the form fields
        first_frame=ctk.CTkFrame(widget_frames)
        first_frame.grid(row=0, column=0, padx=10, pady=10)
        personal_info_frame=ctk.CTkFrame(first_frame)
        personal_info_frame.pack(pady=10, padx=10)

        # Create a custom font for labels
        label_font=ctk.CTkFont(family="Arial bold", size=16)  # Adjust the size as

        # Name
        first_name_label=ctk.CTkLabel(personal_info_frame, text="First Name:", font=label_font)
        first_name_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        first_name_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your first name")
        first_name_entry.grid(row=2, column=1, padx=20, pady=5)

        middle_name_label=ctk.CTkLabel(personal_info_frame, text="Middle Name:", font=label_font)
        middle_name_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")
        middle_name_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your middle name")
        middle_name_entry.grid(row=3, column=1, padx=20, pady=5)

        last_name_label=ctk.CTkLabel(personal_info_frame, text="Last Name:", font=label_font)
        last_name_label.grid(row=4, column=0, padx=20, pady=5, sticky="w")
        last_name_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your last name")
        last_name_entry.grid(row=4, column=1, padx=20, pady=5)

        # Age
        age_label=ctk.CTkLabel(personal_info_frame, text="Age:", font=label_font)
        age_label.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        age_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your age")
        age_entry.grid(row=6, column=1, padx=20, pady=5)

        # Sex
        sex_label=ctk.CTkLabel(personal_info_frame, text="Sex:", font=label_font)
        sex_label.grid(row=7, column=0, padx=20, pady=5, sticky="w")
        sex_entry=ctk.CTkComboBox(personal_info_frame, values=["Male", "Female", "Other"])
        sex_entry.grid(row=7, column=1, padx=20, pady=5)

        # Create a DateEntry widget for the birthdate
        birth_date_label=ctk.CTkLabel(personal_info_frame, text="Date of Birth:", font=label_font)
        birth_date_label.grid(row=5, column=0, padx=20, pady=5, sticky="w")

        # Use the existing birth_date_entry you created
        self.birth_date_entry=DateEntry(personal_info_frame, width=20, date_pattern="yyyy-mm-dd")
        self.birth_date_entry.grid(row=5, column=1, padx=20, pady=15, sticky="w")

        # Bind the function to the <<DateEntrySelected>> event
        self.birth_date_entry.bind("<<DateEntrySelected>>", self.calculate_age)

        # Address
        address_label=ctk.CTkLabel(personal_info_frame, text="Address:", font=label_font)
        address_label.grid(row=8, column=0, padx=20, pady=5, sticky="w")
        address_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your address")
        address_entry.grid(row=8, column=1, padx=20, pady=5)

        second_frame=ctk.CTkFrame(widget_frames)
        second_frame.grid(row=0, column=1, padx=10, pady=10)
        contact_frame=ctk.CTkFrame(second_frame)
        contact_frame.pack(pady=10, padx=10)

        # Create a custom font for labels
        label_font=ctk.CTkFont(family="Arial bold", size=16)  # Adjust the size as

        # Assuming you have a list of nationalities
        nationalities_list=["Select Nationality", "Filipino", "American", "Chinese", "Japanese", "Korean", "Other"]

        # Nationality Label
        nationality_label=ctk.CTkLabel(contact_frame, text="Nationality:", font=label_font)
        nationality_label.pack(pady=5, padx=10, anchor="w")

        # Create a CTkComboBox widget for nationalities
        nationality_combo=ctk.CTkComboBox(contact_frame, values=nationalities_list)
        nationality_combo.pack(pady=5, padx=10, fill="x")
        nationality_combo.set("Select Nationality")  # Set a default selection

        # Contact No
        contact_no_label=ctk.CTkLabel(contact_frame, text="Contact No:", font=label_font)
        contact_no_label.pack(pady=3, padx=10, anchor="w")
        contact_no_entry=ctk.CTkEntry(contact_frame, placeholder_text="+63 9123456789")
        contact_no_entry.pack(pady=0, padx=10, fill="x")

        # Email Address
        email_label=ctk.CTkLabel(contact_frame, text="Email Address:", font=label_font)
        email_label.pack(pady=0, padx=10, anchor="w")
        email_entry=ctk.CTkEntry(contact_frame, placeholder_text="example@gmail.com")
        email_entry.pack(pady=0, padx=10, fill="x")

        # Emergency Contact No
        emergency_contact_label=ctk.CTkLabel(contact_frame, text="Emergency Contact No:", font=label_font)
        emergency_contact_label.pack(pady=0, padx=10, anchor="w")
        emergency_contact_entry=ctk.CTkEntry(contact_frame, placeholder_text="+63 9123456789")
        emergency_contact_entry.pack(pady=10, padx=10, fill="x")

        # Create a "Register" button
        register_button=ctk.CTkButton(outer_frame, text="Register", fg_color="Green",
                                      text_color=("gray10", "gray90"),
                                      hover_color=("green3", "green4"),
                                      command=self.register_subscription)
        register_button.pack(pady=20, side=tk.TOP)

        # Create a "Back" button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.pack(pady=20, side=tk.TOP)

        # Store the Entry fields and other widgets as instance attributes
        self.first_name_entry=first_name_entry
        self.middle_name_entry=middle_name_entry
        self.last_name_entry=last_name_entry
        self.age_entry=age_entry
        self.sex_entry=sex_entry
        self.address_entry=address_entry
        self.nationality_combo=nationality_combo
        self.contact_no_entry=contact_no_entry
        self.email_entry=email_entry
        self.emergency_contact_entry=emergency_contact_entry

        # Create a connection to the database (or create it if it doesn't exist)
        conn=sqlite3.connect('register_trainer.db')

        # Create a cursor object to interact with the database
        cursor=conn.cursor()

        # Create a table to store registration information
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS trainer (
                           id INTEGER PRIMARY KEY,
                           first_name TEXT,
                           middle_name TEXT,
                           last_name TEXT,
                           age INTEGER,
                           sex TEXT,
                           birth_date DATE,
                           address TEXT,
                           nationality TEXT,
                           contact_no TEXT,
                           email TEXT,
                           emergency_contact_no TEXT
                       )
                   ''')

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

    def calculate_age(self, event):
        # Get the selected birthdate
        birth_date_str=self.birth_date_entry.get()

        try:
            # Extract the date part without the time
            birth_date_str=birth_date_str.split()[0]

            # Convert the birthdate string to a datetime object
            birth_date_obj=datetime.strptime(birth_date_str, '%Y-%m-%d')

            # Calculate the age based on the birthdate
            current_date=datetime.now()
            age=current_date.year - birth_date_obj.year - (
                    (current_date.month, current_date.day) < (birth_date_obj.month, birth_date_obj.day)
            )

            # Update the age entry
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, str(age))
        except ValueError:
            # Handle invalid date format
            messagebox.showerror("Invalid Date", "Please enter a valid date in the format YYYY-MM-DD.")

    def send_sms(self, to_phone_number, message):

        print("PHONE NUMBER", to_phone_number)
        print("MESSAGE", message)

        # delete this one kapag magpupush sa github
        api_key=''

        # # you can change this one kung gusto mo maging priority or bulk. read the docs
        # url='https://api.semaphore.co/api/v4/messages'

        # change to this one if you want na maging priority ang message kaso mas mahal ang credits
        # 2 credits per 160 characters
        url='https://api.semaphore.co/api/v4/priority'

        payload={
            'apikey': api_key,
            'number': to_phone_number,
            'message': message
        }

        # this code will connect with the API and send the data
        try:
            response=requests.post(url, data=payload)

            if response.status_code == 200:

                print("SEND MESSAGE SUCCESS")
                print(response.json())
            else:
                print(response.text)
                print("ERROR SENDING MESSAGE")
                print("STATUS CODE", response.status_code)
        except Exception as e:
            print("failed to send message", e)

    def register_subscription(self):
        # Gather data from the form fields
        first_name=self.first_name_entry.get()
        middle_name=self.middle_name_entry.get()
        last_name=self.last_name_entry.get()
        age=self.age_entry.get()
        sex=self.sex_entry.get()
        birth_date=self.birth_date_entry.get()
        address=self.address_entry.get()
        nationality=self.nationality_combo.get()
        contact_no=self.contact_no_entry.get()
        email=self.email_entry.get()
        emergency_contact_no=self.emergency_contact_entry.get()

        # Validate the data (you can add your validation logic here)

        # Validate the data
        if not (first_name and last_name and age and sex and birth_date and address and
                nationality and contact_no and email and emergency_contact_no):
            messagebox.showerror("Validation Error", "All fields are required.")
            return

        try:
            age=int(age)
        except ValueError:
            messagebox.showerror("Validation Error", "Age must be a valid integer.")
            return

        # Create a connection to the database
        conn=sqlite3.connect('register_trainer.db')
        cursor=conn.cursor()

        # Insert the data into the database
        cursor.execute('''
                       INSERT INTO trainer (first_name, middle_name, last_name, age, sex, birth_date, address,
                                                nationality, contact_no, email, emergency_contact_no)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ''', (first_name, middle_name, last_name, age, sex, birth_date, address, nationality, contact_no,
                         email, emergency_contact_no))

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        # Combine all the data entries into a single string
        data_string=f"{first_name},{middle_name},{last_name},{contact_no}"

        # Create a folder if it doesn't exist
        folder_path="trainer_qrcodes"
        os.makedirs(folder_path, exist_ok=True)

        # Create a QR code containing all the data entries
        qr=qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_string)
        qr.make(fit=True)
        qr_img=qr.make_image(fill_color="black", back_color="white")

        # Specify the file path to save the QR code in the folder
        file_path=os.path.join(folder_path, f"dgrit_trainer_{last_name}.png")
        qr_img.save(file_path)

        # After successful registration, send an SMS
        formatted_contact_no=self.contact_no_entry.get()  # Assuming contact_no_entry contains the formatted phone number
        sms_message=f"Hello {first_name}!, You are registered as a Trainer in D'GRIT Gym."
        self.send_sms(formatted_contact_no, sms_message)

        # Show a success message
        messagebox.showinfo("Registration Successful", "Trainer registered successfully!")

        # Clear all form fields
        for entry in [self.first_name_entry, self.middle_name_entry, self.last_name_entry, self.age_entry,
                      self.address_entry, self.contact_no_entry, self.email_entry,
                      self.emergency_contact_entry]:
            entry.delete(0, tk.END)

        # Set ComboBox and DateEntry widgets to default or empty values
        self.sex_entry.set("Male")
        self.birth_date_entry.set_date("")
        self.nationality_combo.set("Select Nationality")

    def back_button_event(self):
        self.destroy()


class ViewTrainerFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Define and configure widgets within the frame
        label=ctk.CTkLabel(self, text="Trainer Information", font=("Arial bold", 28))
        label.pack(pady=20, padx=10)

        # Create a connection to the database
        conn=sqlite3.connect('register_trainer.db')
        cursor=conn.cursor()

        # Get only the specific columns from the database
        cursor.execute(
            "SELECT id, first_name, middle_name, last_name, age, sex, contact_no FROM trainer")
        records=cursor.fetchall()

        # Create a frame that holds the table
        table_frame=ctk.CTkFrame(self)
        table_frame.pack(pady=10, padx=10)

        style=ttk.Style()

        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=50,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=10,
                        anchor="center")
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="groove")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        # Create a table to display the records
        self.table=ttk.Treeview(table_frame, columns=(
            "ID", "First Name", "Middle Name", "Last Name", "Age", "Sex", "Contact No"), show="headings", height=10)
        self.table.pack(side=tk.LEFT)

        self.scrollbar=ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table.configure(yscrollcommand=self.scrollbar.set)

        # Configure the columns
        self.table.heading("ID", text="ID")
        self.table.heading("First Name", text="First Name")
        self.table.heading("Middle Name", text="Middle Name")
        self.table.heading("Last Name", text="Last Name")
        self.table.heading("Age", text="Age")
        self.table.heading("Sex", text="Sex")

        # Define the column headings and their alignment
        columns=[
            ("ID", "center"),
            ("First Name", "center"),
            ("Middle Name", "center"),
            ("Last Name", "center"),
            ("Age", "center"),
            ("Sex", "center"),
            ("Contact No", "center")
        ]

        for col, align in columns:
            self.table.heading(col, text=col, anchor=align)
            self.table.column(col, anchor=align)

        self.table.pack(side=tk.LEFT)

        # Add the records to the table
        for record in records:
            self.table.insert("", tk.END, values=record)

        # create a frame to hold sub-frames
        button_frames=ctk.CTkFrame(self)
        button_frames.pack(pady=10, padx=10)

        # Create a frame to hold the edit button
        view_button_frame=ctk.CTkFrame(button_frames)
        view_button_frame.grid(row=0, column=1, padx=10, pady=10)
        # Create an "Edit" button in the second column
        view_button=ctk.CTkButton(view_button_frame, text="View", command=self.edit_record)
        view_button.pack(padx=10, pady=10)

        # Create a "Back" button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.pack(pady=5, side=tk.TOP)

    def back_button_event(self):
        # Switch back to the previous frame (e.g., the gym membership frame)
        self.destroy()

    def edit_record(self):
        selected_item=self.table.selection()
        if selected_item:
            record_data=self.table.item(selected_item)["values"]

            if record_data:
                # Assuming 'id' is the first element and 'first_name' is the second element in the 'values' list
                id_value=record_data[0]
                first_name=record_data[1]
                edit_trainer_form=EditTrainerForm(self, first_name, id_value, self.table)

    def delete_record(self):
        # Get the selected item (record) from the Treeview
        selected_item=self.table.selection()
        if selected_item:
            # Prompt the user for confirmation
            confirm=messagebox.askyesno("Delete Record", "Are you sure you want to delete this record?")
            if confirm:
                # Retrieve the data of the selected record from the Treeview
                record_data=self.table.item(selected_item)['values']

                # Delete the selected record from the database based on the 'First Name' column
                if record_data:
                    id=record_data[0]  # Assuming 'First Name' is the first column in the 'values' list
                    conn=sqlite3.connect('register_trainer.db')
                    cursor=conn.cursor()
                    try:
                        cursor.execute("DELETE FROM trainer WHERE id=?", (id,))
                        conn.commit()  # Commit the changes to the database
                        print("Record deleted successfully.")
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"Error deleting record: {e}")
                        print(f"Error deleting record: {e}")
                    finally:
                        cursor.close()  # Close the cursor
                        conn.close()  # Close the database connection

                    # Remove the selected item from the Treeview
                    self.table.delete(selected_item)


class EditTrainerForm(ctk.CTkToplevel):
    def __init__(self, master, first_name, id_value, table_reference):
        super().__init__(master)

        # Set the title for the edit form
        self.resizable(False, False)
        self.title("Edit Info")
        self.geometry("500x550")

        # Center-align the window
        window_width=self.winfo_reqwidth()
        window_height=self.winfo_reqheight()
        screen_width=self.winfo_screenwidth()
        screen_height=self.winfo_screenheight()
        x=(screen_width - window_width) // 2
        y=(screen_height - window_height) // 5
        self.geometry(f"+{x}+{y}")

        # Create a connection to the database
        self.conn=sqlite3.connect('register_trainer.db')
        self.cursor=self.conn.cursor()

        # Fetch data for the specified member using the provided 'id_value'
        self.cursor.execute("SELECT * FROM trainer WHERE id=?", (id_value,))
        self.trainer_data=self.cursor.fetchone()

        if self.trainer_data is None:
            messagebox.showerror("Member Not Found", "Member not found in the database.")
            self.destroy()
            return

        # Create and configure widgets within the edit form
        label=ctk.CTkLabel(self, text="Edit Trainer Information", font=("Arial bold", 20))
        label.pack(pady=10)

        # Create a frame to hold edit form frames
        main_frame=ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)

        # Create a frame to hold the form fields with custom width and height
        edit_frame=ctk.CTkScrollableFrame(main_frame, width=450, height=300)
        edit_frame.pack(pady=20, padx=20)

        # Define a custom font style for entry labels
        label_font=ctk.CTkFont(family="Arial", size=16, weight="bold")

        # Create labels and entry fields for editing the record
        labels=["First Name:", "Middle Name:", "Last Name:", "Age:", "Sex:", "Date of Birth:", "Address:",
                "Nationality:", "Contact No:", "Email Address:", "Emergency Contact No:"]
        self.entry_fields=[]

        for i, label_text in enumerate(labels):
            label=ctk.CTkLabel(edit_frame, text=label_text, font=label_font)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry=ctk.CTkEntry(edit_frame)
            entry.grid(row=i, column=1, padx=10, pady=5, ipadx=10, ipady=3)
            entry.insert(0, self.trainer_data[i + 1])  # Fill with data from the database
            self.entry_fields.append(entry)

        # Display the qr code of the member inside the edit form
        qr_code_frame=ctk.CTkFrame(edit_frame)
        qr_code_frame.grid(row=16, column=1, rowspan=16, padx=10, pady=10)

        label=ctk.CTkLabel(edit_frame, text="QR Code:", font=("Arial bold", 16))
        label.grid(row=16, column=0, padx=10, pady=10, sticky="w")

        download_button_frame=ctk.CTkFrame(edit_frame)
        download_button_frame.grid(row=50, column=1, rowspan=50, padx=10, pady=10)

        # create a download button to download the qr code
        download_button=ctk.CTkButton(download_button_frame, text="Download", command=self.download_qr_code)
        download_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Display the qr code from the member_qrcodes folder based on the last name of the member
        qr_code_path=os.path.join("trainer_qrcodes", f"dgrit_trainer_{self.trainer_data[3]}.png")
        qr_code_image=Image.open(qr_code_path)
        qr_code_image=qr_code_image.resize((200, 200), Image.LANCZOS)
        qr_code_image=ImageTk.PhotoImage(qr_code_image)
        qr_code_label=ctk.CTkLabel(qr_code_frame, text="", image=qr_code_image)
        qr_code_label.image=qr_code_image
        qr_code_label.pack(pady=10, padx=10)

        frame_buttons=ctk.CTkFrame(main_frame)
        frame_buttons.pack(pady=20, padx=20)

        # create frame to hold the buttons
        update_button_frame=ctk.CTkFrame(frame_buttons)
        update_button_frame.grid(row=0, column=0, padx=20, pady=20)

        # Create an "Update" button
        update_button=ctk.CTkButton(update_button_frame, text="Update", command=self.update_record)
        update_button.grid(row=0, column=0, padx=20, pady=20)

        # create a frame to hold the delete button
        delete_button_frame=ctk.CTkFrame(frame_buttons)
        delete_button_frame.grid(row=0, column=1, padx=20, pady=20)

        # Create Red Delete button
        delete_button=ctk.CTkButton(delete_button_frame, text="Delete", fg_color="Red",
                                    text_color=("gray10", "gray90"),
                                    hover_color=("red3", "red4"), command=self.delete_record)
        delete_button.grid(row=0, column=0, padx=20, pady=20)

        # Store the reference to the 'table' in EditForm
        self.table=table_reference

    def download_qr_code(self):
        # Download the displayed QR code and save it to the Downloads folder in file explorer
        qr_code_path=os.path.join("trainer_qrcodes", f"dgrit_trainer_{self.trainer_data[3]}.png")
        qr_code_image=Image.open(qr_code_path)

        # Assuming self.member_data[3] is the unique identifier for the member
        save_path=os.path.join(os.path.expanduser("~"), "Downloads", f"dgrit_trainer_{self.trainer_data[3]}.png")
        qr_code_image.save(save_path)

        # show a success message
        messagebox.showinfo("Download Successful", "QR Code downloaded successfully.")

    def refresh_table(self):
        # Fetch the updated records from the database
        conn=sqlite3.connect('register_trainer.db')
        cursor=conn.cursor()
        cursor.execute("SELECT id, first_name, middle_name, last_name, age, sex, contact_no FROM trainer")
        updated_records=cursor.fetchall()
        conn.close()

        # Clear existing records in the table
        self.table.delete(*self.table.get_children())

        # Insert the updated records into the table
        for record in updated_records:
            self.table.insert("", tk.END, values=record)

    def update_record(self):
        # Get the updated data from the entry fields
        updated_data=[entry.get() for entry in self.entry_fields]

        # Validate the updated data
        if not all(updated_data):
            messagebox.showerror("Validation Error", "All fields are required.")
            return

        # Continue with the update logic
        try:
            self.cursor.execute('''
                    UPDATE trainer SET 
                    first_name=?, middle_name=?, last_name=?, age=?, sex=?, birth_date=?, address=?, nationality=?,
                    contact_no=?, email=?, emergency_contact_no=?
                    WHERE first_name=?
                ''', tuple(updated_data + [self.trainer_data[1]]))

            self.conn.commit()  # Commit the changes to the database
            messagebox.showinfo("Update Successful", "Record updated successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error updating record: {e}")
        finally:
            self.cursor.close()  # Close the cursor
            self.conn.close()  # Close the database connection

        # Call the refresh_table method in the parent ViewTrainerFrame
        self.refresh_table()

        # Close the edit form
        self.destroy()

    def delete_record(self):
        selected_item=self.table.selection()
        if selected_item:
            confirm=messagebox.askyesno("Delete Record", "Are you sure you want to delete this record?")
            if confirm:
                # Retrieve the data of the selected record from the Treeview
                record_data=self.table.item(selected_item)['values']

                # Delete the selected record from the database based on the 'First Name' column
                if record_data:
                    id_value=record_data[0]  # Assuming 'ID' is the first column in the 'values' list
                    conn=sqlite3.connect('register_trainer.db')
                    cursor=conn.cursor()
                    try:
                        cursor.execute("DELETE FROM trainer WHERE id=?", (id_value,))
                        conn.commit()  # Commit the changes to the database
                        print("Record deleted successfully.")
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"Error deleting record: {e}")
                        print(f"Error deleting record: {e}")
                    finally:
                        cursor.close()
                        conn.close()
        # Call the refresh_table method in the parent ViewTrainerFrame
        self.refresh_table()

        # Close the edit form
        self.destroy()


class TrainerAttendanceFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        button_width=200
        button_height=200

        # Define the path to the directory containing your image files
        frame_5_icons=os.path.join(os.path.dirname(os.path.realpath(__file__)), "frame_5_icons")

        # Load and resize the images
        scan_image=Image.open(os.path.join(frame_5_icons, 'scan_black.png'))
        scan_image=scan_image.resize((button_width, button_height), Image.LANCZOS)

        time_out_image=Image.open(os.path.join(frame_5_icons, 'list_black.png'))
        time_out_image=time_out_image.resize((button_width, button_height), Image.LANCZOS)

        # Create the buttons with the resized images
        take_attendance_button=ctk.CTkButton(
            master=self,
            text="Take Attendance",
            image=ImageTk.PhotoImage(scan_image),
            compound=tk.TOP,
            command=self.take_attendance,
            width=button_width,
            height=button_height,
            fg_color="#00C957",
            text_color=("gray10", "gray90")
        )
        take_attendance_button.place(x=300, y=150)

        attendance_records_button=ctk.CTkButton(
            master=self,
            text="View Attendance Records",
            image=ImageTk.PhotoImage(time_out_image),
            compound=tk.TOP,
            command=self.view_attendance_records,
            width=button_width,
            height=button_height,
            fg_color="#00C957",
            text_color=("gray10", "gray90")
        )
        attendance_records_button.place(x=550, y=150)

        # create a back button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.place(x=450, y=550)

    def take_attendance(self):
        # When the "Take Attendance" button is clicked, create and show the ScanQrFrame
        attendance_frame=ScanQrFrame(self)
        attendance_frame.pack(fill='both', expand=True)

    def view_attendance_records(self):
        # When the "View Attendance Records" button is clicked, create and show the AttendanceFrame
        records_frame=AttendanceFrame(self)
        records_frame.pack(fill='both', expand=True)

    def back_button_event(self):
        self.destroy()


class ScanQrFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        button_width=200
        button_height=200

        # Define the path to the directory containing your image files
        frame_5_icons=os.path.join(os.path.dirname(os.path.realpath(__file__)), "frame_5_icons")

        # Load and resize the images
        time_in_image=Image.open(os.path.join(frame_5_icons, 'time_in.png'))
        time_in_image=time_in_image.resize((button_width, button_height), Image.LANCZOS)

        time_out_image=Image.open(os.path.join(frame_5_icons, 'time_out.png'))
        time_out_image=time_out_image.resize((button_width, button_height), Image.LANCZOS)

        # Create the buttons with the resized images
        time_in_button=ctk.CTkButton(
            master=self,
            text="Time In",
            image=ImageTk.PhotoImage(time_in_image),
            compound=tk.TOP,
            command=self.scan_qr_code_time_in,  # Call the function to open the frame
            width=button_width,
            height=button_height,
            fg_color="#00C957",
            text_color=("gray10", "gray90")
        )
        time_in_button.place(x=300, y=200)

        time_out_button=ctk.CTkButton(
            master=self,
            text="Time Out",
            image=ImageTk.PhotoImage(time_out_image),
            compound=tk.TOP,
            command=self.scan_qr_code_time_out,
            width=button_width,
            height=button_height,
            fg_color="#00C957",
            text_color=("gray10", "gray90")
        )
        time_out_button.place(x=550, y=200)

        # create a back button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.pack(pady=20, side=tk.BOTTOM)

    def scan_qr_code_time_in(self):
        qr_code_data=self.scan_qr_code()
        if qr_code_data:
            self.record_attendance(qr_code_data, "Time In")

    def scan_qr_code_time_out(self):
        qr_code_data=self.scan_qr_code()
        if qr_code_data:
            self.record_attendance(qr_code_data, "Time Out")

    def send_sms(self, to_phone_number, message):

        print("PHONE NUMBER", to_phone_number)
        print("MESSAGE", message)

        # delete this one kapag magpupush sa github
        api_key=''

        # # you can change this one kung gusto mo maging priority or bulk. read the docs
        # url='https://api.semaphore.co/api/v4/messages'

        # change to this one if you want na maging priority ang message kaso mas mahal ang credits
        # 2 credits per 160 characters
        url='https://api.semaphore.co/api/v4/priority'

        payload={
            'apikey': api_key,
            'number': to_phone_number,
            'message': message
        }

        # this code will connect with the API and send the data
        try:
            response=requests.post(url, data=payload)

            if response.status_code == 200:

                print("SEND MESSAGE SUCCESS")
                print(response.json())
            else:
                print(response.text)
                print("ERROR SENDING MESSAGE")
                print("STATUS CODE", response.status_code)
        except Exception as e:
            print("failed to send message", e)

    @staticmethod
    def record_attendance(member_data, attendance_type):
        try:
            first_name, middle_name, last_name, contact_no=member_data.split(',')
            current_datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with sqlite3.connect('trainer_attendance_records.db') as conn:
                cursor=conn.cursor()

                if attendance_type == "Time In":
                    cursor.execute('''
                                  INSERT INTO trainer_attendance (first_name, middle_name, last_name, contact_no, time_in)
                                  VALUES (?, ?, ?, ?, ?)
                              ''', (first_name, middle_name, last_name, contact_no, current_datetime))
                    send_sms(contact_no,
                             f"Hello {first_name}!, You have Successfully Time In. Time In: {current_datetime}, - D'GRIT GYM")
                elif attendance_type == "Time Out":
                    cursor.execute('''
                                  UPDATE trainer_attendance
                                  SET time_out = ?
                                  WHERE contact_no = ? AND time_out IS NULL
                              ''', (current_datetime, contact_no))
                    send_sms(contact_no,
                             f"Hello {first_name}!, You have Successfully Time Out. Time In: {current_datetime}, - D'GRIT GYM")

                conn.commit()
                messagebox.showinfo("Attendance Recorded",
                                    f"{attendance_type} recorded successfully")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error interacting with the database: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    @staticmethod
    def scan_qr_code():
        cap=cv2.VideoCapture(0)

        while True:
            ret, frame=cap.read()
            cv2.imshow('QR Code Scanner', frame)

            detector=cv2.QRCodeDetector()
            data, _, _=detector.detectAndDecode(frame)

            if data:
                cap.release()
                cv2.destroyAllWindows()
                return data

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def back_button_event(self):
        # Destroy the current frame and show the parent frame
        self.destroy()


class AttendanceFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create a frame to hold the attendance records table
        records_table_frame=ctk.CTkFrame(self)
        records_table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        table_frame=ctk.CTkFrame(records_table_frame)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        label=ctk.CTkLabel(table_frame, text="Trainer Attendance Records", font=("Arial bold", 28))
        label.pack(pady=20, padx=10)

        table_inner_frame=ctk.CTkFrame(table_frame)
        table_inner_frame.pack(pady=10, padx=20)

        style=ttk.Style()

        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=50,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=10,
                        anchor="center")
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="groove")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        # Create a Treeview widget to display the attendance records
        self.records_table=ttk.Treeview(table_inner_frame, columns=(
            "First Name", "Middle Name", "Last Name", "Contact No", "Time In", "Time Out"),
                                        show="headings", height=10)
        self.records_table.pack(side=tk.LEFT)

        # create a back button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.pack(pady=20, side=tk.BOTTOM)

        # Create a scrollbar for the Treeview
        scrollbar=ttk.Scrollbar(table_inner_frame, orient=tk.VERTICAL, command=self.records_table.yview)
        scrollbar.pack(side=ctk.RIGHT, fill=tk.Y)
        self.records_table.configure(yscrollcommand=scrollbar.set)

        # Configure the columns
        self.records_table.heading("First Name", text="First Name")
        self.records_table.heading("Middle Name", text="Middle Name")
        self.records_table.heading("Last Name", text="Last Name")
        self.records_table.heading("Contact No", text="Contact No")
        self.records_table.heading("Time In", text="Time In")
        self.records_table.heading("Time Out", text="Time Out")

        # Define the column headings and their alignment
        columns=[
            ("First Name", "center"),
            ("Middle Name", "center"),
            ("Last Name", "center"),
            ("Contact No", "center"),
            ("Time In", "center"),
            ("Time Out", "center")
        ]

        for col, align in columns:
            self.records_table.heading(col, text=col, anchor=align)
            self.records_table.column(col, anchor=align)

        # Fetch attendance records from the database
        self.load_attendance_records()

        # Create attendance record sqlite database if it doesn't exist
        conn=sqlite3.connect('trainer_attendance_records.db')
        cursor=conn.cursor()
        cursor.execute('''
               CREATE TABLE IF NOT EXISTS trainer_attendance (
                   id INTEGER PRIMARY KEY,
                   first_name TEXT,
                   middle_name TEXT,
                   last_name TEXT,
                   contact_no TEXT,
                   time_in TEXT,
                   time_out TEXT
               )
           ''')
        conn.commit()
        conn.close()

    def load_attendance_records(self):
        # Fetch attendance records from the database and populate the Treeview
        conn=sqlite3.connect('trainer_attendance_records.db')
        cursor=conn.cursor()

        try:
            cursor.execute(
                'SELECT first_name, middle_name, last_name, contact_no, time_in, time_out FROM trainer_attendance')
            records=cursor.fetchall()

            for record in records:
                self.records_table.insert("", tk.END, values=record)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching trainer attendance records: {e}")

        finally:
            cursor.close()
            conn.close()

    def back_button_event(self):
        # Switch back to the previous frame
        self.destroy()


# -------------------- FRAME 6 --------------------#
def create_visitors_frame(frame_6):
    # Define the desired button width and height
    button_width=350
    button_height=350

    # Define the path to the directory containing your image files
    frame_6_icons=os.path.join(os.path.dirname(os.path.realpath(__file__)), "frame_6_icons")

    # Load and resize the images
    logbook_image=Image.open(os.path.join(frame_6_icons, 'logbook_black.png'))
    logbook_image=logbook_image.resize((button_width, button_height), Image.LANCZOS)

    def register_visitors():
        # When the "Register Members" button is clicked, create and show the registration frame
        registration_frame=LogbookFrame(frame_6)
        registration_frame.pack(fill='both', expand=True)

    # Create the buttons with the resized images
    register_visitor_button=ctk.CTkButton(
        master=frame_6,
        text="Gymers Logbook",
        image=ImageTk.PhotoImage(logbook_image),
        compound=tk.TOP,
        command=register_visitors,  # Call the function to open the frame
        width=button_width,
        height=button_height,
        fg_color="#00C957",
        text_color=("gray10", "gray90")
    )
    register_visitor_button.place(y=130, x=350)


class LogbookFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # STEP 1: PERSONAL INFORMATION
        # Define and configure widgets within the frame
        label=ctk.CTkLabel(self, text="GYMERS DAILY LOG", font=("Arial bold", 26))
        label.pack(pady=25, padx=10)

        # outer frame
        outer_frame=ctk.CTkFrame(self)
        outer_frame.pack(pady=20, padx=10)

        # create frame to hold all the widget frames
        widget_frames=ctk.CTkFrame(outer_frame)
        widget_frames.pack(pady=10, padx=10)

        # Create a frame to hold the form fields
        first_frame=ctk.CTkFrame(widget_frames)
        first_frame.grid(row=0, column=0, padx=10, pady=10)

        personal_info_frame=ctk.CTkFrame(first_frame)
        personal_info_frame.pack(pady=10, padx=10)

        # Create a custom font for labels
        label_font=ctk.CTkFont(family="Arial bold", size=16)  # Adjust the size as

        # Name
        first_name_label=ctk.CTkLabel(personal_info_frame, text="First Name:", font=label_font)
        first_name_label.grid(row=2, column=0, padx=10, pady=15, sticky="w")
        first_name_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your first name")
        first_name_entry.grid(row=2, column=1, padx=10, pady=15)

        middle_name_label=ctk.CTkLabel(personal_info_frame, text="Middle Name:", font=label_font)
        middle_name_label.grid(row=3, column=0, padx=10, pady=15, sticky="w")
        middle_name_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your middle name")
        middle_name_entry.grid(row=3, column=1, padx=10, pady=15)

        last_name_label=ctk.CTkLabel(personal_info_frame, text="Last Name:", font=label_font)
        last_name_label.grid(row=4, column=0, padx=10, pady=15, sticky="w")
        last_name_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your last name")
        last_name_entry.grid(row=4, column=1, padx=10, pady=15)

        # Contact No
        contact_no_label=ctk.CTkLabel(personal_info_frame, text="Contact No:", font=label_font)
        contact_no_label.grid(row=5, column=0, padx=10, pady=15, sticky="w")
        contact_no_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="+63 9123456789")
        contact_no_entry.grid(row=5, column=1, padx=10, pady=15)

        # create a button to register the visitor
        attend_button=ctk.CTkButton(personal_info_frame, text="Attend", fg_color="Green",
                                    text_color=("gray10", "gray90"),
                                    hover_color=("green3", "green4"),
                                    command=self.attend_log)
        attend_button.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        # create a button to delete the visitor
        delete_button=ctk.CTkButton(personal_info_frame, text="Delete", fg_color="Red",
                                    text_color=("gray10", "gray90"),
                                    hover_color=("red3", "red4"),
                                    command=self.delete_log)
        delete_button.grid(row=6, column=1, padx=10, pady=10, sticky="e")

        # Create a frame that holds the table
        table_frame=ctk.CTkFrame(widget_frames)
        table_frame.grid(row=0, column=1, padx=10, pady=10)

        # Create a connection to the database
        conn=sqlite3.connect('visitors_log.db')
        cursor=conn.cursor()

        # Get only the specific columns from the database
        cursor.execute(
            "SELECT first_name, middle_name, last_name, contact_no, time FROM visitors")
        cursor.fetchall()

        style=ttk.Style()

        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=50,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=10,
                        anchor="center")
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="groove")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        # Create a table to display the records
        self.table=ttk.Treeview(table_frame, columns=(
            "First Name", "M.I", "Last Name", "Contact No", "Time"), show="headings", height=10)
        self.table.pack(side=tk.LEFT)

        scrollbar=ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table.configure(yscrollcommand=scrollbar.set)

        # Configure the columns
        self.table.heading("First Name", text="First Name")
        self.table.heading("M.I", text="Middle Name")
        self.table.heading("Last Name", text="Last Name")
        self.table.heading("Contact No", text="Contact No")
        self.table.heading("Time", text="Time")

        # Define the column headings and their alignment
        columns=[
            ("First Name", "center"),
            ("M.I", "center"),
            ("Last Name", "center"),
            ("Contact No", "center"),
            ("Time", "center")
        ]

        for col, align in columns:
            self.table.heading(col, text=col, anchor=align)
            self.table.column(col, anchor=align)

        # column width
        columns=[
            ("First Name", 150),
            ("M.I", 50),
            ("Last Name", 200),
            ("Contact No", 200),
            ("Time", 250)
        ]

        for col, width in columns:
            self.table.column(col, width=width)
            self.table.column("#0", width=0)

        # Back button
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.pack(pady=5, side=tk.TOP)

        # Load data into the table
        self.load_data_to_table()

        # Store the Entry fields and other widgets as instance attributes
        self.first_name_entry=first_name_entry
        self.middle_name_entry=middle_name_entry
        self.last_name_entry=last_name_entry
        self.contact_no_entry=contact_no_entry

        # Create a connection to the database (or create it if it doesn't exist)
        try:
            with sqlite3.connect('visitors_log.db') as conn:
                # Create a cursor object to interact with the database
                cursor=conn.cursor()

                # Create a table to store registration information
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS visitors (
                        id INTEGER PRIMARY KEY,
                        first_name TEXT,
                        middle_name TEXT,
                        last_name TEXT,
                        contact_no TEXT,
                        time TEXT
                    )
                ''')

                # Commit the changes
                conn.commit()

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

    def load_data_to_table(self):
        try:
            # Create a connection to the database
            conn=sqlite3.connect('visitors_log.db')
            cursor=conn.cursor()

            # Fetch records from the database ordered by time in descending order
            cursor.execute(
                "SELECT first_name, middle_name, last_name, contact_no, time FROM visitors ORDER BY time DESC")
            records=cursor.fetchall()

            # Clear existing data in the table
            for row in self.table.get_children():
                self.table.delete(row)

            # Insert fetched records into the table
            for record in records:
                self.table.insert("", "end", values=record)

            # Commit the changes and close the database connection
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            # Handle any potential SQLite errors
            print(f"SQLite error: {e}")

    def send_sms(self, to_phone_number, message):

        print("PHONE NUMBER", to_phone_number)
        print("MESSAGE", message)

        # delete this one kapag magpupush sa github
        api_key=''

        # # you can change this one kung gusto mo maging priority or bulk. read the docs
        # url='https://api.semaphore.co/api/v4/messages'

        # change to this one if you want na maging priority ang message kaso mas mahal ang credits
        # 2 credits per 160 characters
        url='https://api.semaphore.co/api/v4/priority'

        payload={
            'apikey': api_key,
            'number': to_phone_number,
            'message': message
        }

        # this code will connect with the API and send the data
        try:
            response=requests.post(url, data=payload)

            if response.status_code == 200:

                print("SEND MESSAGE SUCCESS")
                print(response.json())
            else:
                print(response.text)
                print("ERROR SENDING MESSAGE")
                print("STATUS CODE", response.status_code)
        except Exception as e:
            print("failed to send message", e)

    def attend_log(self):
        # Gather data from the form fields
        first_name=self.first_name_entry.get()
        middle_name=self.middle_name_entry.get()
        last_name=self.last_name_entry.get()
        contact_no=self.contact_no_entry.get()

        # Validate the data
        if not (first_name and last_name and contact_no):
            messagebox.showerror("Validation Error", "All fields are required.")
            return

        # Create a connection to the database
        conn=sqlite3.connect('visitors_log.db')
        cursor=conn.cursor()

        try:
            # Insert the data into the database with the current date and time in 12-hour format
            current_time=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

            cursor.execute('''
                        INSERT INTO visitors (first_name, middle_name, last_name, contact_no, time)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (first_name, middle_name, last_name, contact_no, current_time))

            # Message that visitor has attended
            self.send_sms(contact_no,
                          f"Hello {first_name}!, Thank You for attending D'GRIT GYM. Time In: {current_time}")

            # Commit the changes and close the database connection
            conn.commit()
            conn.close()

            # Show a success message
            messagebox.showinfo("Attendance Recorded", "Attendance recorded successfully!")

            # Clear all form fields
            for entry in [self.first_name_entry, self.middle_name_entry, self.last_name_entry, self.contact_no_entry]:
                entry.delete(0, tk.END)

            # Load data into the table after recording attendance with the latest entry on top
            self.load_data_to_table()

        except sqlite3.Error as e:
            # Handle any potential SQLite errors
            messagebox.showerror("Database Error", f"Error inserting data: {e}")
            conn.rollback()
            conn.close()

    def delete_log(self):
        # Get the selected item in the table
        selected_item=self.table.selection()

        if not selected_item:
            # If no item is selected, show an error message
            messagebox.showerror("Delete Error", "Please select a record to delete.")
            return

        try:
            # Get the values of the selected item
            values=self.table.item(selected_item, 'values')
            first_name, middle_name, last_name, contact_no, time=values

            # Create a connection to the database
            conn=sqlite3.connect('visitors_log.db')
            cursor=conn.cursor()

            # Delete the selected record from the database
            cursor.execute(
                "DELETE FROM visitors WHERE first_name=? AND middle_name=? AND last_name=? AND contact_no=? AND time=?",
                (first_name, middle_name, last_name, contact_no, time))

            # Commit the changes and close the database connection
            conn.commit()
            conn.close()

            # Remove the selected item from the table
            self.table.delete(selected_item)

            # Show a success message
            messagebox.showinfo("Delete Successful", "Record deleted successfully!")

        except sqlite3.Error as e:
            # Handle any potential SQLite errors
            messagebox.showerror("Database Error", f"Error deleting record: {e}")

    def back_button_event(self):
        self.destroy()


# -------------------- FRAME 7 --------------------#
def create_employee_frame(frame_7):
    # Define the desired button width and height
    button_width=250
    button_height=250

    # Define the path to the directory containing your image files
    frame_7_icons=os.path.join(os.path.dirname(os.path.realpath(__file__)), "frame_7_icons")

    # Load and resize the images
    register_image=Image.open(os.path.join(frame_7_icons, 'register_black.png'))
    register_image=register_image.resize((button_width, button_height), Image.LANCZOS)

    view_image=Image.open(os.path.join(frame_7_icons, 'list_black.png'))
    view_image=view_image.resize((button_width, button_height), Image.LANCZOS)

    attendance_image=Image.open(os.path.join(frame_7_icons, 'scan_black.png'))
    attendance_image=attendance_image.resize((button_width, button_height), Image.LANCZOS)

    def register_employee():
        # When the "Register Members" button is clicked, create and show the registration frame
        registration_frame=RegisterEmployeeFrame(frame_7)
        registration_frame.pack(fill='both', expand=True)

    def view_employee_information():
        # When the "View Members" button is clicked, create and show the view members frame
        view_employee_frame=ViewEmployeeFrame(frame_7)
        view_employee_frame.pack(fill='both', expand=True)

    def take_employee_attendance():
        # When the "View Members" button is clicked, create and show the view members frame
        attendance_frame=EmployeeAttendanceFrame(frame_7)
        attendance_frame.pack(fill='both', expand=True)

    # Create the buttons with the resized images
    register_employee_button=ctk.CTkButton(
        master=frame_7,
        text="Register Employee",
        image=ImageTk.PhotoImage(register_image),
        compound=tk.TOP,
        command=register_employee,  # Call the function to open the frame
        width=button_width,
        height=button_height,
        fg_color="#00C957",
        text_color=("gray10", "gray90")
    )
    register_employee_button.place(x=100, y=180)

    view_employee_button=ctk.CTkButton(
        master=frame_7,
        text="View Employee Information",
        image=ImageTk.PhotoImage(view_image),
        compound=tk.TOP,
        command=view_employee_information,
        width=button_width,
        height=button_height,
        fg_color="#00C957",
        text_color=("gray10", "gray90")
    )
    view_employee_button.place(x=400, y=180)

    attendance_employee_button=ctk.CTkButton(
        master=frame_7,
        text="Employee Attendance",
        image=ImageTk.PhotoImage(attendance_image),
        compound=tk.TOP,
        command=take_employee_attendance,
        width=button_width,
        height=button_height,
        fg_color="#00C957",
        text_color=("gray10", "gray90")
    )
    attendance_employee_button.place(x=700, y=180)


class RegisterEmployeeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # STEP 1: PERSONAL INFORMATION
        # Define and configure widgets within the frame
        label=ctk.CTkLabel(self, text="Register Employee", font=("Arial bold", 26))
        label.pack(pady=20, padx=10)

        # outer frame
        outer_frame=ctk.CTkFrame(self)
        outer_frame.pack(pady=20, padx=10)

        # create frame to hold all the widget frames
        widget_frames=ctk.CTkFrame(outer_frame)
        widget_frames.pack(pady=10, padx=10)

        # Create a frame to hold the form fields
        first_frame=ctk.CTkFrame(widget_frames)
        first_frame.grid(row=0, column=0, padx=10, pady=10)
        personal_info_frame=ctk.CTkFrame(first_frame)
        personal_info_frame.pack(pady=10, padx=10)

        # Create a custom font for labels
        label_font=ctk.CTkFont(family="Arial bold", size=16)  # Adjust the size as

        # Name
        first_name_label=ctk.CTkLabel(personal_info_frame, text="First Name:", font=label_font)
        first_name_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        first_name_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your first name")
        first_name_entry.grid(row=2, column=1, padx=20, pady=5)

        middle_name_label=ctk.CTkLabel(personal_info_frame, text="Middle Name:", font=label_font)
        middle_name_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")
        middle_name_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your middle name")
        middle_name_entry.grid(row=3, column=1, padx=20, pady=5)

        last_name_label=ctk.CTkLabel(personal_info_frame, text="Last Name:", font=label_font)
        last_name_label.grid(row=4, column=0, padx=20, pady=5, sticky="w")
        last_name_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your last name")
        last_name_entry.grid(row=4, column=1, padx=20, pady=5)

        # Age
        age_label=ctk.CTkLabel(personal_info_frame, text="Age:", font=label_font)
        age_label.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        age_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your age")
        age_entry.grid(row=6, column=1, padx=20, pady=5)

        # Sex
        sex_label=ctk.CTkLabel(personal_info_frame, text="Sex:", font=label_font)
        sex_label.grid(row=7, column=0, padx=20, pady=5, sticky="w")
        sex_entry=ctk.CTkComboBox(personal_info_frame, values=["Male", "Female", "Other"])
        sex_entry.grid(row=7, column=1, padx=20, pady=5)

        # Create a DateEntry widget for the birthdate
        birth_date_label=ctk.CTkLabel(personal_info_frame, text="Date of Birth:", font=label_font)
        birth_date_label.grid(row=5, column=0, padx=20, pady=5, sticky="w")

        # Use the existing birth_date_entry you created
        self.birth_date_entry=DateEntry(personal_info_frame, width=20, date_pattern="yyyy-mm-dd")
        self.birth_date_entry.grid(row=5, column=1, padx=20, pady=15, sticky="w")

        # Bind the function to the <<DateEntrySelected>> event
        self.birth_date_entry.bind("<<DateEntrySelected>>", self.calculate_age)

        # Address
        address_label=ctk.CTkLabel(personal_info_frame, text="Address:", font=label_font)
        address_label.grid(row=8, column=0, padx=20, pady=5, sticky="w")
        address_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your address")
        address_entry.grid(row=8, column=1, padx=20, pady=5)

        second_frame=ctk.CTkFrame(widget_frames)
        second_frame.grid(row=0, column=1, padx=10, pady=10)
        contact_frame=ctk.CTkFrame(second_frame)
        contact_frame.pack(pady=10, padx=10)

        # Create a custom font for labels
        label_font=ctk.CTkFont(family="Arial bold", size=16)  # Adjust the size as

        # Assuming you have a list of nationalities
        nationalities_list=["Select Nationality", "Filipino", "American", "Chinese", "Japanese", "Korean", "Other"]

        # Nationality Label
        nationality_label=ctk.CTkLabel(contact_frame, text="Nationality:", font=label_font)
        nationality_label.pack(pady=5, padx=10, anchor="w")

        # Create a CTkComboBox widget for nationalities
        nationality_combo=ctk.CTkComboBox(contact_frame, values=nationalities_list)
        nationality_combo.pack(pady=5, padx=10, fill="x")
        nationality_combo.set("Select Nationality")  # Set a default selection

        # Contact No
        contact_no_label=ctk.CTkLabel(contact_frame, text="Contact No:", font=label_font)
        contact_no_label.pack(pady=3, padx=10, anchor="w")
        contact_no_entry=ctk.CTkEntry(contact_frame, placeholder_text="+63 9123456789")
        contact_no_entry.pack(pady=0, padx=10, fill="x")

        # Email Address
        email_label=ctk.CTkLabel(contact_frame, text="Email Address:", font=label_font)
        email_label.pack(pady=0, padx=10, anchor="w")
        email_entry=ctk.CTkEntry(contact_frame, placeholder_text="example@gmail.com")
        email_entry.pack(pady=0, padx=10, fill="x")

        # Emergency Contact No
        emergency_contact_label=ctk.CTkLabel(contact_frame, text="Emergency Contact No:", font=label_font)
        emergency_contact_label.pack(pady=0, padx=10, anchor="w")
        emergency_contact_entry=ctk.CTkEntry(contact_frame, placeholder_text="+63 9123456789")
        emergency_contact_entry.pack(pady=10, padx=10, fill="x")

        # Create a "Register" button
        register_button=ctk.CTkButton(outer_frame, text="Register", fg_color="Green",
                                      text_color=("gray10", "gray90"),
                                      hover_color=("green3", "green4"),
                                      command=self.register_employees)
        register_button.pack(pady=20, side=tk.TOP)

        # Create a "Back" button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.pack(pady=20, side=tk.TOP)

        # Store the Entry fields and other widgets as instance attributes
        self.first_name_entry=first_name_entry
        self.middle_name_entry=middle_name_entry
        self.last_name_entry=last_name_entry
        self.age_entry=age_entry
        self.sex_entry=sex_entry
        self.address_entry=address_entry
        self.nationality_combo=nationality_combo
        self.contact_no_entry=contact_no_entry
        self.email_entry=email_entry
        self.emergency_contact_entry=emergency_contact_entry

        # Create a connection to the database (or create it if it doesn't exist)
        conn=sqlite3.connect('register_employee.db')

        # Create a cursor object to interact with the database
        cursor=conn.cursor()

        # Create a table to store registration information
        cursor.execute('''
                                 CREATE TABLE IF NOT EXISTS employees (
                                     id INTEGER PRIMARY KEY,
                                     first_name TEXT,
                                     middle_name TEXT,
                                     last_name TEXT,
                                     age INTEGER,
                                     sex TEXT,
                                     birth_date DATE,
                                     address TEXT,
                                     nationality TEXT,
                                     contact_no TEXT,
                                     email TEXT,
                                     emergency_contact_no TEXT
                                 )
                             ''')

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

    def calculate_age(self, event):
        # Get the selected birthdate
        birth_date_str=self.birth_date_entry.get()

        try:
            # Extract the date part without the time
            birth_date_str=birth_date_str.split()[0]

            # Convert the birthdate string to a datetime object
            birth_date_obj=datetime.strptime(birth_date_str, '%Y-%m-%d')

            # Calculate the age based on the birthdate
            current_date=datetime.now()
            age=current_date.year - birth_date_obj.year - (
                    (current_date.month, current_date.day) < (birth_date_obj.month, birth_date_obj.day)
            )

            # Update the age entry
            self.age_entry.delete(0, tk.END)
            self.age_entry.insert(0, str(age))
        except ValueError:
            # Handle invalid date format
            messagebox.showerror("Invalid Date", "Please enter a valid date in the format YYYY-MM-DD.")

    def send_sms(self, to_phone_number, message):

        print("PHONE NUMBER", to_phone_number)
        print("MESSAGE", message)

        # delete this one kapag magpupush sa github
        api_key=''

        # # you can change this one kung gusto mo maging priority or bulk. read the docs
        # url='https://api.semaphore.co/api/v4/messages'

        # change to this one if you want na maging priority ang message kaso mas mahal ang credits
        # 2 credits per 160 characters
        url='https://api.semaphore.co/api/v4/priority'

        payload={
            'apikey': api_key,
            'number': to_phone_number,
            'message': message
        }

        # this code will connect with the API and send the data
        try:
            response=requests.post(url, data=payload)

            if response.status_code == 200:

                print("SEND MESSAGE SUCCESS")
                print(response.json())
            else:
                print(response.text)
                print("ERROR SENDING MESSAGE")
                print("STATUS CODE", response.status_code)
        except Exception as e:
            print("failed to send message", e)

    def register_employees(self):
        # Gather data from the form fields
        first_name=self.first_name_entry.get()
        middle_name=self.middle_name_entry.get()
        last_name=self.last_name_entry.get()
        age=self.age_entry.get()
        sex=self.sex_entry.get()
        birth_date=self.birth_date_entry.get()
        address=self.address_entry.get()
        nationality=self.nationality_combo.get()
        contact_no=self.contact_no_entry.get()
        email=self.email_entry.get()
        emergency_contact_no=self.emergency_contact_entry.get()

        # Validate the data (you can add your validation logic here)

        # Validate the data
        if not (first_name and last_name and age and sex and birth_date and address and
                nationality and contact_no and email and emergency_contact_no):
            messagebox.showerror("Validation Error", "All fields are required.")
            return

        try:
            age=int(age)
        except ValueError:
            messagebox.showerror("Validation Error", "Age must be a valid integer.")
            return

        # Create a connection to the database
        conn=sqlite3.connect('register_employee.db')
        cursor=conn.cursor()

        # Insert the data into the database
        cursor.execute('''
                              INSERT INTO employees (first_name, middle_name, last_name, age, sex, birth_date, address,
                                                       nationality, contact_no, email, emergency_contact_no)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                          ''',
                       (first_name, middle_name, last_name, age, sex, birth_date, address, nationality, contact_no,
                        email, emergency_contact_no))

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        # Combine all the data entries into a single string
        data_string=f"{first_name},{middle_name},{last_name},{contact_no}"

        # Create a folder if it doesn't exist
        folder_path="employee_qrcodes"
        os.makedirs(folder_path, exist_ok=True)

        # Create a QR code containing all the data entries
        qr=qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_string)
        qr.make(fit=True)
        qr_img=qr.make_image(fill_color="black", back_color="white")

        # Specify the file path to save the QR code in the folder
        file_path=os.path.join(folder_path, f"dgrit_employee_{last_name}.png")
        qr_img.save(file_path)

        # After successful registration, send an SMS
        formatted_contact_no=self.contact_no_entry.get()  # Assuming contact_no_entry contains the formatted phone number
        sms_message=f"Hello {first_name}!, You are registered as an Employee of D'GRIT Gym."
        self.send_sms(formatted_contact_no, sms_message)

        # Show a success message
        messagebox.showinfo("Registration Successful", "Employee registered successfully!")

        # Clear all form fields
        for entry in [self.first_name_entry, self.middle_name_entry, self.last_name_entry, self.age_entry,
                      self.address_entry, self.contact_no_entry, self.email_entry,
                      self.emergency_contact_entry]:
            entry.delete(0, tk.END)

        # Set ComboBox and DateEntry widgets to default or empty values
        self.sex_entry.set("Male")
        self.birth_date_entry.set_date("")
        self.nationality_combo.set("Select Nationality")

    def back_button_event(self):
        self.destroy()


class ViewEmployeeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Define and configure widgets within the frame
        label=ctk.CTkLabel(self, text="Employee Information", font=("Arial bold", 28))
        label.pack(pady=20, padx=10)

        # Create a connection to the database
        conn=sqlite3.connect('register_employee.db')
        cursor=conn.cursor()

        # Get only the specific columns from the database
        cursor.execute(
            "SELECT id, first_name, middle_name, last_name, age, sex, contact_no FROM employees")
        records=cursor.fetchall()

        # Create a frame that holds the table
        table_frame=ctk.CTkFrame(self)
        table_frame.pack(pady=10, padx=10)

        style=ttk.Style()

        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=50,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=10,
                        anchor="center")
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="groove")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        # Create a table to display the records
        self.table=ttk.Treeview(table_frame, columns=(
            "ID", "First Name", "Middle Name", "Last Name", "Age", "Sex", "Contact No"), show="headings", height=10)
        self.table.pack(side=tk.LEFT)

        self.scrollbar=ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table.configure(yscrollcommand=self.scrollbar.set)

        # Configure the columns
        self.table.heading("ID", text="ID")
        self.table.heading("First Name", text="First Name")
        self.table.heading("Middle Name", text="Middle Name")
        self.table.heading("Last Name", text="Last Name")
        self.table.heading("Age", text="Age")
        self.table.heading("Sex", text="Sex")

        # Define the column headings and their alignment
        columns=[
            ("ID", "center"),
            ("First Name", "center"),
            ("Middle Name", "center"),
            ("Last Name", "center"),
            ("Age", "center"),
            ("Sex", "center"),
            ("Contact No", "center")
        ]

        for col, align in columns:
            self.table.heading(col, text=col, anchor=align)
            self.table.column(col, anchor=align)

        self.table.pack(side=tk.LEFT)

        # Add the records to the table
        for record in records:
            self.table.insert("", tk.END, values=record)

        # create a frame to hold sub-frames
        button_frames=ctk.CTkFrame(self)
        button_frames.pack(pady=10, padx=10)

        # Create a frame to hold the edit button
        view_button_frame=ctk.CTkFrame(button_frames)
        view_button_frame.grid(row=0, column=1, padx=10, pady=10)
        # Create an "Edit" button in the second column
        view_button=ctk.CTkButton(view_button_frame, text="View", command=self.edit_record)
        view_button.pack(padx=10, pady=10)

        # create a back button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.pack(pady=5, side=tk.TOP)

    def back_button_event(self):
        # Switch back to the previous frame (e.g., the gym membership frame)
        self.destroy()

    def edit_record(self):
        selected_item=self.table.selection()
        if selected_item:
            record_data=self.table.item(selected_item)["values"]

            if record_data:
                # Assuming 'id' is the first element and 'first_name' is the second element in the 'values' list
                id_value=record_data[0]
                first_name=record_data[1]
                edit_employee_form=EditEmployeeForm(self, first_name, id_value, self.table)

    def delete_record(self):
        # Get the selected item (record) from the Treeview
        selected_item=self.table.selection()
        if selected_item:
            # Prompt the user for confirmation
            confirm=messagebox.askyesno("Delete Record", "Are you sure you want to delete this record?")
            if confirm:
                # Retrieve the data of the selected record from the Treeview
                record_data=self.table.item(selected_item)['values']

                # Delete the selected record from the database based on the 'First Name' column
                if record_data:
                    id=record_data[0]  # Assuming 'First Name' is the first column in the 'values' list
                    conn=sqlite3.connect('register_employee.db')
                    cursor=conn.cursor()
                    try:
                        cursor.execute("DELETE FROM employees WHERE id=?", (id,))
                        conn.commit()  # Commit the changes to the database
                        print("Record deleted successfully.")
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"Error deleting record: {e}")
                        print(f"Error deleting record: {e}")
                    finally:
                        cursor.close()  # Close the cursor
                        conn.close()  # Close the database connection

            # Remove the selected item from the Treeview
            self.table.delete(selected_item)


class EditEmployeeForm(ctk.CTkToplevel):
    def __init__(self, master, first_name, id_value, table_reference):
        super().__init__(master)

        # Set the title for the edit form
        self.resizable(False, False)
        self.title("Edit Employee Record")
        self.geometry("500x550")

        # Center-align the window
        window_width=self.winfo_reqwidth()
        window_height=self.winfo_reqheight()
        screen_width=self.winfo_screenwidth()
        screen_height=self.winfo_screenheight()
        x=(screen_width - window_width) // 2
        y=(screen_height - window_height) // 5
        self.geometry(f"+{x}+{y}")

        # Create a connection to the database
        self.conn=sqlite3.connect('register_employee.db')
        self.cursor=self.conn.cursor()

        # Fetch data for the specified member using the provided 'id_value'
        self.cursor.execute("SELECT * FROM employees WHERE id=?", (id_value,))
        self.employee_data=self.cursor.fetchone()

        if self.employee_data is None:
            messagebox.showerror("Employee Not Found", "Employee not found in the database.")
            self.destroy()
            return

        # Create and configure widgets within the edit form
        label=ctk.CTkLabel(self, text="Edit Employee Record", font=("Arial bold", 20))
        label.pack(pady=10)

        # Create a frame to hold edit form frames
        main_frame=ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)

        # Create a frame to hold the form fields with custom width and height
        edit_frame=ctk.CTkScrollableFrame(main_frame, width=450, height=300)
        edit_frame.pack(pady=20, padx=20)

        # Define a custom font style for entry labels
        label_font=ctk.CTkFont(family="Arial", size=16, weight="bold")

        # Create labels and entry fields for editing the record
        labels=["First Name:", "Middle Name:", "Last Name:", "Age:", "Sex:", "Date of Birth:", "Address:",
                "Nationality:", "Contact No:", "Email Address:", "Emergency Contact No:"]
        self.entry_fields=[]

        for i, label_text in enumerate(labels):
            label=ctk.CTkLabel(edit_frame, text=label_text, font=label_font)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry=ctk.CTkEntry(edit_frame)
            entry.grid(row=i, column=1, padx=10, pady=5, ipadx=10, ipady=3)
            entry.insert(0, self.employee_data[i + 1])  # Fill with data from the database
            self.entry_fields.append(entry)

        # Display the qr code of the member inside the edit form
        qr_code_frame=ctk.CTkFrame(edit_frame)
        qr_code_frame.grid(row=16, column=1, rowspan=16, padx=10, pady=10)

        label=ctk.CTkLabel(edit_frame, text="QR Code:", font=("Arial bold", 16))
        label.grid(row=16, column=0, padx=10, pady=10, sticky="w")

        download_button_frame=ctk.CTkFrame(edit_frame)
        download_button_frame.grid(row=50, column=1, rowspan=50, padx=10, pady=10)

        # create a download button to download the qr code
        download_button=ctk.CTkButton(download_button_frame, text="Download", command=self.download_qr_code)
        download_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Display the qr code from the member_qrcodes folder based on the last name of the member
        qr_code_path=os.path.join("employee_qrcodes", f"dgrit_employee_{self.employee_data[3]}.png")
        qr_code_image=Image.open(qr_code_path)
        qr_code_image=qr_code_image.resize((200, 200), Image.LANCZOS)
        qr_code_image=ImageTk.PhotoImage(qr_code_image)
        qr_code_label=ctk.CTkLabel(qr_code_frame, text="", image=qr_code_image)
        qr_code_label.image=qr_code_image
        qr_code_label.pack(pady=10, padx=10)

        frame_buttons=ctk.CTkFrame(main_frame)
        frame_buttons.pack(pady=20, padx=20)

        # create frame to hold the buttons
        update_button_frame=ctk.CTkFrame(frame_buttons)
        update_button_frame.grid(row=0, column=0, padx=20, pady=20)

        # Create an "Update" button
        update_button=ctk.CTkButton(update_button_frame, text="Update", command=self.update_record)
        update_button.grid(row=0, column=0, padx=20, pady=20)

        # create a frame to hold the delete button
        delete_button_frame=ctk.CTkFrame(frame_buttons)
        delete_button_frame.grid(row=0, column=1, padx=20, pady=20)

        # Create Red Delete button
        delete_button=ctk.CTkButton(delete_button_frame, text="Delete", fg_color="Red",
                                    text_color=("gray10", "gray90"),
                                    hover_color=("red3", "red4"), command=self.delete_record)
        delete_button.grid(row=0, column=0, padx=20, pady=20)

        # Store the reference to the 'table' in EditForm
        self.table=table_reference

    def download_qr_code(self):
        # Download the displayed QR code and save it to the Downloads folder in file explorer
        qr_code_path=os.path.join("employee_qrcodes", f"dgrit_employee_{self.employee_data[3]}.png")
        qr_code_image=Image.open(qr_code_path)

        # Assuming self.member_data[3] is the unique identifier for the member
        save_path=os.path.join(os.path.expanduser("~"), "Downloads", f"dgrit_employee_{self.employee_data[3]}.png")
        qr_code_image.save(save_path)

        # show a success message
        messagebox.showinfo("Download Successful", "QR Code downloaded successfully.")

    def update_records(self):
        # Clear existing records in the Treeview
        for item in self.table.get_children():
            self.table.delete(item)

        # Fetch the updated records from the database
        conn=sqlite3.connect('register_employee.db')
        cursor=conn.cursor()
        cursor.execute("SELECT id, first_name, middle_name, last_name, age, sex, contact_no FROM employees")
        records=cursor.fetchall()

        # Add the updated records to the Treeview
        for record in records:
            self.table.insert("", tk.END, values=record)

        # Close the cursor and connection
        cursor.close()
        conn.close()

    def update_record(self):
        # Get the updated data from the entry fields
        updated_data=[entry.get() for entry in self.entry_fields]

        # Validate the updated data
        if not all(updated_data):
            messagebox.showerror("Validation Error", "All fields are required.")
            return

        # Continue with the update logic
        try:
            self.cursor.execute('''
                UPDATE employees SET 
                first_name=?, middle_name=?, last_name=?, age=?, sex=?, birth_date=?, address=?, nationality=?,
                contact_no=?, email=?, emergency_contact_no=?
                WHERE id=?
            ''', (*updated_data, self.employee_data[0]))

            self.conn.commit()  # Commit the changes to the database
            messagebox.showinfo("Update Successful", "Record updated successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error updating record: {e}")
        finally:
            self.cursor.close()  # Close the cursor
            self.conn.close()  # Close the database connection

        # Fetch the updated records from the database
        self.update_records()

        # Close the edit form
        self.destroy()

    def delete_record(self):
        selected_item=self.table.selection()
        if selected_item:
            confirm=messagebox.askyesno("Delete Record", "Are you sure you want to delete this record?")
            if confirm:
                # Retrieve the data of the selected record from the Treeview
                record_data=self.table.item(selected_item)['values']

                # Delete the selected record from the database based on the 'First Name' column
                if record_data:
                    id_value=record_data[0]  # Assuming 'ID' is the first column in the 'values' list
                    conn=sqlite3.connect('register_employee.db')
                    cursor=conn.cursor()
                    try:
                        cursor.execute("DELETE FROM employees WHERE id=?", (id_value,))
                        conn.commit()  # Commit the changes to the database
                        print("Record deleted successfully.")
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"Error deleting record: {e}")
                        print(f"Error deleting record: {e}")
                    finally:
                        cursor.close()
                        conn.close()

            # Fetch the updated records from the database
            self.update_records()

            # Close the edit form
            self.destroy()


class EmployeeAttendanceFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_ui_elements()

    def create_ui_elements(self):
        # Create and configure UI elements within frame
        label=ctk.CTkLabel(self, text="", font=("Arial bold", 8))
        label.pack(pady=5, padx=10)

        # Define the desired button width and height
        button_width=200
        button_height=200

        # Define the path to the directory containing your image files
        frame_7_icons=os.path.join(os.path.dirname(os.path.realpath(__file__)), "frame_7_icons")

        # Load and resize the images
        scan_image=Image.open(os.path.join(frame_7_icons, 'scan_black.png'))
        scan_image=scan_image.resize((button_width, button_height), Image.LANCZOS)

        view_image=Image.open(os.path.join(frame_7_icons, 'list_black.png'))
        view_image=view_image.resize((button_width, button_height), Image.LANCZOS)

        # Create the buttons with the resized images
        take_attendance_button=ctk.CTkButton(
            master=self,
            text="Take Attendance",
            image=ImageTk.PhotoImage(scan_image),
            compound=tk.TOP,
            command=self.take_attendance,  # Call the function to open the frame
            width=button_width,
            height=button_height,
            fg_color="#00C957",
            text_color=("gray10", "gray90")
        )
        take_attendance_button.place(x=300, y=150)

        attendance_records_button=ctk.CTkButton(
            master=self,
            text="View Attendance Records",
            image=ImageTk.PhotoImage(view_image),
            compound=tk.TOP,
            command=self.view_attendance_records,
            width=button_width,
            height=button_height,
            fg_color="#00C957",
            text_color=("gray10", "gray90")
        )
        attendance_records_button.place(x=550, y=150)

        # create a back button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.place(x=450, y=550)

    def take_attendance(self):
        # When the "Register Members" button is clicked, create and show the registration frame
        attendance_frame=EmployeeScanQrFrame(self)
        attendance_frame.pack(fill='both', expand=True)

    def view_attendance_records(self):
        # When the "Register Members" button is clicked, create and show the registration frame
        records_frame=RecordsAttendanceFrame(self)
        records_frame.pack(fill='both', expand=True)

    def back_button_event(self):
        self.destroy()


class EmployeeScanQrFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Define the desired button width and height
        button_width=200
        button_height=200

        # Configure pack to maximize the frame
        self.pack(fill='both', expand=True)

        # Define the path to the directory containing your image files
        frame_7_icons=os.path.join(os.path.dirname(os.path.realpath(__file__)), "frame_7_icons")

        # Load and resize the images
        time_in_image=Image.open(os.path.join(frame_7_icons, 'time_in.png'))
        time_in_image=time_in_image.resize((button_width, button_height), Image.LANCZOS)

        time_out_image=Image.open(os.path.join(frame_7_icons, 'time_out.png'))
        time_out_image=time_out_image.resize((button_width, button_height), Image.LANCZOS)

        # Create the buttons with the resized images
        time_in_button=ctk.CTkButton(
            master=self,
            text="Time In",
            image=ImageTk.PhotoImage(time_in_image),
            compound=tk.TOP,
            command=self.scan_qr_code_time_in,  # Call the function to open the frame
            width=button_width,
            height=button_height,
            fg_color="#00C957",
            text_color=("gray10", "gray90")
        )
        time_in_button.place(x=300, y=150)

        time_out_button=ctk.CTkButton(
            master=self,
            text="Time Out",
            image=ImageTk.PhotoImage(time_out_image),
            compound=tk.TOP,
            command=self.scan_qr_code_time_out,
            width=button_width,
            height=button_height,
            fg_color="#00C957",
            text_color=("gray10", "gray90")
        )
        time_out_button.place(x=550, y=150)

        # create a back button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.pack(pady=20, side=tk.BOTTOM)

    def scan_qr_code_time_in(self):
        qr_code_data=self.scan_qr_code()
        if qr_code_data:
            self.record_attendance(qr_code_data, "Time In")

    def scan_qr_code_time_out(self):
        qr_code_data=self.scan_qr_code()
        if qr_code_data:
            self.record_attendance(qr_code_data, "Time Out")

    def send_sms(self, to_phone_number, message):

        print("PHONE NUMBER", to_phone_number)
        print("MESSAGE", message)

        # delete this one kapag magpupush sa github
        api_key=''

        # # you can change this one kung gusto mo maging priority or bulk. read the docs
        # url='https://api.semaphore.co/api/v4/messages'

        # change to this one if you want na maging priority ang message kaso mas mahal ang credits
        # 2 credits per 160 characters
        url='https://api.semaphore.co/api/v4/priority'

        payload={
            'apikey': api_key,
            'number': to_phone_number,
            'message': message
        }

        # this code will connect with the API and send the data
        try:
            response=requests.post(url, data=payload)

            if response.status_code == 200:

                print("SEND MESSAGE SUCCESS")
                print(response.json())
            else:
                print(response.text)
                print("ERROR SENDING MESSAGE")
                print("STATUS CODE", response.status_code)
        except Exception as e:
            print("failed to send message", e)

    @staticmethod
    def record_attendance(member_data, attendance_type):
        try:
            first_name, middle_name, last_name, contact_no=member_data.split(',')
            current_datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with sqlite3.connect('employee_attendance_records.db') as conn:
                cursor=conn.cursor()

                if attendance_type == "Time In":
                    cursor.execute('''
                                      INSERT INTO employee_attendance (first_name, middle_name, last_name, contact_no, time_in)
                                      VALUES (?, ?, ?, ?, ?)
                                  ''', (first_name, middle_name, last_name, contact_no, current_datetime))
                    send_sms(contact_no,
                             f"Hello {first_name}!, You have Successfully Time In. Time In: {current_datetime}, - D'GRIT GYM")
                elif attendance_type == "Time Out":
                    cursor.execute('''
                                      UPDATE employee_attendance
                                      SET time_out = ?
                                      WHERE contact_no = ? AND time_out IS NULL
                                  ''', (current_datetime, contact_no))
                    send_sms(contact_no,
                             f"Hello {first_name}!, You have Successfully Time Out. Time Out: {current_datetime}, - D'GRIT GYM")

                conn.commit()
                messagebox.showinfo("Attendance Recorded",
                                    f"{attendance_type} recorded successfully")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error interacting with the database: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    @staticmethod
    def scan_qr_code():
        cap=cv2.VideoCapture(0)

        while True:
            ret, frame=cap.read()
            cv2.imshow('QR Code Scanner', frame)

            detector=cv2.QRCodeDetector()
            data, _, _=detector.detectAndDecode(frame)

            if data:
                cap.release()
                cv2.destroyAllWindows()
                return data

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def back_button_event(self):
        self.destroy()


class RecordsAttendanceFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create a frame to hold the attendance records table
        records_table_frame=ctk.CTkFrame(self)
        records_table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        table_frame=ctk.CTkFrame(records_table_frame)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        label=ctk.CTkLabel(table_frame, text="Employee Attendance Records", font=("Arial bold", 28))
        label.pack(pady=20, padx=10)

        inner_table_frame=ctk.CTkFrame(table_frame)
        inner_table_frame.pack(pady=10, padx=20)

        style=ttk.Style()

        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=50,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=10,
                        anchor="center")
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="groove")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        # Create a Treeview widget to display the attendance records
        self.records_table=ttk.Treeview(inner_table_frame, columns=(
            "First Name", "Middle Name", "Last Name", "Contact No", "Time In", "Time Out"),
                                        show="headings", height=10)
        self.records_table.pack(side=tk.LEFT)

        # Create a scrollbar for the Treeview
        scrollbar=ttk.Scrollbar(inner_table_frame, orient=tk.VERTICAL, command=self.records_table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.records_table.configure(yscrollcommand=scrollbar.set)

        # back button
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.pack(pady=20, side=tk.BOTTOM)

        # Configure the columns
        self.records_table.heading("First Name", text="First Name")
        self.records_table.heading("Middle Name", text="Middle Name")
        self.records_table.heading("Last Name", text="Last Name")
        self.records_table.heading("Contact No", text="Contact No")
        self.records_table.heading("Time In", text="Time In")
        self.records_table.heading("Time Out", text="Time Out")

        # Define the column headings and their alignment
        columns=[
            ("First Name", "center"),
            ("Middle Name", "center"),
            ("Last Name", "center"),
            ("Contact No", "center"),
            ("Time In", "center"),
            ("Time Out", "center")
        ]

        for col, align in columns:
            self.records_table.heading(col, text=col, anchor=align)
            self.records_table.column(col, anchor=align)

        # Fetch attendance records from the database
        self.load_attendance_records()

        # Create attendance record sqlite database if it doesn't exist
        conn=sqlite3.connect('employee_attendance_records.db')
        cursor=conn.cursor()
        cursor.execute('''
                   CREATE TABLE IF NOT EXISTS employee_attendance (
                       id INTEGER PRIMARY KEY,
                       first_name TEXT,
                       middle_name TEXT,
                       last_name TEXT,
                       contact_no TEXT,
                       time_in TEXT,
                       time_out TEXT
                   )
               ''')
        conn.commit()
        conn.close()

    def load_attendance_records(self):
        # Fetch attendance records from the database and populate the Treeview
        conn=sqlite3.connect('employee_attendance_records.db')
        cursor=conn.cursor()

        try:
            cursor.execute(
                'SELECT first_name, middle_name, last_name, contact_no, time_in, time_out FROM employee_attendance')
            records=cursor.fetchall()

            for record in records:
                self.records_table.insert("", tk.END, values=record)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching employee attendance records: {e}")

        finally:
            cursor.close()
            conn.close()

    def back_button_event(self):
        # Switch back to the previous frame
        self.destroy()


def create_account_management_frame(frame_8):
    # Create the main frame for account management
    form_frame=ctk.CTkFrame(frame_8)
    form_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Add a title label to the form frame
    label=ctk.CTkLabel(form_frame, text="", font=("Agency FB bold", 24))
    label.pack(pady=25, padx=10)

    # Create a frame for input fields
    fields_frame=ctk.CTkFrame(form_frame)
    fields_frame.pack(pady=20, padx=20)

    # Create a sub-frame for information
    info_frame=ctk.CTkFrame(fields_frame)
    info_frame.grid(row=0, column=0, padx=20, pady=20)

    # Create a sub-sub-frame for organizing input fields
    sub_frame=ctk.CTkFrame(info_frame)
    sub_frame.pack(pady=20, padx=20)

    # Set the font for labels
    label_font=ctk.CTkFont(family="Arial bold", size=24)

    # Add Full Name entry
    full_name_label=ctk.CTkLabel(sub_frame, text="Full Name:", font=label_font)
    full_name_label.grid(row=1, column=0, padx=20, pady=20)
    full_name_entry=ctk.CTkEntry(sub_frame, placeholder_text="Enter your full name")
    full_name_entry.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

    # Add Contact Number entry
    contact_no_label=ctk.CTkLabel(sub_frame, text="Contact No:", font=label_font)
    contact_no_label.grid(row=2, column=0, padx=20, pady=20)
    contact_no_entry=ctk.CTkEntry(sub_frame, placeholder_text="Enter your contact number")
    contact_no_entry.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

    # Add Username entry
    username_label=ctk.CTkLabel(sub_frame, text="Username:", font=label_font)
    username_label.grid(row=3, column=0, padx=20, pady=20)
    username_entry=ctk.CTkEntry(sub_frame, placeholder_text="Enter your new username")
    username_entry.grid(row=3, column=1, padx=20, pady=20, sticky="ew")

    # Add Password entry
    password_label=ctk.CTkLabel(sub_frame, text="Password:", font=label_font)
    password_label.grid(row=4, column=0, padx=20, pady=20)
    password_entry=ctk.CTkEntry(sub_frame, placeholder_text='Enter your new password', show="*")
    password_entry.grid(row=4, column=1, padx=20, pady=20, sticky="ew")

    register_button=ctk.CTkButton(
        info_frame,
        text="Create",
        command=lambda: register(
            full_name_entry.get(),  # Add this line to include full name
            contact_no_entry.get(),  # Assuming you have a contact_no_entry widget
            username_entry.get(),
            password_entry.get(),
            full_name_entry,
            contact_no_entry,
            username_entry,
            password_entry
        )
    )
    register_button.pack(pady=10, padx=10)


def register(full_name, contact_no, username, password, contact_no_entry, full_name_entry, username_entry,
             password_entry):
    # Check if the username and password meet your criteria (uppercase, lowercase, symbol)
    if not is_valid(username, password):
        messagebox.showerror("Invalid Data",
                             "Username and Password must be mixed with uppercase and lowercase letters and numbers/symbols.")
        return

    # Validate the contact number format (11 digits starting with 0)
    if not (contact_no.startswith('0') and len(contact_no) == 11 and contact_no[1:].isdigit()):
        messagebox.showerror("Invalid Contact Number",
                             "Please enter a valid contact number starting with 0 and 11 digits long (e.g., 09123456789).")
        return

    # Connect to SQLite database
    conn=sqlite3.connect('registered_users.db')
    cursor=conn.cursor()

    try:
        # Create a table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                contact_no TEXT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Check if the username already exists
        cursor.execute('SELECT * FROM accounts WHERE username = ?', (username,))
        existing_user=cursor.fetchone()
        if existing_user:
            messagebox.showerror("Username Exists", "Username already exists. Please choose a different one.")
        else:
            # Insert the data into the database including full name and contact number
            cursor.execute('INSERT INTO accounts (full_name, contact_no, username, password) VALUES (?, ?, ?, ?)',
                           (full_name, contact_no, username, password))
            conn.commit()

            messagebox.showinfo("Registration Successful", "Your account has been registered successfully.")

            # Clear the entry fields after successful registration
            full_name_entry.delete(0, 'end')
            contact_no_entry.delete(0, 'end')
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')

    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Registration Error", "An error occurred during registration.")
    finally:
        conn.close()


def is_valid(username, password):
    # You can define your criteria here for a valid username and password
    # For example, it should contain at least one uppercase, one lowercase, and one symbol
    # Modify this according to your requirements.
    has_upper=any(c.isupper() for c in username)
    has_lower=any(c.islower() for c in username)
    has_symbol=any(c for c in username if not c.isalnum())

    if not (has_upper and has_lower and has_symbol) or len(password) < 8:
        return False

    return True


def center_window(window, width, height):
    screen_width=window.winfo_screenwidth()
    screen_height=window.winfo_screenheight()
    x=(screen_width / 1.5) - (width / 1.5)
    y=(screen_height / 2) - (height / 2)
    window.geometry(f"{int(width)}x{int(height)}+{int(x)}+{int(y)}")


def send_sms(to_phone_number, message):
    print("PHONE NUMBER", to_phone_number)
    print("MESSAGE", message)

    api_key=''
    url='https://api.semaphore.co/api/v4/priority'  # Using priority endpoint

    payload={
        'apikey': api_key,
        'number': to_phone_number,
        'message': message
    }

    try:
        response=requests.post(url, data=payload)

        if response.status_code == 200:
            print("SEND MESSAGE SUCCESS")
            print(response.json())
        else:
            print(response.text)
            print("ERROR SENDING MESSAGE")
            print("STATUS CODE", response.status_code)
    except Exception as e:
        print("failed to send message", e)


def is_valid_password(password):
    # Add your password policy checks here
    # For example, you can require at least one uppercase letter, one lowercase letter, one digit, and one special character.
    return (
            any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)
    )


def forgot_password():
    otp=''.join(random.choices(string.digits, k=6))

    while True:
        user_phone_number=simpledialog.askstring('Enter Phone Number', 'Enter your phone number (e.g., 09123456789):')

        if user_phone_number is None:
            break
        elif user_phone_number.startswith('0') and len(user_phone_number) == 11 and user_phone_number[1:].isdigit():
            conn=sqlite3.connect('registered_users.db')
            cursor=conn.cursor()
            cursor.execute('SELECT * FROM accounts WHERE contact_no = ?', (user_phone_number,))
            registered_user=cursor.fetchone()
            conn.close()

            if registered_user:
                send_sms(user_phone_number, f'Your OTP is: {otp}')

                entered_otp=simpledialog.askstring('Enter OTP', 'Enter the OTP sent to your phone:', show='*')

                if entered_otp is None:
                    break
                elif entered_otp == otp:
                    new_username=simpledialog.askstring('New Username', 'Enter your new username:')
                    new_password=simpledialog.askstring('New Password', 'Enter your new password:', show='*')

                    if new_username and new_password:
                        if is_valid_password(new_password):
                            conn=sqlite3.connect('registered_users.db')
                            cursor=conn.cursor()
                            cursor.execute('UPDATE accounts SET username = ?, password = ? WHERE contact_no = ?',
                                           (new_username, new_password, user_phone_number))
                            # send sms to the user's contact number to notify them of the username and password reset
                            send_sms(user_phone_number,
                                     f'Your username and password have been reset. Username: {new_username}. Password:{new_password}.')
                            conn.commit()
                            conn.close()
                            messagebox.showinfo('Password Reset Successful',
                                                'Your password has been reset successfully.')
                        else:
                            messagebox.showerror('Invalid Password', 'Password must meet the specified policy.')
                    else:
                        messagebox.showerror('Error', 'New username and password are required.')
                    break
                else:
                    messagebox.showerror('Invalid OTP', 'The entered OTP is incorrect.')
            else:
                messagebox.showerror('Unregistered Phone Number', 'The entered phone number is not registered.')
                break
        else:
            messagebox.showerror('Invalid Phone Number',
                                 'Please enter a valid phone number starting with 0 and 11 digits long (e.g., 09123456789).')


# Create the login system
def create_login_window():
    def login():
        username=user_entry.get()
        password=user_pass.get()

        if username == "" or password == "":
            messagebox.showerror(title="Login Failed", message="Please enter both username and password")
            return

        # Connect to SQLite database
        conn=sqlite3.connect('registered_users.db')
        cursor=conn.cursor()

        # Check if the provided username and password match an account in the database
        cursor.execute('SELECT * FROM accounts WHERE username = ? AND password = ?', (username, password))
        user_data=cursor.fetchone()
        conn.close()

        if user_data:
            messagebox.showinfo(title="Login Successful", message="You have logged in Successfully")
            login_window.destroy()
            app=MainApp()
            app.mainloop()
        else:
            messagebox.showerror(title="Login Failed", message="Invalid Username and password")

    def toggle_password_visibility():
        # Toggle password visibility
        if user_pass.cget("show") == "":
            user_pass.configure(show="*")
        else:
            user_pass.configure(show="")

    login_window=ctk.CTk()
    login_window.geometry("400x550")
    login_window.title("D'Grit Gym Management System")
    login_window.resizable(False, False)

    # Calculate the position to center the login window
    center_window(login_window, 400, 550)

    # Load and set the background image
    background_image=ImageTk.PhotoImage(file="pat.png")
    background_label=tk.Label(login_window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    logo_image=ImageTk.PhotoImage(file="test_images/gym_dark.png")
    label=ctk.CTkLabel(login_window, text="", font=("arial", 20), image=logo_image, compound=tk.LEFT)
    label.pack(pady=20)

    frame=ctk.CTkFrame(master=login_window)
    frame.pack(pady=30, padx=40, fill='both', expand=True)

    label=ctk.CTkLabel(master=frame, text="Login", font=("Arial bold", 18))
    label.pack(pady=12, padx=10)

    user_entry=ctk.CTkEntry(master=frame, placeholder_text="Username")
    user_entry.pack(pady=12, padx=10)

    user_pass=ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
    user_pass.pack(pady=12, padx=10)

    show_password_checkbox=ctk.CTkCheckBox(master=frame, text='Show Password', command=toggle_password_visibility)
    show_password_checkbox.pack(pady=12, padx=10)

    login_button=ctk.CTkButton(master=frame, text='Login', command=login)
    login_button.pack(pady=12, padx=10)

    forgot_password_button=ctk.CTkButton(master=frame, text='Reset Username & Password?', fg_color="Red",
                                         text_color=("gray10", "gray90"),
                                         hover_color=("red3", "red4"), command=forgot_password)
    forgot_password_button.pack(pady=12, padx=10)

    login_window.mainloop()

    create_account_management_frame(frame)


# Create the login window first
create_login_window()
