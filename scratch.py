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