# import customtkinter as ctk
# from tkcalendar import DateEntry
# import tkinter as tk
#
#
# class RegistrationFrame(ctk.CTkFrame):
#     def __init__(self, master, **kwargs):
#         super().__init__(master, **kwargs)
#
#         # STEP 1: PERSONAL INFORMATION
#         # Define and configure widgets within the frame
#         label=ctk.CTkLabel(self, text="Step 1: Personal Information", font=("Arial bold", 28))
#         label.pack(pady=20, padx=10)
#
#         # Add registration form fields here
#         fields_frame=ctk.CTkFrame(self)
#         fields_frame.pack(pady=10, padx=20)
#
#         # Configure the fixed width for the frame (adjust the value as needed)
#         fixed_width=500  # Set the desired width
#
#         # Set the fixed width for the frame
#         fields_frame.configure(width=fixed_width)
#
#         # Create a custom font for labels
#         label_font=ctk.CTkFont(family="Arial bold", size=16)  # Adjust the size as needed
#
#         # Member ID
#         member_id_label=ctk.CTkLabel(fields_frame, text="Member ID:", font=label_font)
#         member_id_label.grid(row=1, column=0, padx=20, pady=5, sticky="w")
#         self.member_id_entry=ctk.CTkEntry(fields_frame, placeholder_text="DG-XXX")
#         self.member_id_entry.grid(row=1, column=1, padx=20, pady=5)
#
#         # Name
#         first_name_label=ctk.CTkLabel(fields_frame, text="First Name:", font=label_font)
#         first_name_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
#         self.first_name_entry=ctk.CTkEntry(fields_frame, placeholder_text="Enter your first name")
#         self.first_name_entry.grid(row=2, column=1, padx=20, pady=5)
#
#         middle_name_label=ctk.CTkLabel(fields_frame, text="Middle Name:", font=label_font)
#         middle_name_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")
#         self.middle_name_entry=ctk.CTkEntry(fields_frame, placeholder_text="Enter your middle name")
#         self.middle_name_entry.grid(row=3, column=1, padx=20, pady=5)
#
#         last_name_label=ctk.CTkLabel(fields_frame, text="Last Name:", font=label_font)
#         last_name_label.grid(row=4, column=0, padx=20, pady=5, sticky="w")
#         self.last_name_entry=ctk.CTkEntry(fields_frame, placeholder_text="Enter your last name")
#         self.last_name_entry.grid(row=4, column=1, padx=20, pady=5)
#
#         # Age
#         age_label=ctk.CTkLabel(fields_frame, text="Age:", font=label_font)
#         age_label.grid(row=5, column=0, padx=20, pady=5, sticky="w")
#         self.age_entry=ctk.CTkEntry(fields_frame, placeholder_text="Enter your age")
#         self.age_entry.grid(row=5, column=1, padx=20, pady=5)
#
#         # Sex
#         sex_label=ctk.CTkLabel(fields_frame, text="Sex:", font=label_font)
#         sex_label.grid(row=6, column=0, padx=20, pady=5, sticky="w")
#         self.sex_entry=ctk.CTkComboBox(fields_frame, values=["Male", "Female", "Other"])
#         self.sex_entry.grid(row=6, column=1, padx=20, pady=5)
#
#         # Create a DateEntry widget for the birthdate
#         birth_date_label=ctk.CTkLabel(fields_frame, text="Birth Date:", font=label_font)
#         birth_date_label.grid(row=7, column=0, padx=20, pady=5, sticky="w")
#         # Create a DateEntry widget for the birthdate
#         self.birth_date_entry=DateEntry(fields_frame, width=20, date_pattern="yyyy-mm-dd")
#         self.birth_date_entry.grid(row=7, column=1, padx=20, pady=15, sticky="w")
#
#         # Add a "Register" button to submit the registration form
#         next_button=ctk.CTkButton(self, text="Next", command=self.next_button_event)
#         next_button.pack(pady=10)
#
#         # Create a "Back" button to return to the previous frame
#         back_button=ctk.CTkButton(self, text="Back", fg_color="Red", text_color=("gray10", "gray90"),
#                                   hover_color=("red3", "red4"), command=self.back_button_event)
#         back_button.pack(pady=20, side=tk.TOP)
#
#     def next_button_event(self):
#         pass
#
#     def back_button_event(self):
#         self.destroy()

