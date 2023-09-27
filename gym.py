import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import sqlite3

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
            Image.open(os.path.join(image_path, "gym1.png")),
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
        self.product_image=ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "product_black.png")),
            dark_image=Image.open(os.path.join(image_path, "product_white.png")), size=(20, 20))
        self.announcement_image=ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "bell_black.png")),
            dark_image=Image.open(os.path.join(image_path, "bell_white.png")), size=(20, 20))
        self.location_image=ctk.CTkImage(
            light_image=Image.open(os.path.join(image_path, "location_black.png")),
            dark_image=Image.open(os.path.join(image_path, "location_white.png")), size=(20, 20))

        # Load the large image you want to insert
        large_image=Image.open("test_images/gym1.png")
        large_image=ImageTk.PhotoImage(large_image)

        # create navigation frame
        self.navigation_frame=ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(11, weight=1)

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
            text="Gym Equipment",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_equipment_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Trainers",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_user_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.frame_5_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Visitors",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.visitor_image, anchor="w", command=self.frame_5_button_event)
        self.frame_5_button.grid(row=5, column=0, sticky="ew")

        self.frame_6_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Products",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.product_image, anchor="w", command=self.frame_6_button_event)
        self.frame_6_button.grid(row=6, column=0, sticky="ew")

        self.frame_7_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Employees",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.add_user_image, anchor="w", command=self.frame_7_button_event)
        self.frame_7_button.grid(row=7, column=0, sticky="ew")

        self.frame_8_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Announcements",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.announcement_image, anchor="w", command=self.frame_8_button_event)
        self.frame_8_button.grid(row=8, column=0, sticky="ew")

        self.frame_9_button=ctk.CTkButton(
            self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
            text="Location",
            fg_color="transparent", text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.location_image, anchor="w", command=self.frame_9_button_event)
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

        # create 2nd-10th frame
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
        create_gym_equipment_frame(self.third_frame)
        create_trainers_frame(self.fourth_frame)
        create_visitors_frame(self.fifth_frame)

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
    # Create and configure UI elements within frame
    label=ctk.CTkLabel(frame_2, text="GYM MEMBERSHIP MANAGEMENT", font=("Arial bold", 34))
    label.pack(pady=10, padx=10)

    # Define the desired button width and height
    button_width=150
    button_height=150

    # Define the path to the directory containing your image files
    frame_2_icons=os.path.join(os.path.dirname(os.path.realpath(__file__)), "frame_2_icons")

    # Load and resize the images
    register_image=Image.open(os.path.join(frame_2_icons, 'register_black.png'))
    register_image=register_image.resize((button_width, button_height), Image.LANCZOS)

    view_image=Image.open(os.path.join(frame_2_icons, 'list_black.png'))
    view_image=view_image.resize((button_width, button_height), Image.LANCZOS)

    attendance_image=Image.open(os.path.join(frame_2_icons, 'scan_black.png'))
    attendance_image=attendance_image.resize((button_width, button_height), Image.LANCZOS)

    def register_member():
        # When the "Register Members" button is clicked, create and show the registration frame
        registration_frame=RegistrationFrame(frame_2)
        registration_frame.pack(fill='both', expand=True)

    def view_member():
        # When the "View Members" button is clicked, create and show the view members frame
        view_member_frame=ViewFrame(frame_2)
        view_member_frame.pack(fill='both', expand=True)

    def take_attendance():
        pass

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
    register_member_button.place(x=200, y=200)

    view_member_button=ctk.CTkButton(
        master=frame_2,
        text="View Members",
        image=ImageTk.PhotoImage(view_image),
        compound=tk.TOP,
        command=view_member,
        width=button_width,
        height=button_height
    )
    view_member_button.place(x=450, y=200)

    take_attendance_button=ctk.CTkButton(
        master=frame_2,
        text="Take Attendance",
        image=ImageTk.PhotoImage(attendance_image),
        compound=tk.TOP,
        command=take_attendance,
        width=button_width,
        height=button_height
    )
    take_attendance_button.place(x=700, y=200)


