def update_record(self):
    # Get the updated data from the entry fields, including the status
    updated_data=[entry.get() if label_text != "Status:" else self.status_combobox.get() for label_text, entry in
                  zip(["First Name:", "Middle Name:", "Last Name:", "Age:", "Sex:", "Date of Birth:", "Address:",
                       "Nationality:", "Contact No:", "Email Address:", "Emergency Contact No:", "Status:"],
                      self.entry_fields)]

    # Validate the updated data
    if not all(updated_data[:-1]):  # Exclude the last item (status) from validation
        messagebox.showerror("Validation Error", "All fields (except Status) are required.")
        return

    # Continue with the update logic
    try:
        with sqlite3.connect('register_trainer.db') as conn:
            cursor=conn.cursor()
            cursor.execute('''
                UPDATE trainer SET 
                first_name=?, middle_name=?, last_name=?, age=?, sex=?, birth_date=?, address=?, nationality=?,
                contact_no=?, email=?, emergency_contact_no=?, status=?
                WHERE id=?
            ''', tuple(updated_data + [self.trainer_data[0]]))

        # Commit the changes to the database within the 'with' block
        conn.commit()
        messagebox.showinfo("Update Successful", "Record updated successfully.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error updating record: {e}")

    # Call the refresh_table method in the parent ViewTrainerFrame
    self.refresh_table()

    # Close the edit form
    self.destroy()




@staticmethod
def record_attendance(member_data, attendance_type):
    try:
        first_name, middle_name, last_name, contact_no=member_data.split(',')
        current_datetime=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

        with sqlite3.connect('register_trainer.db') as conn:
            cursor=conn.cursor()

            # Check the status before recording attendance
            cursor.execute('SELECT status FROM trainer WHERE first_name=? AND last_name=? AND contact_no=?',
                           (first_name, last_name, contact_no))
            status=cursor.fetchone()

            # Assuming 'status' is a tuple with a single element being the status
            if status and status[0] in ['Active', 'On Leave']:
                # Only proceed if the status is 'Active' or 'On Leave'
                with sqlite3.connect('trainer_attendance_records.db') as attendance_conn:
                    attendance_cursor=attendance_conn.cursor()

                    if attendance_type == "Time In":
                        attendance_cursor.execute('''
                               INSERT INTO trainer_attendance (first_name, middle_name, last_name, contact_no, time_in)
                               VALUES (?, ?, ?, ?, ?)
                           ''', (first_name, middle_name, last_name, contact_no, current_datetime))
                        send_sms(contact_no,
                                 f"Hello {first_name}!, You have Successfully Time In. Time In: {current_datetime}, - D'GRIT GYM")

                    elif attendance_type == "Time Out":
                        attendance_cursor.execute('''
                               UPDATE trainer_attendance
                               SET time_out = ?
                               WHERE contact_no = ? AND time_out IS NULL
                           ''', (current_datetime, contact_no))
                        send_sms(contact_no,
                                 f"Hello {first_name}!, You have Successfully Time Out. Time In: {current_datetime}, - D'GRIT GYM")

                    attendance_conn.commit()
                    messagebox.showinfo("Attendance Recorded",
                                        f"{attendance_type} recorded successfully")

            elif status and status[0] in ['Inactive', 'On Leave']:
                messagebox.showwarning("Attendance Denied",
                                       f"Trainer {first_name} {last_name}'s status is inactive. Attendance denied.")

            else:
                # Handle other cases if needed
                pass

            conn.commit()
            # Show appropriate messages or perform further actions based on attendance recording

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error interacting with the database: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

        elif status and status[0] == 'Inactive':
        messagebox.showwarning("Attendance Denied",
                               f"Trainer {first_name} {last_name}'s status is inactive. Attendance denied.")