def display_table(self) -> None:
    """Display the table of medicines."""

    check_box_var=ctk.StringVar()

    for pos, text in enumerate(self.col_headers):
        col_cell=ctk.CTkLabel(
            self.scrollable_frame,
            text=text.capitalize(),
            font=self.text_font,
            width=self.column_widths[pos],
            height=50,
        )
        col_cell.grid(
            row=1, column=(pos + 1), pady=(10, 20), ipady=1, padx=5
        )

        col=ctk.CTkEntry(
            self.scrollable_frame,
            width=self.column_widths[pos],
            height=50,
            font=self.text_font,
        )

        col.insert(ctk.END, text.capitalize())
        col.configure(state=ctk.DISABLED)

        col.grid(row=1, column=(pos + 1), pady=(10, 20), ipady=1, padx=5)

    order_entry=ctk.CTkEntry(
        self.scrollable_frame, height=50, font=self.text_font, width=80
    )
    order_entry.insert(ctk.END, "Order")
    order_entry.grid(row=1, column=6, pady=(10, 20), ipady=1, padx=5)

    row=2
    for i in self.dataset:

        for j in range(0, len(i)):
            entry=ctk.CTkEntry(
                self.scrollable_frame,
                width=self.column_widths[j],
                font=self.small_text_font,
            )
            entry.grid(row=row, column=(j + 1), padx=5)

            try:
                entry.insert(ctk.END, i[j].capitalize())
            except AttributeError:
                entry.insert(ctk.END, i[j])

            entry.configure(state=ctk.DISABLED)

        order_checkbox=ctk.CTkCheckBox(
            self.scrollable_frame,
            text="",
            variable=check_box_var,
            onvalue=i[0],
            offvalue=i[0],
            command=lambda: self.order_check_button(check_box_var.get()),
            width=70,
        )

        if i[-1].lower() == "no":
            ctk.CTkLabel(
                self.scrollable_frame,
                text="  -",
                font=self.small_text_font,
                anchor=ctk.W,
                width=70,
            ).grid(row=row, column=6, padx=5)
        else:
            order_checkbox.grid(row=row, column=6, padx=5)

        row+=1


