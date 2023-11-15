import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from twilio.rest import Client
import os
import sqlite3
import random
import string
import qrcode
import cv2
import datetime
from tkintermapview import TkinterMapView

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


def change_appearance_mode_event(new_appearance_mode):
    ctk.set_appearance_mode(new_appearance_mode)


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

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
        self.location_image=ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "location_black.png")),
            dark_image=Image.open(os.path.join(image_path, "location_white.png")), size=(20, 20))
        self.attendance_image=ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "scan_black.png")),
            dark_image=Image.open(os.path.join(image_path, "scan_white.png")), size=(20, 20))

        # Load the large image you want to insert
        large_image=Image.open("test_images/gym_cover.png")
        large_image=ImageTk.PhotoImage(large_image)

        # create navigation frame
        self.navigation_frame=ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(12, weight=1)

        self.navigation_frame_label=ctk.CTkLabel(
            self.navigation_frame, text="", image=self.logo_image,
            compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Home",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Membership",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_user_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Take Attendance",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.attendance_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Gym Equipment",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_equipment_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.frame_5_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Trainers",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.trainer_image, anchor="w", command=self.frame_5_button_event)
        self.frame_5_button.grid(row=5, column=0, sticky="ew")

        self.frame_6_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Visitors",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.visitor_image, anchor="w", command=self.frame_6_button_event)
        self.frame_6_button.grid(row=6, column=0, sticky="ew")

        self.frame_7_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Employees",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.employee_image, anchor="w", command=self.frame_7_button_event)
        self.frame_7_button.grid(row=7, column=0, sticky="ew")

        self.frame_8_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Location",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.location_image, anchor="w", command=self.frame_8_button_event)
        self.frame_8_button.grid(row=8, column=0, sticky="ew")

        self.frame_9_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Account",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_user_image, anchor="w", command=self.frame_9_button_event)
        self.frame_9_button.grid(row=9, column=0, sticky="ew")

        self.appearance_mode_menu=ctk.CTkOptionMenu(
            self.navigation_frame, values=["Light", "Dark", "System"],
            command=change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=10, column=0, padx=20, pady=20, sticky="s")

        self.logout_button=ctk.CTkButton(
            self.navigation_frame,
            text="Logout",
            fg_color="Red", text_color=("gray10", "gray90"),
            hover_color=("red3", "red4"),
            command=self.logout)
        self.logout_button.grid(row=11, column=0, padx=20, pady=10, sticky="ew")

        # create home frame
        self.home_frame=ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.large_image_label=ctk.CTkLabel(self.home_frame, text="", image=large_image)
        self.large_image_label.grid(row=4, column=0, padx=20, pady=10)

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
        # 9
        self.ninth_frame=ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")
        create_gym_membership_frame(self.second_frame)  # Call the function to create gym membership frame
        create_take_attendance_frame(self.third_frame)
        create_gym_equipment_frame(self.fourth_frame)
        create_trainers_frame(self.fifth_frame)
        create_visitors_frame(self.sixth_frame)
        create_employee_frame(self.seventh_frame)
        create_location_frame(self.eighth_frame)
        create_account_management_frame(self.ninth_frame)

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
        self.frame_9_button.configure(fg_color=("gray75", "gray25") if name == "frame_9" else "transparent")

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
        if name == "frame_9":
            self.ninth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.ninth_frame.grid_forget()

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

    def frame_9_button_event(self):
        self.select_frame_by_name("frame_9")

    # Add a logout method to the MainApp class
    def logout(self):
        # Close the main application window
        self.destroy()

        # Reopen the login window
        create_login_window()


# ------------FRAME_2----------------------#


def create_gym_membership_frame(frame_2):
    # Define the desired button width and height
    button_width=200
    button_height=200

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
        height=button_height
    )
    register_member_button.place(x=250, y=200)

    view_member_button=ctk.CTkButton(
        master=frame_2,
        text="View Members",
        image=ImageTk.PhotoImage(view_image),
        compound=tk.TOP,
        command=view_member,
        width=button_width,
        height=button_height
    )
    view_member_button.place(x=600, y=200)


