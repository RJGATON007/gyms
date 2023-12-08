# with sqlite3.connect('registration_form.db') as conn:
#     cursor=conn.cursor()
#
#     # Create a table to store registration information
# cursor.execute('''
#                  CREATE TABLE IF NOT EXISTS registration (
#                      id INTEGER PRIMARY KEY AUTOINCREMENT,
#                      first_name TEXT,
#                      middle_name TEXT,
#                      last_name TEXT,
#                      age INTEGER,
#                      sex TEXT,
#                      birth_date DATE,
#                      address TEXT,
#                      nationality TEXT,
#                      contact_no TEXT,
#                      email TEXT,
#                      emergency_contact_no TEXT,
#                      subscription_id TEXT,
#                      subscription_plan TEXT,
#                      start_date DATE,
#                      end_date DATE,
#                      user_reference TEXT,
#                      status TEXT DEFAULT 'Ongoing'
#                  )
#              ''')
#
# # Commit the changes and close the database connection
# conn.commit()
# conn.close()
#
#
# # Create a connection to the database (or create it if it doesn't exist)
#         conn=sqlite3.connect('register_equipment.db')
#
#         # Create a cursor object to interact with the database
#         cursor=conn.cursor()
#
#         # Create a table to store registration information
#         cursor.execute('''
#                        CREATE TABLE IF NOT EXISTS equipment (
#                            id INTEGER PRIMARY KEY,
#                             equipment_name TEXT NOT NULL,
#                             equipment_brand TEXT NOT NULL,
#                             equipment_model TEXT NOT NULL,
#                             equipment_serial_number TEXT NOT NULL,
#                             equipment_quantity TEXT NOT NULL,
#                             equipment_condition TEXT NOT NULL,
#                             equipment_type TEXT NOT NULL,
#                             equipment_status TEXT NOT NULL,
#                             equipment_location TEXT NOT NULL,
#                             equipment_training_required TEXT NOT NULL
#                        )
#                    ''')
#
#         # Commit the changes and close the database connection
#         conn.commit()
#         conn.close()
#
# # Create a connection to the database (or create it if it doesn't exist)
# conn=sqlite3.connect('register_trainer.db')
#
# # Create a cursor object to interact with the database
# cursor=conn.cursor()
#
# # Create a table to store registration information
# cursor.execute('''
#                       CREATE TABLE IF NOT EXISTS trainer (
#                           id INTEGER PRIMARY KEY,
#                           first_name TEXT,
#                           middle_name TEXT,
#                           last_name TEXT,
#                           age INTEGER,
#                           sex TEXT,
#                           birth_date DATE,
#                           address TEXT,
#                           nationality TEXT,
#                           contact_no TEXT,
#                           email TEXT,
#                           emergency_contact_no TEXT
#                       )
#                   ''')
#
# # Commit the changes and close the database connection
# conn.commit()
# conn.close()
#
#
# # Create a connection to the database (or create it if it doesn't exist)
#         try:
#             with sqlite3.connect('visitors_log.db') as conn:
#                 # Create a cursor object to interact with the database
#                 cursor=conn.cursor()
#
#                 # Create a table to store registration information
#                 cursor.execute('''
#                     CREATE TABLE IF NOT EXISTS visitors (
#                         id INTEGER PRIMARY KEY,
#                         first_name TEXT,
#                         middle_name TEXT,
#                         last_name TEXT,
#                         contact_no TEXT,
#                         time TEXT
#                     )
#                 ''')
#
#                 # Commit the changes
#                 conn.commit()
#
#         except sqlite3.Error as e:
#             print(f"SQLite error: {e}")
#
#
# # Create a connection to the database (or create it if it doesn't exist)
#         conn=sqlite3.connect('register_employee.db')
#
#         # Create a cursor object to interact with the database
#         cursor=conn.cursor()
#
#         # Create a table to store registration information
#         cursor.execute('''
#                                  CREATE TABLE IF NOT EXISTS employees (
#                                      id INTEGER PRIMARY KEY,
#                                      first_name TEXT,
#                                      middle_name TEXT,
#                                      last_name TEXT,
#                                      age INTEGER,
#                                      sex TEXT,
#                                      birth_date DATE,
#                                      address TEXT,
#                                      nationality TEXT,
#                                      contact_no TEXT,
#                                      email TEXT,
#                                      emergency_contact_no TEXT
#                                  )
#                              ''')
#
#         # Commit the changes and close the database connection
#         conn.commit()
#         conn.close()