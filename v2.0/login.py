import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

# Create a themed Tkinter window
root = tk.Tk()
root.title("PersioN Envanter Takip Programı v2.0")

# Example user authentication function
def authenticate_user(username, password):
    file_name = 'users.csv'

    # Check if the file exists, and create it if it doesn't
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='') as file:
            pass  # Create an empty file if it doesn't exist

    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and len(row) >= 2 and row[0] == username and row[1] == password:
                return True
    return False

# Function to show the main program interface
def show_program_interface():
    root.destroy()
    import persion_env_tracker_v2

# Example user login function
def user_login():
    username = username_entry.get()
    password = password_entry.get()

    if authenticate_user(username, password):
        # messagebox.showinfo("Başarılı", "Giriş Başarılı")
        show_program_interface()  # Show the main program interface
    else:
        messagebox.showerror("Hata", "Kullanıcı Adı veya Şifre Hatalı")

# User login components
username_label = ttk.Label(root, text="Kullanıcı Adı:")
username_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
username_entry = ttk.Entry(root, font=('Helvetica', 12))
username_entry.grid(row=1, column=1, padx=10, pady=5)

password_label = ttk.Label(root, text="Şifre:")
password_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
password_entry = ttk.Entry(root, show="*", font=('Helvetica', 12))
password_entry.grid(row=2, column=1, padx=10, pady=5)

login_button = ttk.Button(root, text="Giriş", command=user_login)
login_button.grid(row=3, column=0, columnspan=2, pady=10)
login_button['style'] = 'TButton'

# Styling
style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 14))
style.configure('TButton', font=('Helvetica', 14))

# Start the tkinter main loop
root.mainloop()



