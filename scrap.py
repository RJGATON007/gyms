# import customtkinter as ctk
# from tkinter import messagebox
#
# ctk.set_appearance_mode("dark")
# ctk.set_default_color_theme("green")
#
#
# class MainApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#
#         self.title("CTkTabview Example")
#         self.geometry("800x600")
#
#         # Create tabview
#         self.tabview=ctk.CTkTabview(self)
#         self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
#
#         # Create tabs
#         self.tabview.add("CTkTabview")
#         self.tabview.add("Tab 2")
#         self.tabview.add("Tab 3")
#
#         # Configure grid of individual tabs
#         self.tabview.tab("CTkTabview").grid_columnconfigure(0, weight=1)
#         self.tabview.tab("Tab 2").grid_columnconfigure(0, weight=1)
#
#         # Tab 1 widgets
#         self.optionmenu_1=ctk.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
#                                             values=["Value 1", "Value 2", "Value Long Long Long"])
#         self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
#
#         self.combobox_1=ctk.CTkComboBox(self.tabview.tab("CTkTabview"),
#                                         values=["Value 1", "Value 2", "Value Long....."])
#         self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
#
#         # Tab 2 widgets
#         self.label_tab_2=ctk.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
#         self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)
#
#         # Tab 3 widgets
#         self.button_tab_3=ctk.CTkButton(self.tabview.tab("Tab 3"), text="CTkButton on Tab 3", command=self.button_event)
#         self.button_tab_3.grid(row=0, column=0, padx=20, pady=20)
#
#     def button_event(self):
#         messagebox.showinfo("Tab 3 Button", "Button on Tab 3 clicked!")
#
#
# if __name__ == "__main__":
#     app=MainApp()
#     app.mainloop()
#
#
#  # print(first_name)
#
#         # # Insert the data into the 'members' table
#         # try:
#         #     conn=sqlite3.connect('database.db')
#         #     cursor=conn.cursor()
#         #
#         #     # SQL query to insert data into the 'members' table
#         #     insert_query="""
#         #         INSERT INTO members (first_name, middle_name, last_name, age, sex, birth_date, address, nationality, contact_no,
#         #          email, emergency_contact_no, subscription_id, subscription_plan, subscription_start, subscription_end, user_reference)
#         #         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         #     """
#         #     cursor.execute(insert_query,
#         #                    (first_name, middle_name, last_name, age, sex, birth_date, address, nationality, contact_no,
#         #                     email, emergency_contact_no, subscription_id, subscription_plan, start_timestamp,
#         #                     end_timestamp, user_reference))
#         #
#         #     conn.commit()
#         #     conn.close()
#         #
#         #     # Display a success message or perform any other necessary actions
#         #     messagebox.showinfo("Success", "Subscription registered successfully!")
#         #
#         # except sqlite3.Error as e:
#         #     # Handle any database errors
#         #     messagebox.showerror("Error", f"Error registering subscription: {e}")
