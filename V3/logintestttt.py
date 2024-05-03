import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
from PIL import ImageTk,Image
from mtn import App
import os
import csv

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


app = ctk.CTk()  #creating cutstom tkinter window
app.geometry("600x440")
app.title('Persion Tech Giriş Ekranı')


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

def user_login():
    username = entry1.get()
    password = entry2.get()

    if authenticate_user(username, password):
        app.destroy
        apphomepage = App()
        # app.withdraw()  # Giriş penceresini gizle
        apphomepage.mainloop()  # Mtn.py'yi başlat
        apphomepage.exit_application()  # Mtn.py'yi kapat
    else:
        messagebox.showerror("Hata", "Kullanıcı Adı veya Şifre Hatalı")



resim_adi = "persion_600_x_440_piksel.png"
resim_dizini = os.path.abspath(os.path.dirname(__file__))
resim_yolu = os.path.join(resim_dizini, resim_adi)
img1 = ImageTk.PhotoImage(Image.open(resim_yolu))
l1=ctk.CTkLabel(master=app,image=img1)
l1.pack()


#creating custom frame
frame=ctk.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

l2=ctk.CTkLabel(master=frame, text="Giriş Yapınız",font=('Century Gothic',20))
l2.place(x=50, y=45)

entry1=ctk.CTkEntry(master=frame, width=220, placeholder_text='Kullanıcı Adı')
entry1.place(x=50, y=110)

entry2=ctk.CTkEntry(master=frame, width=220, placeholder_text='Şifre', show="*")
entry2.place(x=50, y=165)


#Create custom button
button1 = ctk.CTkButton(master=frame, width=220, text="Giriş Yap", command=user_login, corner_radius=6)
button1.place(x=50, y=240)


app.resizable(False,False)


# You can easily integrate authentication system 

app.mainloop()
