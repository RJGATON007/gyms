def create_home_frame(home):
    dashboard_frame=ctk.CTkFrame(home)
    dashboard_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # dashboard label align left
    dashboard_label=ctk.CTkLabel(dashboard_frame, text="Dashboard", font=("Arial bold", 26))
    dashboard_label.pack(pady=20, padx=10, anchor="w")

    # frame
    panel_frame=ctk.CTkScrollableFrame(dashboard_frame)
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

    # get the no. of members from the database
    conn=sqlite3.connect('registration_form.db')
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM registration")
    members_count=cursor.fetchone()[0]
    members_counter_label.configure(text=members_count)
    conn.close()

    # visitor panel frame
    visitors_panel_frame=ctk.CTkFrame(panel_frame, fg_color="orange")
    visitors_panel_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # create a small rectangular label to display the no. of members
    visitors_label=ctk.CTkLabel(visitors_panel_frame, text="Visitors", font=("Arial bold", 14))
    visitors_label.pack(pady=5, padx=65, anchor="w")

    # create a counter label to display the no. of members
    visitor_counter_label=ctk.CTkLabel(visitors_panel_frame, text="", font=("Arial bold", 50))
    visitor_counter_label.pack(pady=10, padx=10, anchor="center")

    # get the no. of members from the database
    conn=sqlite3.connect('visitors_log.db')
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM visitors")
    visitors_count=cursor.fetchone()[0]
    visitor_counter_label.configure(text=visitors_count)
    conn.close()

    # employee panel frame
    employee_panel_frame=ctk.CTkFrame(panel_frame, fg_color="blue")
    employee_panel_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    # create a small rectangular label to display the no. of employees
    employee_label=ctk.CTkLabel(employee_panel_frame, text="Employees", font=("Arial bold", 14))
    employee_label.pack(pady=5, padx=50, anchor="w")

    # create a counter label to display the no. of employees
    employee_counter_label=ctk.CTkLabel(employee_panel_frame, text="", font=("Arial bold", 50))
    employee_counter_label.pack(pady=10, padx=10, anchor="center")

    # get the no. of employees from the database
    conn=sqlite3.connect('register_employee.db')
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM employees")
    employee_count=cursor.fetchone()[0]
    employee_counter_label.configure(text=employee_count)
    conn.close()

    # trainer panel frame
    trainer_panel_frame=ctk.CTkFrame(panel_frame, fg_color="purple")
    trainer_panel_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

    # create a small rectangular label to display the no. of trainers
    trainer_label=ctk.CTkLabel(trainer_panel_frame, text="Trainers", font=("Arial bold", 14))
    trainer_label.pack(pady=5, padx=60, anchor="w")

    # create a counter label to display the no. of trainers
    trainer_counter_label=ctk.CTkLabel(trainer_panel_frame, text="", font=("Arial bold", 50))
    trainer_counter_label.pack(pady=10, padx=10, anchor="center")

    # get the no. of trainers from the database
    conn=sqlite3.connect('register_trainer.db')
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM trainer")
    trainer_count=cursor.fetchone()[0]
    trainer_counter_label.configure(text=trainer_count)
    conn.close()

    # gym equipment panel frame
    gym_equipment_panel_frame=ctk.CTkFrame(panel_frame, fg_color="red")
    gym_equipment_panel_frame.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

    # create a small rectangular label to display the no. of gym equipment
    gym_equipment_label=ctk.CTkLabel(gym_equipment_panel_frame, text="Gym Equipment", font=("Arial bold", 14))
    gym_equipment_label.pack(pady=5, padx=30, anchor="w")

    # create a counter label to display the no. of gym equipment
    gym_equipment_counter_label=ctk.CTkLabel(gym_equipment_panel_frame, text="", font=("Arial bold", 50))
    gym_equipment_counter_label.pack(pady=10, padx=10, anchor="center")

    # get the no. of gym equipment from the database
    conn=sqlite3.connect('register_equipment.db')
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM equipment")
    gym_equipment_count=cursor.fetchone()[0]
    gym_equipment_counter_label.configure(text=gym_equipment_count)
    conn.close()

    # Make the rows and columns resizable
    for i in range(5):
        panel_frame.grid_columnconfigure(i, weight=1)

    panel_frame.grid_rowconfigure(0, weight=1)

    # Schedule periodic updates
    home.after(10000, update_counters, members_counter_label, visitor_counter_label, employee_counter_label,
               trainer_counter_label, gym_equipment_counter_label)


def update_counters(members_counter_label, visitor_counter_label, employee_counter_label, trainer_counter_label,
                    gym_equipment_counter_label):
    # Update members counter
    conn=sqlite3.connect('registration_form.db')
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM registration")
    members_count=cursor.fetchone()[0]
    members_counter_label.configure(text=members_count)
    conn.close()

    # Update visitors counter
    conn=sqlite3.connect('visitors_log.db')
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM visitors")
    visitors_count=cursor.fetchone()[0]
    visitor_counter_label.configure(text=visitors_count)
    conn.close()

    # Update employees counter
    conn=sqlite3.connect('register_employee.db')
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM employees")
    employee_count=cursor.fetchone()[0]
    employee_counter_label.configure(text=employee_count)
    conn.close()

    # Update trainers counter
    conn=sqlite3.connect('register_trainer.db')
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM trainer")
    trainer_count=cursor.fetchone()[0]
    trainer_counter_label.configure(text=trainer_count)
    conn.close()

    # Update gym equipment counter
    conn=sqlite3.connect('register_equipment.db')
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM equipment")
    gym_equipment_count=cursor.fetchone()[0]
    gym_equipment_counter_label.configure(text=gym_equipment_count)
    conn.close()

    # Schedule the next update
    members_counter_label.after(10000, update_counters, members_counter_label, visitor_counter_label,
                                employee_counter_label, trainer_counter_label, gym_equipment_counter_label)




def force_refresh_counters(members_counter_label, visitor_counter_label, employee_counter_label,
                           trainer_counter_label, gym_equipment_counter_label, ax, canvas, count_label1, count_label2):
    update_counters(members_counter_label, visitor_counter_label, employee_counter_label, trainer_counter_label,
                    gym_equipment_counter_label, ax, canvas, count_label1, count_label2)


# Example of deleting data and then forcing an immediate refresh
def delete_data_and_refresh(members_counter_label, visitor_counter_label, employee_counter_label,
                            trainer_counter_label, gym_equipment_counter_label, ax, canvas, count_label1, count_label2):
    try:
        # Delete data from the registration_form database (example)
        conn_registration = sqlite3.connect('registration_form.db')
        cursor_registration = conn_registration.cursor()
        cursor_registration.execute("DELETE FROM registration WHERE some_condition")
        conn_registration.commit()
        conn_registration.close()

        # Delete data from the visitors_log database (example)
        conn_visitors = sqlite3.connect('visitors_log.db')
        cursor_visitors = conn_visitors.cursor()
        cursor_visitors.execute("DELETE FROM visitors WHERE some_condition")
        conn_visitors.commit()
        conn_visitors.close()

        # Force an immediate refresh of the counters
        update_counters(members_counter_label, visitor_counter_label, employee_counter_label,
                        trainer_counter_label, gym_equipment_counter_label, ax, canvas, count_label1, count_label2)

    except Exception as e:
        print(f"Error deleting data and refreshing counters: {e}")