class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create a connection to the database
        self.conn=sqlite3.connect('registration_form.db')
        self.cursor=self.conn.cursor()

        # STEP 1: PERSONAL INFORMATION
        # Define and configure widgets within the frame
        label=ctk.CTkLabel(self, text="Member Registration", font=("Arial bold", 26))
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
        age_label.grid(row=5, column=0, padx=20, pady=5, sticky="w")
        age_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your age")
        age_entry.grid(row=5, column=1, padx=20, pady=5)

        # Sex
        sex_label=ctk.CTkLabel(personal_info_frame, text="Sex:", font=label_font)
        sex_label.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        sex_entry=ctk.CTkComboBox(personal_info_frame, values=["Male", "Female", "Other"])
        sex_entry.grid(row=6, column=1, padx=20, pady=5)

        # Create a DateEntry widget for the birthdate
        birth_date_label=ctk.CTkLabel(personal_info_frame, text="Date of Birth:", font=label_font)
        birth_date_label.grid(row=7, column=0, padx=20, pady=5, sticky="w")
        birth_date_entry=DateEntry(personal_info_frame, width=20, date_pattern="yyyy-mm-dd")
        birth_date_entry.grid(row=7, column=1, padx=20, pady=15, sticky="w")

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

        # Set the subscription ID based on the last inserted ID
        self.set_subscription_id()

        # Create the widgets for subscription plan, start date, and end date
        subscription_plan_label=ctk.CTkLabel(subscription_frame, text="Subscription Plan:", font=label_font)
        subscription_plan_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        subscription_plan_options=["Weekly", "Monthly", "Yearly"]
        subscription_plan_entry=ctk.CTkComboBox(subscription_frame, values=subscription_plan_options)
        subscription_plan_entry.grid(row=2, column=1, padx=20, pady=15)

        start_timestamp_label=ctk.CTkLabel(subscription_frame, text="Start:", font=label_font)
        start_timestamp_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        start_timestamp_entry=DateEntry(subscription_frame, width=20, date_pattern="yyyy-mm-dd")
        start_timestamp_entry.grid(row=3, column=1, padx=20, pady=15, sticky="w")

        end_timestamp_label=ctk.CTkLabel(subscription_frame, text="End:", font=label_font)
        end_timestamp_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        end_timestamp_entry=DateEntry(subscription_frame, width=20, date_pattern="yyyy-mm-dd")
        end_timestamp_entry.grid(row=4, column=1, padx=20, pady=15, sticky="w")

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
        self.birth_date_entry=birth_date_entry
        self.address_entry=address_entry
        self.nationality_combo=nationality_combo
        self.contact_no_entry=contact_no_entry
        self.email_entry=email_entry
        self.emergency_contact_entry=emergency_contact_entry
        self.subscription_id_entry=self.subscription_id_entry
        self.subscription_plan_entry=subscription_plan_entry
        self.start_timestamp_entry=start_timestamp_entry
        self.end_timestamp_entry=end_timestamp_entry
        self.user_reference_entry=user_reference_entry

        with sqlite3.connect('registration_form.db') as conn:
            cursor=conn.cursor()

        # Create a table to store registration information
        cursor.execute('''
                   CREATE TABLE IF NOT EXISTS registration (
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
                       emergency_contact_no TEXT,
                       subscription_id TEXT,
                       subscription_plan TEXT,
                       start_date DATE,
                       end_date DATE,
                       user_reference TEXT
                   )
               ''')

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

    @staticmethod
    def set_subscription_id():
        # generate random string of length 5
        letters=string.ascii_uppercase + string.digits
        result_str="DG-" + ''.join(random.choice(letters) for i in range(8))
        return result_str

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

        # Validate the data (you can add your validation logic here)

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

        # Create a connection to the database
        conn=sqlite3.connect('registration_form.db')
        cursor=conn.cursor()

        # Insert the data into the database
        cursor.execute('''
                   INSERT INTO registration (first_name, middle_name, last_name, age, sex, birth_date, address,
                                            nationality, contact_no, email, emergency_contact_no, subscription_id,
                                            subscription_plan, start_date, end_date, user_reference)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ''', (first_name, middle_name, last_name, age, sex, birth_date, address, nationality, contact_no,
                     email, emergency_contact_no, subscription_id, subscription_plan, start_date, end_date,
                     user_reference))

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()

        # Combine all the data entries into a single string
        data_string=subscription_id

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

        # Show a success message
        messagebox.showinfo("Registration Successful", "User registered successfully!")

        # Clear all form fields
        for entry in [self.first_name_entry, self.middle_name_entry, self.last_name_entry, self.age_entry,
                      self.address_entry, self.contact_no_entry, self.email_entry,
                      self.emergency_contact_entry, self.subscription_id_entry,
                      self.user_reference_entry]:
            entry.delete(0, tk.END)

        # Set ComboBox and DateEntry widgets to default or empty values
        self.sex_entry.set("Male")
        self.birth_date_entry.set_date("")
        self.nationality_combo.set("Select Nationality")
        self.subscription_plan_entry.set("Weekly")
        self.start_timestamp_entry.set_date("")
        self.end_timestamp_entry.set_date("")

    def back_button_event(self):
        self.destroy()


def back_button_event(self):
    # Switch back to the previous frame (e.g., the gym membership frame)
    self.destroy()


class ViewFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Define and configure widgets within the frame
        label=ctk.CTkLabel(self, text="Members List", font=("Arial bold", 28))
        label.pack(pady=20, padx=10)

        # Create a connection to the database
        conn=sqlite3.connect('registration_form.db')
        cursor=conn.cursor()

        # Get only the specific columns from the database
        cursor.execute(
            "SELECT id, first_name, middle_name, last_name, subscription_plan, start_date, end_date FROM registration")
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
                        borderwidth=0,
                        anchor="center")
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        # Create a table to display the records
        self.table=ttk.Treeview(table_frame, columns=(
            "ID", "First Name", "Middle Name", "Last Name", "Subscription Plan",
            "Start Date", "End Date"), show="headings", height=10)
        self.table.pack(side=tk.LEFT)

        self.scrollbar=ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table.configure(yscrollcommand=self.scrollbar.set)

        # Configure the columns
        self.table.heading("ID", text="ID")
        self.table.heading("First Name", text="First Name")
        self.table.heading("Middle Name", text="Middle Name")
        self.table.heading("Last Name", text="Last Name")
        self.table.heading("Subscription Plan", text="Subscription Plan")
        self.table.heading("Start Date", text="Start Date")
        self.table.heading("End Date", text="End Date")

        # Define the column headings and their alignment
        columns=[
            ("ID", "center"),
            ("First Name", "center"),
            ("Middle Name", "center"),
            ("Last Name", "center"),
            ("Subscription Plan", "center"),
            ("Start Date", "center"),
            ("End Date", "center")
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

        # create a frame to hold the return button
        return_button_frame=ctk.CTkFrame(button_frames)
        return_button_frame.grid(row=0, column=0, padx=10, pady=10)
        # Create a "Return" button in the first column
        return_button=ctk.CTkButton(return_button_frame, text="Return", command=self.back_button_event)
        return_button.pack(padx=10, pady=10)

        # Create a frame to hold the edit button
        view_button_frame=ctk.CTkFrame(button_frames)
        view_button_frame.grid(row=0, column=1, padx=10, pady=10)
        # Create an "Edit" button in the second column
        view_button=ctk.CTkButton(view_button_frame, text="View", command=self.edit_record)
        view_button.pack(padx=10, pady=10)

        # Create a frame to hold the delete button
        delete_button_frame=ctk.CTkFrame(button_frames)
        delete_button_frame.grid(row=0, column=2, padx=10, pady=10)
        # Create a "Delete" button in the third column
        delete_button=ctk.CTkButton(delete_button_frame, text="Delete", command=self.delete_record)
        delete_button.pack(padx=10, pady=10)

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
                    conn=sqlite3.connect('registration_form.db')
                    cursor=conn.cursor()
                    try:
                        cursor.execute("DELETE FROM registration WHERE id=?", (id,))
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


class EditForm(ctk.CTkToplevel):
    def __init__(self, master, first_name, id_value, table_reference):
        super().__init__(master)

        # Set the title for the edit form
        self.title("Edit Member Record")
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
        label=ctk.CTkLabel(self, text="Edit Member Record", font=("Arial bold", 20))
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
                "Nationality:", "Contact No:", "Email Address:", "Emergency Contact No:", "Subscription ID:",
                "Subscription Plan:", "Start Date:", "End Date:", "User Reference:"]
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
        qr_code_frame.grid(row=16, column=1, rowspan=16, padx=10, pady=10)

        label=ctk.CTkLabel(edit_frame, text="QR Code:", font=("Arial bold", 16))
        label.grid(row=16, column=0, padx=10, pady=10, sticky="w")

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

        # Create Delete button to remove data from the database
        delete_button=ctk.CTkButton(delete_button_frame, text="Delete", command=self.delete_record)
        delete_button.grid(row=0, column=1, padx=20, pady=20)

        # Store the reference to the 'table' in EditForm
        self.table=table_reference

    def download_qr_code(self):
        # Download the displayed QR code and save it to the Downloads folder in file explorer
        qr_code_path=os.path.join("member_qrcodes", f"dgrit_{self.member_data[3]}.png")
        qr_code_image=Image.open(qr_code_path)

        # Assuming self.member_data[3] is the unique identifier for the member
        save_path=os.path.join(os.path.expanduser("~"), "Downloads", f"dgrit_{self.member_data[3]}.png")
        qr_code_image.save(save_path)

        # show a success message
        messagebox.showinfo("Download Successful", "QR Code downloaded successfully.")

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
                UPDATE registration SET 
                first_name=?, middle_name=?, last_name=?, age=?, sex=?, birth_date=?, address=?, nationality=?,
                contact_no=?, email=?, emergency_contact_no=?, subscription_id=?, subscription_plan=?, start_date=?,
                end_date=?, user_reference=?
                WHERE first_name=?
            ''', (*updated_data, updated_data[0]))

            self.conn.commit()  # Commit the changes to the database
            messagebox.showinfo("Update Successful", "Record updated successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error updating record: {e}")
        finally:
            self.cursor.close()  # Close the cursor
            self.conn.close()  # Close the database connection

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


# ------------- FRAME 3 -----------------------#

def create_take_attendance_frame(frame_3):
    # Define the desired button width and height
    button_width=200
    button_height=200

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
        height=button_height
    )
    scan_qr_button.place(x=250, y=200)

    view_records_button=ctk.CTkButton(
        master=frame_3,
        text="Attendance Records",
        image=ImageTk.PhotoImage(view_image),
        compound=tk.TOP,
        command=view_records,
        width=button_width,
        height=button_height
    )
    view_records_button.place(x=600, y=200)


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
            height=button_height
        )
        time_in_button.place(x=300, y=150)

        time_out_button=ctk.CTkButton(
            master=self,
            text="Time Out",
            image=ImageTk.PhotoImage(time_out_image),
            compound=tk.TOP,
            command=self.scan_qr_code_time_out,
            width=button_width,
            height=button_height
        )
        time_out_button.place(x=550, y=150)

        # create a back button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.pack(pady=20, side=tk.BOTTOM)

    def scan_qr_code_time_in(self):
        # Implement the QR code scanning for time in
        qr_code_data=self.scan_qr_code()
        if qr_code_data:
            # Process the QR code data for time in
            self.record_attendance(qr_code_data, "Time In")

    def scan_qr_code_time_out(self):
        # Implement the QR code scanning for time out
        qr_code_data=self.scan_qr_code()
        if qr_code_data:
            # Process the QR code data for time out
            self.record_attendance(qr_code_data, "Time Out")

    @staticmethod
    def record_attendance(member_data, attendance_type):
        # Extract relevant information from the QR code data
        # Modify this part based on your QR code content and data format
        member_id=member_data  # Assuming the QR code contains the member ID

        # Get the current date and time
        current_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log the attendance record in the database or any other storage mechanism
        # Modify the logic to suit your database schema
        conn=sqlite3.connect('attendance_records.db')
        cursor=conn.cursor()

        try:
            if attendance_type == "Time In":
                cursor.execute('''
                    INSERT INTO attendance_records (member_id, time_in)
                    VALUES (?, ?)
                ''', (member_id, current_datetime))
            elif attendance_type == "Time Out":
                cursor.execute('''
                    UPDATE attendance_records
                    SET time_out = ?
                    WHERE member_id = ? AND time_out IS NULL
                ''', (current_datetime, member_id))

            conn.commit()
            messagebox.showinfo("Attendance Recorded",
                                f"{attendance_type} recorded successfully for Member ID: {member_id}")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error recording attendance: {e}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def scan_qr_code():
        # Open a camera to capture video
        cap=cv2.VideoCapture(0)

        while True:
            # Capture frame-by-frame
            ret, frame=cap.read()

            # Display the frame
            cv2.imshow('QR Code Scanner', frame)

            # Check for QR code in the frame
            detector=cv2.QRCodeDetector()
            data, vertices, qr_code=detector.detectAndDecode(frame)

            if data:
                # If QR code is detected, close the camera and return the data
                cap.release()
                cv2.destroyAllWindows()
                return data

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and destroy all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

    def back_button_event(self):
        # Switch back to the take attendance frame
        self.destroy()


class RecordsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.create_ui_elements()

    def create_ui_elements(self):
        # Create a frame to hold the attendance records table
        records_table_frame=ctk.CTkFrame(self)
        records_table_frame.pack(pady=10, padx=10)

        # Create a style for the Treeview
        style=ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25,
                        fieldbackground="#343638", bordercolor="#343638", borderwidth=0, anchor="center")
        style.map('Treeview', background=[('selected', '#22559b')])

        # Create a Treeview widget to display the attendance records
        self.records_table=ttk.Treeview(records_table_frame, columns=("Member ID", "Time In", "Time Out"),
                                        show="headings", height=25)
        self.records_table.pack(side=tk.LEFT)

        # Create a scrollbar for the Treeview
        scrollbar=ttk.Scrollbar(records_table_frame, orient=tk.VERTICAL, command=self.records_table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.records_table.configure(yscrollcommand=scrollbar.set)

        # Configure the columns
        self.records_table.heading("Member ID", text="Member ID")
        self.records_table.heading("Time In", text="Time In")
        self.records_table.heading("Time Out", text="Time Out")

        # Fetch attendance records from the database
        self.load_attendance_records()

        # Create attendance record sqlite database if it doesn't exist
        conn=sqlite3.connect('attendance_records.db')
        cursor=conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance_records (
                id INTEGER PRIMARY KEY,
                member_id TEXT,
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
            cursor.execute('SELECT member_id, time_in, time_out FROM attendance_records')
            records=cursor.fetchall()

            for record in records:
                self.records_table.insert("", tk.END, values=record)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching attendance records: {e}")

        finally:
            cursor.close()
            conn.close()

            # create a back button to return to the previous frame
            back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                      hover_color=("red3", "red4"), command=self.back_button_event)
            back_button.pack(pady=20, side=tk.BOTTOM)

    def back_button_event(self):
        # Switch back to the previous frame
        self.destroy()


# -------------------------- FRAME 4 ----------------------#

def create_gym_equipment_frame(frame_4):
    # Define the desired button width and height
    button_width=200
    button_height=200

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
        height=button_height
    )
    register_equipment_button.place(x=250, y=200)

    view_member_button=ctk.CTkButton(
        master=frame_4,
        text="View Equipment Records",
        image=ImageTk.PhotoImage(view_image),
        compound=tk.TOP,
        command=view_member,
        width=button_width,
        height=button_height
    )
    view_member_button.place(x=600, y=200)


class RegistrationEquipment(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create frame to hold all the widget frames
        outer_frame=ctk.CTkFrame(self)
        outer_frame.pack(padx=20, pady=20, fill="both", expand=True)

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
        equipment_name_label.grid(row=1, column=0, padx=10, pady=20, sticky="w")
        equipment_name_entry=ctk.CTkEntry(equipment_info_frame, placeholder_text="Description")
        equipment_name_entry.grid(row=1, column=1, padx=10, pady=20)

        # Brand
        equipment_brand_label=ctk.CTkLabel(equipment_info_frame, text="Brand:", font=label_font)
        equipment_brand_label.grid(row=2, column=0, padx=10, pady=20, sticky="w")
        equipment_brand_entry=ctk.CTkEntry(equipment_info_frame, placeholder_text="Brand/Manufacturer")
        equipment_brand_entry.grid(row=2, column=1, padx=10, pady=20)

        # Model
        equipment_model_label=ctk.CTkLabel(equipment_info_frame, text="Model:", font=label_font)
        equipment_model_label.grid(row=3, column=0, padx=10, pady=20, sticky="w")
        equipment_model_entry=ctk.CTkEntry(equipment_info_frame, placeholder_text="Model/Year")
        equipment_model_entry.grid(row=3, column=1, padx=10, pady=20)

        # Serial Number
        equipment_serial_number_label=ctk.CTkLabel(equipment_info_frame, text="Serial No:", font=label_font)
        equipment_serial_number_label.grid(row=4, column=0, padx=10, pady=20, sticky="w")
        equipment_serial_number_entry=ctk.CTkEntry(equipment_info_frame, placeholder_text="Serial Number")
        equipment_serial_number_entry.grid(row=4, column=1, padx=10, pady=20)

        # quantity
        equipment_quantity_label=ctk.CTkLabel(equipment_info_frame, text="Quantity:", font=label_font)
        equipment_quantity_label.grid(row=5, column=0, padx=10, pady=20, sticky="w")
        equipment_quantity_entry=ctk.CTkEntry(equipment_info_frame, placeholder_text="Quantity")
        equipment_quantity_entry.grid(row=5, column=1, padx=10, pady=20)

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
        register_button.pack(pady=10, side=tk.TOP)

        # Create a "Back" button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.pack(pady=10, side=tk.TOP)

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
        label=ctk.CTkLabel(self, text="Gym Equipment Records", font=("Arial bold", 28))
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
                        borderwidth=0,
                        anchor="center")
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        # Create a table to display the records
        self.table=ttk.Treeview(table_frame, columns=(
            "ID", "Equipment Name", "Equipment Quantity", "Equipment Type", "Equipment Status",
            "Equipment Training Required"), show="headings", height=10)
        self.table.pack(side=tk.LEFT)

        self.scrollbar=ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table.configure(yscrollcommand=self.scrollbar.set)

        # Configure the columns
        self.table.heading("ID", text="ID")
        self.table.heading("Equipment Name", text="Equipment Name")
        self.table.heading("Equipment Quantity", text="Quantity")
        self.table.heading("Equipment Type", text="Type")
        self.table.heading("Equipment Status", text="Status")
        self.table.heading("Equipment Training Required", text="Training Required")

        # Define the column headings and their alignment
        columns=[
            ("ID", "center"),
            ("Equipment Name", "center"),
            ("Equipment Quantity", "center"),
            ("Equipment Type", "center"),
            ("Equipment Status", "center"),
            ("Equipment Training Required", "center")
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
        button_frames.pack(pady=20, padx=10)

        # create a frame to hold the return button
        return_button_frame=ctk.CTkFrame(button_frames)
        return_button_frame.grid(row=0, column=0, padx=10, pady=10)
        # Create a "Return" button in the first column
        return_button=ctk.CTkButton(return_button_frame, text="Return", command=self.back_button_event)
        return_button.pack(padx=10, pady=10)

        # Create a frame to hold the edit button
        view_button_frame=ctk.CTkFrame(button_frames)
        view_button_frame.grid(row=0, column=1, padx=10, pady=10)
        # Create an "Edit" button in the second column
        view_button=ctk.CTkButton(view_button_frame, text="View", command=self.edit_record)
        view_button.pack(padx=10, pady=10)

        # Create a frame to hold the delete button
        delete_button_frame=ctk.CTkFrame(button_frames)
        delete_button_frame.grid(row=0, column=2, padx=10, pady=10)
        # Create a "Delete" button in the third column
        delete_button=ctk.CTkButton(delete_button_frame, text="Delete", command=self.delete_record)
        delete_button.pack(padx=10, pady=10)

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
        self.title("Edit Equipment Record")
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
        label=ctk.CTkLabel(self, text="Edit Equipment Record", font=("Arial bold", 20))
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

        # Create Delete button to remove data from the database
        delete_button=ctk.CTkButton(delete_button_frame, text="Delete", command=self.delete_record)
        delete_button.grid(row=0, column=1, padx=20, pady=20)

        # Store the reference to the 'table' in EditForm
        self.table=table_reference

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
                        cursor.execute("DELETE FROM registration WHERE id=?", (id_value,))
                        conn.commit()  # Commit the changes to the database
                        print("Record deleted successfully.")
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"Error deleting record: {e}")
                        print(f"Error deleting record: {e}")
                    finally:
                        cursor.close()
                        conn.close()


# --------------------------FRAME 5 -----------------------------------------#

def create_trainers_frame(frame_5):
    # Define the desired button width and height
    button_width=200
    button_height=200

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
        height=button_height
    )
    register_trainer_button.place(x=200, y=200)

    view_trainer_button=ctk.CTkButton(
        master=frame_5,
        text="View Trainer Records",
        image=ImageTk.PhotoImage(view_image),
        compound=tk.TOP,
        command=view_trainer,
        width=button_width,
        height=button_height
    )
    view_trainer_button.place(x=450, y=200)

    trainer_attendance_button=ctk.CTkButton(
        master=frame_5,
        text="Trainer Attendance",
        image=ImageTk.PhotoImage(take_attendance),
        compound=tk.TOP,
        command=trainer_attendance,
        width=button_width,
        height=button_height
    )
    trainer_attendance_button.place(x=700, y=200)


class TrainerFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # STEP 1: PERSONAL INFORMATION
        # Define and configure widgets within the frame
        label=ctk.CTkLabel(self, text="Trainer Registration", font=("Arial bold", 26))
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
        age_label.grid(row=5, column=0, padx=20, pady=5, sticky="w")
        age_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your age")
        age_entry.grid(row=5, column=1, padx=20, pady=5)

        # Sex
        sex_label=ctk.CTkLabel(personal_info_frame, text="Sex:", font=label_font)
        sex_label.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        sex_entry=ctk.CTkComboBox(personal_info_frame, values=["Male", "Female", "Other"])
        sex_entry.grid(row=6, column=1, padx=20, pady=5)

        # Create a DateEntry widget for the birthdate
        birth_date_label=ctk.CTkLabel(personal_info_frame, text="Date of Birth:", font=label_font)
        birth_date_label.grid(row=7, column=0, padx=20, pady=5, sticky="w")
        birth_date_entry=DateEntry(personal_info_frame, width=20, date_pattern="yyyy-mm-dd")
        birth_date_entry.grid(row=7, column=1, padx=20, pady=15, sticky="w")

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
        self.birth_date_entry=birth_date_entry
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
        data_string=f"First Name: {first_name}\n" \
                    f"Middle Name: {middle_name}\n" \
                    f"Last Name: {last_name}\n" \
                    f"Age: {age}\n" \
                    f"Sex: {sex}\n" \
                    f"Date of Birth: {birth_date}\n" \
                    f"Address: {address}\n" \
                    f"Nationality: {nationality}\n" \
                    f"Contact No: {contact_no}\n" \
                    f"Email: {email}\n" \
                    f"Emergency Contact No: {emergency_contact_no}\n" \
 \
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
        label=ctk.CTkLabel(self, text="Trainer Records", font=("Arial bold", 28))
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
                        borderwidth=0,
                        anchor="center")
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
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

        # create a frame to hold the return button
        return_button_frame=ctk.CTkFrame(button_frames)
        return_button_frame.grid(row=0, column=0, padx=10, pady=10)
        # Create a "Return" button in the first column
        return_button=ctk.CTkButton(return_button_frame, text="Return", command=self.back_button_event)
        return_button.pack(padx=10, pady=10)

        # Create a frame to hold the edit button
        view_button_frame=ctk.CTkFrame(button_frames)
        view_button_frame.grid(row=0, column=1, padx=10, pady=10)
        # Create an "Edit" button in the second column
        view_button=ctk.CTkButton(view_button_frame, text="View", command=self.edit_record)
        view_button.pack(padx=10, pady=10)

        # Create a frame to hold the delete button
        delete_button_frame=ctk.CTkFrame(button_frames)
        delete_button_frame.grid(row=0, column=2, padx=10, pady=10)
        # Create a "Delete" button in the third column
        delete_button=ctk.CTkButton(delete_button_frame, text="Delete", command=self.delete_record)
        delete_button.pack(padx=10, pady=10)

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
        self.title("Edit Trainer Record")
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
        label=ctk.CTkLabel(self, text="Edit Trainer Record", font=("Arial bold", 20))
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

        # Create Delete button to remove data from the database
        delete_button=ctk.CTkButton(delete_button_frame, text="Delete", command=self.delete_record)
        delete_button.grid(row=0, column=1, padx=20, pady=20)

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
                ''', (tuple, updated_data))

            self.conn.commit()  # Commit the changes to the database
            messagebox.showinfo("Update Successful", "Record updated successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error updating record: {e}")
        finally:
            self.cursor.close()  # Close the cursor
            self.conn.close()  # Close the database connection

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