def display_mrec(self) -> None:
    """Display the medicine records of the user."""

    mrec=self.db_object.get_medicine_record(self.user_id)

    if mrec == []:
        ctk.CTkLabel(
            self.mrec_frame,
            text="No records found",
            font=self.text_font,
        ).grid(row=1, column=0, padx=20, pady=20, sticky=ctk.NSEW)
    else:
        mrec_col_headers=[
            "Mid",
            "Name",
            "Treatment",
            "Price",
            "Time of Purchase",
        ]

        mrec_col_widths=[80, 150, 450, 80, 220]

        for i in range(0, len(mrec_col_headers)):
            col_cell=ctk.CTkEntry(
                self.mrec_frame,
                width=mrec_col_widths[i],
                font=self.text_font,
            )
            col_cell.insert(ctk.END, mrec_col_headers[i].capitalize())
            col_cell.configure(state=ctk.DISABLED)
            col_cell.grid(row=1, column=i, pady=(10, 20), ipady=1, padx=5)

        for i in range(0, len(mrec)):
            m_row=self.db_object.get_medicine_details(mrec[i][1])
            for j in range(0, len(m_row) - 1):
                entry=ctk.CTkEntry(
                    self.mrec_frame,
                    width=self.column_widths[j],
                    font=self.small_text_font,
                )
                try:
                    entry.insert(ctk.END, m_row[j].capitalize())
                except AttributeError:
                    entry.insert(ctk.END, m_row[j])
                entry.configure(state=ctk.DISABLED)
                entry.grid(row=(i + 2), column=j, padx=5)

        for i in range(len(mrec)):
            e=ctk.CTkEntry(
                self.mrec_frame,
                width=mrec_col_widths[4],
                font=self.small_text_font,
            )
            e.insert(ctk.END, mrec[i][2])
            e.configure(state=ctk.DISABLED)
            e.grid(row=(i + 2), column=4, padx=5)

    self.mrec_frame.pack(
        fill=ctk.BOTH, expand=True, padx=(0, 20), pady=(0, 20)
    )



 # Get data from the form fields using self.
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
        emergency_contact=self.emergency_contact_entry.get()
        subscription_id=self.subscription_id_entry.get()
        subscription_plan=self.subscription_plan_entry.get()
        start_timestamp=self.start_timestamp_entry.get()
        end_timestamp=self.end_timestamp_entry.get()
        user_reference=self.user_reference_entry.get()

        # Create or connect to the SQLite database
        conn=sqlite3.connect('registration.db')
        cursor=conn.cursor()

        # Check if the "registrations" table exists, and create it if it doesn't
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                middle_name TEXT,
                last_name TEXT,
                age INTEGER,
                sex TEXT,
                birth_date TEXT,
                address TEXT,
                nationality TEXT,
                contact_no TEXT,
                email TEXT,
                emergency_contact TEXT,
                subscription_id TEXT,
                subscription_plan TEXT,
                start_timestamp TEXT,
                end_timestamp TEXT,
                user_reference TEXT
            )
        ''')

        # Commit the changes
        conn.commit()

        try:
            # Insert the data into the "registrations" table
            cursor.execute('''
                       INSERT INTO registrations (
                           first_name, middle_name, last_name, age, sex, birth_date, address,
                           nationality, contact_no, email, emergency_contact, subscription_id,
                           subscription_plan, start_timestamp, end_timestamp, user_reference
                       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ''', (
                first_name, middle_name, last_name, age, sex, birth_date, address,
                nationality, contact_no, email, emergency_contact, subscription_id,
                subscription_plan, start_timestamp, end_timestamp, user_reference
            ))

            # Commit the changes
            conn.commit()

            # Check if any of the required fields are empty
            required_fields=[
                self.first_name_entry, self.last_name_entry, self.age_entry,
                self.sex_entry, self.birth_date_entry, self.address_entry,
                self.nationality_combo, self.contact_no_entry, self.email_entry
            ]

            if any(not field.get() for field in required_fields):
                # Display a message box to inform the user
                tk.messagebox.showwarning("Incomplete Fields", "Please fill in all required fields.")
                return

            # Clear the form fields after a successful registration
            self.clear_form_fields()

            # Display a success message (optional)
            success_message="Registration Successful!"
            messagebox.showinfo("Success", success_message)
            return success_message  # Return the success message

        except sqlite3.Error as e:
            # Handle any database-related errors (e.g., unique constraint violations)
            messagebox.showerror("Error", f"Error during registration: {e}")

        finally:
            # Close the database connection
            conn.close()

    def clear_form_fields(self):
        # Clear all form fields
        self.first_name_entry.delete(0, "end")
        self.middle_name_entry.delete(0, "end")
        self.last_name_entry.delete(0, "end")
        self.age_entry.delete(0, "end")
        self.sex_entry.set("Male")  # Set a default value
        self.birth_date_entry.set_date("")  # Clear the DateEntry field
        self.address_entry.delete(0, "end")
        self.nationality_combo.set("Select Nationality")  # Set a default value
        self.contact_no_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.emergency_contact_entry.delete(0, "end")
        self.subscription_id_entry.delete(0, "end")
        self.subscription_plan_entry.set("Weekly")  # Set a default value
        self.start_timestamp_entry.set_date("")  # Clear the DateEntry field
        self.end_timestamp_entry.set_date("")  # Clear the DateEntry field
        self.user_reference_entry.delete(0, "end")

style=ttk.Style()
        style.theme_use("default")

        # Configure the Treeview style with borderwidth for column headers
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0,
                        relief="groove")  # Adjust borderwidth as needed

        style.map('Treeview', background=[('selected', '#00C957')])

        # Configure the Treeview.Heading style with background color and borderwidth for column headers
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="groove",
                        borderwidth=2)  # Adjust borderwidth for column headers

        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        # Create a frame to hold the Treeview
        tree_frame=ctk.CTkFrame(self)
        tree_frame.grid(row=0, column=1, padx=10, pady=10)

        # Create a Treeview widget to display the employee data
        self.tree=ttk.Treeview(tree_frame, columns=(
            "First Name", "Middle Name", "Last Name", "Age", "Sex", "Date of Birth", "Address", "Contact No"),
                               show="headings")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Middle Name", text="Middle Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Sex", text="Sex")
        self.tree.heading("Date of Birth", text="Date of Birth")
        self.tree.heading("Address", text="Address")
        self.tree.heading("Contact No", text="Contact No")
        self.tree.pack(side=tk.LEFT)

        # Define the column headings and their alignment
        columns=[
            ("First Name", "center"),
            ("Middle Name", "center"),
            ("Last Name", "center"),
            ("Age", "center"),
            ("Sex", "center"),
            ("Date of Birth", "center"),
            ("Address", "center"),
            ("Contact No", "center")
        ]

        for col, align in columns:
            self.tree.heading(col, text=col, anchor=align)
            self.tree.column(col, anchor=align)

        self.tree.pack(side=tk.LEFT)