import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.simpledialog import Dialog
import csv
from ttkthemes import ThemedTk
import os
import customtkinter as ctk

def main():
    root = ctk.CTk()
    ctk.set_appearance_mode("dark")

    firma_yerleri = ["Tamgör", "SDT", "SDT-Tamgör"]
    durumlar = ["Yeni", "Kullanılmış", "Arızalı"]

    class MyTabView(ctk.CTkTabview):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

            # create tabs
            self.add("tab 1")
            self.add("tab 2")

            # add widgets on tabs
            self.label = ctk.CTkLabel(master=self.tab("tab 1"))
            self.label.grid(row=0, column=0, padx=20, pady=10)


    class App(ctk.CTk):
        def __init__(self):
            super().__init__()

            self.tab_view = MyTabView(master=self)
            self.tab_view.grid(row=0, column=0, padx=20, pady=20)


    app = App()
    app.mainloop()

    root.state('zoomed')
    root.mainloop()

if __name__ == "__main__":
    main()