class TrainerAttendanceFrame(ctk.CTkFrame):
    pass


def create_visitors_frame(frame_6):
    # Create and configure UI elements within frame
    label=ctk.CTkLabel(frame_6, text="VISITORS LOG BOOK", font=("Arial bold", 34))
    label.pack(pady=10, padx=10)

    # Widgets


def create_employee_frame(frame_7):
    # Define the desired button width and height
    button_width=200
    button_height=200

    # Define the path to the directory containing your image files
    frame_7_icons=os.path.join(os.path.dirname(os.path.realpath(__file__)), "frame_7_icons")

    # Load and resize the images
    register_image=Image.open(os.path.join(frame_7_icons, 'register_black.png'))
    register_image=register_image.resize((button_width, button_height), Image.LANCZOS)

    view_image=Image.open(os.path.join(frame_7_icons, 'list_black.png'))
    view_image=view_image.resize((button_width, button_height), Image.LANCZOS)

    def register_employee():
        # When the "Register Members" button is clicked, create and show the registration frame
        registration_frame=RegisterEmployeeFrame(frame_7)
        registration_frame.pack(fill='both', expand=True)

    def view_employee_information():
        # When the "View Members" button is clicked, create and show the view members frame
        view_employee_frame=ViewEmployeeFrame(frame_7)
        view_employee_frame.pack(fill='both', expand=True)

    # Create the buttons with the resized images
    register_employee_button=ctk.CTkButton(
        master=frame_7,
        text="Register Employee",
        image=ImageTk.PhotoImage(register_image),
        compound=tk.TOP,
        command=register_employee,  # Call the function to open the frame
        width=button_width,
        height=button_height
    )
    register_employee_button.place(x=250, y=200)

    view_employee_button=ctk.CTkButton(
        master=frame_7,
        text="View Employee Information",
        image=ImageTk.PhotoImage(view_image),
        compound=tk.TOP,
        command=view_employee_information,
        width=button_width,
        height=button_height
    )
    view_employee_button.place(x=600, y=200)


class RegisterEmployeeFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # STEP 1: PERSONAL INFORMATION
        # Define and configure widgets within the frame
        label=ctk.CTkLabel(self, text="Employee Registration", font=("Arial bold", 26))
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
        age_label.grid(row=5, column=0, padx=20, pady=5, sticky="w")
        age_entry=ctk.CTkEntry(personal_info_frame, placeholder_text="Enter your age")
        age_entry.grid(row=5, column=1, padx=20, pady=5)

        # Sex
        sex_label=ctk.CTkLabel(personal_info_frame, text="Sex:", font=label_font)
        sex_label.grid(row=6, column=0, padx=20, pady=5, sticky="w")
        sex_entry=ctk.CTkComboBox(personal_info_frame, values=["Male", "Female", "Other"])
        sex_entry.grid(row=6, column=1, padx=20, pady=5)

        # Create a DateEntry widget for the birthdate
        birth_date_label=ctk.CTkLabel(personal_info_frame, text="Date of Birth:", font=label_font)
        birth_date_label.grid(row=7, column=0, padx=20, pady=5, sticky="w")
        birth_date_entry=DateEntry(personal_info_frame, width=20, date_pattern="yyyy-mm-dd")
        birth_date_entry.grid(row=7, column=1, padx=20, pady=15, sticky="w")

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
        self.birth_date_entry=birth_date_entry
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
                        borderwidth=0,
                        anchor="center")
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
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

        # create a frame to hold the return button
        return_button_frame=ctk.CTkFrame(button_frames)
        return_button_frame.grid(row=0, column=0, padx=10, pady=10)
        # Create a "Return" button in the first column
        return_button=ctk.CTkButton(return_button_frame, text="Return", command=self.back_button_event)
        return_button.pack(padx=10, pady=10)

        # Create a frame to hold the edit button
        view_button_frame=ctk.CTkFrame(button_frames)
        view_button_frame.grid(row=0, column=1, padx=10, pady=10)
        # Create an "Edit" button in the second column
        view_button=ctk.CTkButton(view_button_frame, text="View", command=self.edit_record)
        view_button.pack(padx=10, pady=10)

        # Create a frame to hold the delete button
        delete_button_frame=ctk.CTkFrame(button_frames)
        delete_button_frame.grid(row=0, column=2, padx=10, pady=10)
        # Create a "Delete" button in the third column
        delete_button=ctk.CTkButton(delete_button_frame, text="Delete", command=self.delete_record)
        delete_button.pack(padx=10, pady=10)

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
                        cursor.execute("DELETE FROM employee WHERE id=?", (id,))
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
        self.trainer_data=self.cursor.fetchone()

        if self.trainer_data is None:
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
            entry.insert(0, self.trainer_data[i + 1])  # Fill with data from the database
            self.entry_fields.append(entry)


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

        # Create Delete button to remove data from the database
        delete_button=ctk.CTkButton(delete_button_frame, text="Delete", command=self.delete_record)
        delete_button.grid(row=0, column=1, padx=20, pady=20)

        # Store the reference to the 'table' in EditForm
        self.table=table_reference

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
                    WHERE first_name=?
                ''', (tuple, updated_data))

            self.conn.commit()  # Commit the changes to the database
            messagebox.showinfo("Update Successful", "Record updated successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error updating record: {e}")
        finally:
            self.cursor.close()  # Close the cursor
            self.conn.close()  # Close the database connection

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
                        cursor.execute("DELETE FROM employees WHERE id=?", (id_value,))
                        conn.commit()  # Commit the changes to the database
                        print("Record deleted successfully.")
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"Error deleting record: {e}")
                        print(f"Error deleting record: {e}")
                    finally:
                        cursor.close()
                        conn.close()


def create_location_frame(frame_8):
    location_frame=LocationFrame(frame_8)
    location_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Configure the map widget
class LocationFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create a frame to hold the map
        map_frame=ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        map_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Create a frame to hold the search bar
        search_frame=ctk.CTkFrame(map_frame, corner_radius=0, fg_color="transparent")
        search_frame.pack(fill='x', padx=10, pady=10)

        search_frame.grid_rowconfigure(0, weight=1)
        search_frame.grid_columnconfigure(0, weight=1)
        search_frame.grid_columnconfigure(1, weight=0)

        search_entry=ctk.CTkEntry(search_frame, placeholder_text="Type address")
        search_entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        search_entry.bind("<Return>", self.search_event)  # Bind the Enter key to trigger the search_event

        search_button=ctk.CTkButton(search_frame, text="Search", width=90, command=self.search_event)
        search_button.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)
        self.search_entry=search_entry  # Store the search_entry widget as an instance variable

        # Create a frame to hold the buttons
        button_frame=ctk.CTkFrame(map_frame, corner_radius=0, fg_color="transparent")
        button_frame.pack(fill='x', padx=10, pady=10)

        set_marker_button=ctk.CTkButton(button_frame, text="Set Marker", command=self.set_marker_event)
        set_marker_button.grid(row=0, column=0, padx=(10, 10), pady=(5, 5))

        clear_marker_button=ctk.CTkButton(button_frame, text="Clear Markers", command=self.clear_marker_event)
        clear_marker_button.grid(row=0, column=1, padx=(10, 100), pady=(5, 5))

        map_option_menu=ctk.CTkOptionMenu(button_frame, values=["OpenStreetMap", "Google normal", "Google satellite"],
                                          command=self.change_map)
        map_option_menu.grid(row=0, column=3, padx=(450, 100), pady=(5, 5))

        # Create a map widget inside the existing map_frame
        self.map_widget=TkinterMapView(map_frame, corner_radius=0)
        self.map_widget.pack(fill='both', expand=True)  # Use pack manager here

        # Set default values
        self.map_widget.set_address("Matnog, Sorsogon, Philippines")
        self.map_widget.set_zoom(30)

        # Initialize the marker_list as an instance variable
        self.marker_list=[]

    def search_event(self):
        address=self.search_entry.get()
        self.map_widget.set_address(address)

    def set_marker_event(self):
        current_position=self.map_widget.get_position()
        self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1]))

    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                            max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                            max_zoom=22)


def create_account_management_frame(frame_9):
    label=ctk.CTkLabel(frame_9, text="MANAGE ACCOUNT", font=("Arial bold", 34))
    label.pack(pady=30, padx=10)

    fields_frame=ctk.CTkFrame(frame_9)
    fields_frame.pack(pady=10, padx=10)

    label=ctk.CTkLabel(fields_frame, text="Create Account", font=("Arial bold", 28),
                       fg_color="transparent")
    label.pack(pady=10, padx=10)

    label_font=ctk.CTkFont(family="Arial bold", size=16)  # Adjust the size as needed

    # Widgets
    username_label=ctk.CTkLabel(fields_frame, text="Username:", font=label_font)
    username_label.pack(pady=10, padx=10)
    username_entry=ctk.CTkEntry(fields_frame, placeholder_text="Enter new username")
    username_entry.pack(pady=10, padx=10)

    password_label=ctk.CTkLabel(fields_frame, text="Password:", font=label_font)
    password_label.pack(pady=10, padx=10)
    password_entry=ctk.CTkEntry(fields_frame, placeholder_text='Enter new password', show="*")
    password_entry.pack(pady=10, padx=10)

    register_button=ctk.CTkButton(fields_frame, text="Register",
                                  command=lambda: register(username_entry.get(), password_entry.get()))
    register_button.pack(pady=10, padx=10)


def register(username, password):
    # Check if the username and password meet your criteria (uppercase, lowercase, symbol)
    if not is_valid(username, password):
        messagebox.showerror("Invalid Data",
                             "Username and Password must be mixed with uppercase and lowercase letters and numbers/symbols.")
        return

    # Connect to SQLite database
    conn=sqlite3.connect('your_database.db')
    cursor=conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
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
        # Insert the data into the database
        cursor.execute('INSERT INTO accounts (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        messagebox.showinfo("Registration Successful", "Your account has been registered successfully.")


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


def forgot_password():
    # Generate a random 6-character OTP
    otp=''.join(random.choices(string.digits, k=6))

    # Replace these with your actual Twilio credentials
    TWILIO_SID='ACcaf2b0445f94b586ad6105561b2f46ff'
    TWILIO_AUTH_TOKEN='dcd1bdc389d703c25f2099c052fab288'
    TWILIO_PHONE_NUMBER='+14698043282'

    def send_otp_via_sms(phone_number, otp_to_send):
        client=Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

        try:
            message=client.messages.create(
                body=f'Your OTP is: {otp_to_send}',
                from_=TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            return message.sid
        except Exception as e:
            messagebox.showerror('Error', f'Error sending SMS: {str(e)}')

    while True:
        user_phone_number=simpledialog.askstring('Enter Phone Number', 'Enter your phone number (e.g., +639123456789):')

        if user_phone_number is None:
            break
        elif user_phone_number.startswith('+639') and len(user_phone_number) == 13:
            send_otp_via_sms(user_phone_number, otp)

            entered_otp=simpledialog.askstring('Enter OTP', 'Enter the OTP sent to your phone:', show='*')

            if entered_otp is None:
                break
            elif entered_otp == otp:
                new_username=simpledialog.askstring('New Username', 'Enter your new username:')
                new_password=simpledialog.askstring('New Password', 'Enter your new password:', show='*')

                if new_username and new_password:
                    conn=sqlite3.connect('your_database.db')
                    cursor=conn.cursor()
                    cursor.execute('INSERT INTO accounts (username, password) VALUES (?, ?)',
                                   (new_username, new_password))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo('Password Reset Successful', 'Your password has been reset successfully.')
                else:
                    messagebox.showerror('Error', 'New username and password are required.')
                break
            else:
                messagebox.showerror('Invalid OTP', 'The entered OTP is incorrect.')
        else:
            messagebox.showerror('Invalid Phone Number',
                                 'Please enter a valid Philippines phone number (e.g., +639123456789).')


# Create the login system
def create_login_window():
    def login():
        username=user_entry.get()
        password=user_pass.get()

        if username == "" or password == "":
            messagebox.showerror(title="Login Failed", message="Please enter both username and password")
            return

        # Connect to SQLite database
        conn=sqlite3.connect('your_database.db')
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
