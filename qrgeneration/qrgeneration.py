from tkinter import *
import qrcode
from PIL import ImageTk
from resizeimage import resizeimage


class QrGenerate:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x500+200+50")
        self.root.title("D'Grit Gym QR Code Generator")
        self.root.resizable(False, False)

        title = Label(self.root, text="QR CODE GENERATOR", font=("Arial Bold", 25), bg='green', fg='white',
                      anchor='w').place(x=0, y=0, relwidth=1),

        self.var_emp_code = StringVar()
        self.var_emp_name = StringVar()
        self.var_emp_age = StringVar()
        self.var_emp_address = StringVar()
        self.var_emp_contact = StringVar()

        emp_Frame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        emp_Frame.place(x=50, y=100, width=500, height=380)

        emp_title = Label(
            emp_Frame, text=" Member Details", font=("Arial bold", 20), bg='green', fg='white').place(
            x=0,
            y=0,
            relwidth=1),

        lbl_emp_code = Label(emp_Frame, text=" Member ID", font=("Arial", 15, 'bold'), bg='white').place(
            x=20, y=60),
        lbl_name = Label(emp_Frame, text=" Name", font=("Arial", 15, 'bold'), bg='white').place(x=20, y=100),
        lbl_age = Label(emp_Frame, text=" Age", font=("Arial", 15, 'bold'), bg='white').place(x=20, y=140),
        lbl_address = Label(emp_Frame, text=" Address", font=("Arial", 15, 'bold'), bg='white').place(
            x=20, y=180),
        lbl_contact = Label(emp_Frame, text=" Contact Number", font=("Arial", 15, 'bold'), bg='white').place(
            x=20,
            y=220),

        txt_emp_code = Entry(
            emp_Frame, font=("Arial", 15, 'bold'), textvariable=self.var_emp_code,
            bg='lightblue').place(x=200, y=60),
        txt_name = Entry(
            emp_Frame, font=("Arial", 15, 'bold'), textvariable=self.var_emp_name, bg='lightblue').place(
            x=200, y=100),
        txt_age = Entry(
            emp_Frame, font=("Arial", 15, 'bold'), textvariable=self.var_emp_age, bg='lightblue').place(
            x=200, y=140),
        txt_address = Entry(emp_Frame, font=("Arial", 15, 'bold'), textvariable=self.var_emp_address,
                            bg='lightblue').place(x=200, y=180),
        txt_contact = Entry(
            emp_Frame, font=("Arial", 15, 'bold'), textvariable=self.var_emp_contact,
            bg='lightblue').place(x=200, y=220),

        btn_generate = Button(
            emp_Frame, text='Generate QR', command=self.generate, font=("Arial", 18, 'bold'),
            bg='navy blue', fg='white').place(x=90, y=270, width=180, height=30),
        btn_clear = Button(
            emp_Frame, text='Clear', command=self.clear, font=("Arial", 18, 'bold'), bg='red',
            fg='white').place(x=282, y=270, width=120, height=30),

        self.msg = ''
        self.lbl_msg = Label(emp_Frame, text=self.msg, font=("Calibri bold", 20), bg='white', fg='green')
        self.lbl_msg.place(x=0, y=310, relwidth=1)

        # -----Employee QR Code window-----
        qr_Frame = Frame(self.root, bd=2, relief=RIDGE, bg='white')
        qr_Frame.place(x=600, y=100, width=250, height=380)

        emp_title = Label(qr_Frame, text=" Member QR Code", font=("Calibri bold", 15), bg='green', fg='white').place(
            x=0, y=0, relwidth=1),

        self.qr_code = Label(qr_Frame, text="No Qr \nAvailable", font=("Calibri bold", 10), bg='grey', fg='white', bd=1,
                             relief=RIDGE)
        self.qr_code.place(x=35, y=100, width=180, height=180)

    def clear(self):
        self.var_emp_code.set('')
        self.var_emp_name.set('')
        self.var_emp_age.set('')
        self.var_emp_address.set('')
        self.var_emp_contact.set('')
        self.msg = ''
        self.lbl_msg.config(text=self.msg)
        self.qr_code.config(image='')

    def generate(self):
        if self.var_emp_age.get() == '' or self.var_emp_code.get() == '' or self.var_emp_address.get() == '' or self.var_emp_name.get() == '' or self.var_emp_contact.get() == '':
            self.msg = 'All fields are Required!!!'
            self.lbl_msg.config(text=self.msg, fg='red')
        else:
            qr_data = (
                f"Member ID: {self.var_emp_code.get()}\nMember Name:{self.var_emp_name.get()}\nAge:{self.var_emp_age.get()}\nAddress:{self.var_emp_address.get()}\nContact:{self.var_emp_contact.get()}")
            qr_code = qrcode.make(qr_data)
            print(qr_code)
            qr_code = resizeimage.resize_cover(qr_code, [180, 180])
            qr_code.save("member_qr/Emp_" + str(self.var_emp_code.get()) + '.png')
            # --------QR Code Image Update---------
            self.image = ImageTk.PhotoImage(file="member_qr/Emp_" + str(self.var_emp_code.get()) + '.png')
            self.qr_code.config(image=self.image)
            # --------updating Notification-------
            self.msg = 'QR Generated Successfully!!'
            self.lbl_msg.config(text=self.msg, fg='green')


root = Tk()
obj = QrGenerate(root)
root.mainloop()
