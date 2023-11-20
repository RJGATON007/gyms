# Combine all the data entries into a single string
data_string=f"{first_name},{middle_name},{last_name},{contact_no}"

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


def download_qr_code(self):
    # Download the displayed QR code and save it to the Downloads folder in file explorer
    qr_code_path=os.path.join("trainer_qrcodes", f"dgrit_trainer_{self.trainer_data[3]}.png")
    qr_code_image=Image.open(qr_code_path)

    # Assuming self.member_data[3] is the unique identifier for the member
    save_path=os.path.join(os.path.expanduser("~"), "Downloads", f"dgrit_trainer_{self.trainer_data[3]}.png")
    qr_code_image.save(save_path)

    # show a success message
    messagebox.showinfo("Download Successful", "QR Code downloaded successfully.")