class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        label=ctk.CTkLabel(self, text="Member Registration", font=("Arial bold", 28))
        label.pack(pady=20, padx=10)

        # Add registration form fields here
        fields_frame=ctk.CTkFrame(self)
        fields_frame.pack(pady=10, padx=20)

        # Configure the fixed width for the frame (adjust the value as needed)
        fixed_width=500  # Set the desired width

        # Set the fixed width for the frame
        fields_frame.configure(width=fixed_width)

        # Name
        name_label=ctk.CTkLabel(fields_frame, text="Name:")
        name_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.name_entry=ctk.CTkEntry(fields_frame, placeholder_text="Enter your name")
        self.name_entry.grid(row=2, column=1, padx=10, pady=10, sticky="e")

        # Email
        email_label=ctk.CTkLabel(fields_frame, text="Email:")
        email_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.email_entry=ctk.CTkEntry(fields_frame, placeholder_text="Enter your email")
        self.email_entry.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        # Age
        age_label=ctk.CTkLabel(fields_frame, text="Age:")
        age_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.age_entry=ctk.CTkEntry(fields_frame, placeholder_text="Enter your age")
        self.age_entry.grid(row=4, column=1, padx=10, pady=10, sticky="e")

        # Address
        address_label=ctk.CTkLabel(fields_frame, text="Address:")
        address_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.address_entry=ctk.CTkEntry(fields_frame, placeholder_text="Enter your address")
        self.address_entry.grid(row=5, column=1, padx=10, pady=10, sticky="e")

        # Contact Number
        contact_label=ctk.CTkLabel(fields_frame, text="Contact Number:")
        contact_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.contact_entry=ctk.CTkEntry(fields_frame, placeholder_text="Enter your contact number")
        self.contact_entry.grid(row=6, column=1, padx=10, pady=10, sticky="e")

        # Subscription Type
        self.subscription_var=tk.StringVar()
        self.subscription_var.set("Weekly")  # Set the default value
        subscription_label=ctk.CTkLabel(fields_frame, text="Subscription Type:")
        subscription_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")

        subscription_options=["Weekly", "Monthly", "Yearly"]
        subscription_menu=ctk.CTkOptionMenu(fields_frame, variable=self.subscription_var,
                                            values=subscription_options)
        subscription_menu.grid(row=7, column=1, padx=10, pady=10, sticky="e")

        # Add a "Register" button to submit the registration form
        register_button=ctk.CTkButton(self, text="Register", command=self.register_button_event)
        register_button.pack(pady=10)

        # Create a "Back" button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.pack(pady=20, side=tk.BOTTOM)

    def register_button_event(self):
        # Retrieve data from the registration form fields
        name=self.name_entry.get()
        email=self.email_entry.get()
        age=self.age_entry.get()
        address=self.address_entry.get()
        contact_number=self.contact_entry.get()
        subscription_type=self.subscription_var.get()

        # Validate the data (you can add more validation if needed)

        if not name or not email or not age or not address or not contact_number:
            messagebox.showerror(title="Registration Failed", message="Please fill in all fields.")
            return

        try:
            age=int(age)
        except ValueError:
            messagebox.showerror(title="Registration Failed", message="Age must be a number.")
            return

        # Insert data into the database
        conn=sqlite3.connect("registration_db.db")
        cursor=conn.cursor()
        cursor.execute("""
        INSERT INTO registrations (name, email, age, address, contact_number, subscription_type)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, age, address, contact_number, subscription_type))
        conn.commit()
        conn.close()

        # Show a success message
        messagebox.showinfo(title="Registration Successful", message="Member registered successfully")

        # Clear the form fields
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.subscription_var.set("Weekly")  # Reset subscription type to the default

    def back_button_event(self):
        # Switch back to the previous frame (e.g., the gym membership frame)
        self.destroy()


class ViewFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Define and configure widgets within the frame
        label=ctk.CTkLabel(self, text="Members List", font=("Arial bold", 28))
        label.pack(pady=20, padx=10)

        # Create a Treeview widget for displaying the table
        self.tree=ttk.Treeview(self, columns=("Name", "Email", "Age", "Address", "Contact", "Subscription"),
                               style="Treeview")
        self.tree.heading("#1", text="Name")
        self.tree.heading("#2", text="Email")
        self.tree.heading("#3", text="Age")
        self.tree.heading("#4", text="Address")
        self.tree.heading("#5", text="Contact")
        self.tree.heading("#6", text="Subscription")
        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        # Configure column widths
        self.tree.column("#1", width=200, anchor="center")
        self.tree.column("#2", width=250, anchor="center")
        self.tree.column("#3", width=50, anchor="center")
        self.tree.column("#4", width=200, anchor="center")
        self.tree.column("#5", width=150, anchor="center")
        self.tree.column("#6", width=150, anchor="center")

        style=ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=50,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=10)
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="solid")
        style.map("Treeview.Heading",
                  background=[('active', '#3484F0')])

        # Add a "Back" button to return to the previous frame
        back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
                                  hover_color=("red3", "red4"), command=self.back_button_event)
        back_button.pack(pady=20, side=tk.BOTTOM)

        # Load member data and populate the table
        self.load_member_data()

    def back_button_event(self):
        # Switch back to the previous frame (e.g., the gym membership frame)
        self.destroy()

    def load_member_data(self):
        # Connect to the database and fetch member data
        conn=sqlite3.connect("registration_db.db")
        cursor=conn.cursor()
        cursor.execute("SELECT name, email, age, address, contact_number, subscription_type FROM registrations")
        member_data=cursor.fetchall()
        conn.close()

        # Clear existing data in the table
        self.tree.delete(*self.tree.get_children())

        # Populate the table with member data
        for member in member_data:
            self.tree.insert("", "end", values=(member[0], member[1], member[2], member[3], member[4], member[5]))


# Function to create the "login users" table in the database if it doesn't exist
def create_users_table():
    conn=sqlite3.connect("user_db.db")
    cursor=conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


# Call create_users_table() to ensure the table exists
create_users_table()


# Function to create the "registration" table in the database if it doesn't exist
def create_registration_table():
    conn=sqlite3.connect("registration_db.db")
    cursor=conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        address TEXT NOT NULL,
        contact_number TEXT NOT NULL,
        subscription_type TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


# Call create_registration_table() to ensure the table exists
create_registration_table()


# ------------- FRAME 3 -----------------------#

def create_gym_equipment_frame(frame_3):
    # Create and configure UI elements within frame
    label=ctk.CTkLabel(frame_3, text="GYM EQUIPMENT MANAGEMENT", font=("Arial bold", 34))
    label.pack(pady=10, padx=10)

    # Widgets


# ---------------FRAME 4-----------------------#

def create_trainers_frame(frame_4):
    # Create and configure UI elements within frame
    label=ctk.CTkLabel(frame_4, text="TRAINER MANAGEMENT", font=("Arial bold", 34))
    label.pack(pady=10, padx=10)

    # Widgets


# ------------------- FRAME 5 ------------------#

def create_visitors_frame(frame_5):
    # Create and configure UI elements within frame
    label=ctk.CTkLabel(frame_5, text="VISITORS LOG BOOK", font=("Arial bold", 34))
    label.pack(pady=10, padx=10)

    # Widgets


def center_window(window, width, height):
    screen_width=window.winfo_screenwidth()
    screen_height=window.winfo_screenheight()
    x=(screen_width / 1.5) - (width / 1.5)
    y=(screen_height / 2) - (height / 2)
    window.geometry(f"{int(width)}x{int(height)}+{int(x)}+{int(y)}")


# Create the login system
def create_login_window():
    def login():
        username=user_entry.get()
        password=user_pass.get()

        if username == "" or password == "":
            messagebox.showerror(title="Login Failed", message="Please enter both username and password")
            return

        # Check if the user exists in the database
        conn=sqlite3.connect("user_db.db")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user=cursor.fetchone()
        conn.close()

        if user:
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

    def register():
        username=user_entry.get()
        password=user_pass.get()

        if username == "" or password == "":
            messagebox.showerror(title="Registration Failed", message="Please enter both username and password")
            return

        # Check if the user already exists in the database
        conn=sqlite3.connect("user_db.db")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user=cursor.fetchone()

        if existing_user:
            messagebox.showwarning(title="Registration Failed", message="Username already exists")
            conn.close()
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            messagebox.showinfo(title="Registration Successful", message="You have registered successfully")

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

    register_button=ctk.CTkButton(master=frame, text='Register User', fg_color="dodgerblue2",
                                  text_color=("gray10", "gray90"),
                                  hover_color=("dodgerblue3", "dodgerblue4"), command=register)
    register_button.pack(pady=12, padx=10)

    login_window.mainloop()


# Create the login window first
create_login_window()
