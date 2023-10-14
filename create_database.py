import sqlite3

# create database named 'database.db'
conn = sqlite3.connect('database.db')

# create table named 'users'
conn.execute('CREATE TABLE users (username TEXT, password TEXT)')
conn.commit()

# create table named 'members' with the following columns: firstname, middle name, lastname, age, sex, date_of_birth, address, nationality, contact_number, email_address, emergency_contact, subscription_id, subscription_plan, subscription_start, subscription_end, user_reference
conn.execute('CREATE TABLE members (first_name TEXT,middle_name TEXT,last_name TEXT,age TEXT,sex TEXT,birth_date TEXT,address TEXT,nationality TEXT,contact_no TEXT,email_address TEXT,emergency_contact_no TEXT,subscription_id TEXT,subscription_plan TEXT,subscription_start TEXT,subscription_end TEXT,user_reference TEXT)')
conn.commit()

conn.close()
