# import tkinter as tk
# from tkinter import messagebox, simpledialog, ttk
# from tkinter.simpledialog import Dialog
# import csv
# from ttkthemes import ThemedTk
# from PIL import Image, ImageTk
# import os

# # Create a themed Tkinter window
# root = ThemedTk(theme="adapta")  # You can choose a different theme like 'Arc', 'equilux', etc.
# root.title("PersioN Envanter Takip Programı v1.0")

# # Custom validation function to allow only integer input
# def validate_integer_input(P):
#     if P == "" or P.isdigit():
#         return True
#     else:
#         return False

# # Envantere yeni bir öğe ekleme fonksiyonu
# def oge_ekle():
#     urun_tanimi = urun_tanimi_entry.get()
#     seri_no = seri_no_entry.get()
#     parca_no = parca_no_entry.get()
#     adet = adet_entry.get()

#     if urun_tanimi and seri_no and parca_no and adet:
#         with open('inventory.csv', 'a', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow([urun_tanimi, seri_no, parca_no, adet])
#         clear_entries()
#         messagebox.showinfo("Başarılı", "Öğe başarıyla envantere eklendi!")
#         load_inventory()
#     else:
#         messagebox.showerror("Hata", "Tüm alanların doldurulması zorunludur!")

# # Girdi alanlarını temizleme fonksiyonu
# def clear_entries():
#     urun_tanimi_entry.delete(0, 'end')
#     seri_no_entry.delete(0, 'end')
#     parca_no_entry.delete(0, 'end')
#     adet_entry.delete(0, 'end')

# # Seçilen öğeyi düzenleme fonksiyonu
# def oge_duzenle():
#     selected_index = inventory_treeview.selection()
#     if not selected_index:
#         messagebox.showerror("Hata", "Düzenlecek öğe seçiniz!")
#         return

#     selected_index = inventory_treeview.selection()[0]
#     item_data = inventory_list[int(selected_index.lstrip('I'))]

#     # Düzenlenecek alanları tek bir pencerede oluşturma
#     class EditDialog(Dialog):
#         def body(self, master):
#             self.title("Düzenle")
#             ttk.Label(master, text="Ürün Tanımı:").grid(row=0, column=0, sticky="w")
#             ttk.Label(master, text="Seri No:").grid(row=1, column=0, sticky="w")
#             ttk.Label(master, text="Parça No:").grid(row=2, column=0, sticky="w")
#             ttk.Label(master, text="Adet:").grid(row=3, column=0, sticky="w")

#             self.new_urun_tanimi = ttk.Entry(master)
#             self.new_urun_tanimi.grid(row=0, column=1)
#             self.new_urun_tanimi.insert(0, item_data[0])

#             self.new_seri_no = ttk.Entry(master)
#             self.new_seri_no.grid(row=1, column=1)
#             self.new_seri_no.insert(0, item_data[1])

#             self.new_parca_no = ttk.Entry(master)
#             self.new_parca_no.grid(row=2, column=1)
#             self.new_parca_no.insert(0, item_data[2])

#             self.new_adet = ttk.Entry(master)
#             self.new_adet.grid(row=3, column=1)
#             self.new_adet.insert(0, item_data[3])

#         def apply(self):
#             new_urun_tanimi = self.new_urun_tanimi.get()
#             new_seri_no = self.new_seri_no.get()
#             new_parca_no = self.new_parca_no.get()
#             new_adet = self.new_adet.get()

#             if new_urun_tanimi and new_seri_no and new_parca_no and new_adet:
#                 item_data[0] = new_urun_tanimi
#                 item_data[1] = new_seri_no
#                 item_data[2] = new_parca_no
#                 item_data[3] = new_adet
#                 inventory_treeview.item(selected_index, values=item_data)
#                 with open('inventory.csv', 'w', newline='') as file:
#                     writer = csv.writer(file)
#                     for item in inventory_list:
#                         writer.writerow(item)
#                 self.result = True
#                 self.destroy()
#                 messagebox.showinfo("Başarılı", "Öğe başarıyla düzenlendi!")
#             else:
#                 messagebox.showerror("Hata", "Tüm alanların doldurulması zorunludur!")

#     edit_dialog = EditDialog(root)
#     if edit_dialog.result:
#         load_inventory()

# # Seçilen öğe/öğeleri silme fonksiyonu
# def delete_selected_items():
#     selected_indices = inventory_treeview.selection()
#     if not selected_indices:
#         messagebox.showerror("Hata", "Lütfen silinecek öğe/öğeleri seçiniz!")
#         return

#     # Seçilen indeksleri öğe numaralarına dönüştürme
#     oge_nolar = [int(selected_index.lstrip('I')) for selected_index in selected_indices]

#     # Dizin çakışmalarını önlemek için seçili öğeleri ters sırayla silme
#     for oge_no in sorted(oge_nolar, reverse=True):
#         selected_index = f'I{oge_no}'
#         inventory_treeview.delete(selected_index)
#         inventory_list.pop(oge_no)

#     with open('inventory.csv', 'w', newline='') as file:
#         writer = csv.writer(file)
#         for item in inventory_list:
#             writer.writerow(item)

#     messagebox.showinfo("Başarılı", "Öğe/Öğeler başarıyla silindi.")

# # Function to load and display the inventory
# def load_inventory():
#     # Clear the inventory_list to avoid duplicates
#     inventory_list.clear()

#     inventory_treeview.delete(*inventory_treeview.get_children())

#     file_name = 'inventory.csv'

#     # Check if the file exists, and create it if it doesn't
#     if not os.path.exists(file_name):
#         open(file_name, 'w').close()

#     with open(file_name, 'r') as file:
#         reader = csv.reader(file)
#         for i, row in enumerate(reader):
#             inventory_treeview.insert('', 'end', values=row, iid=f'I{i}')
#             inventory_list.append(list(row))




# # Create labels and entry fields for input
# urun_tanimi_label = ttk.Label(root, text="Ürün Tanımı:")
# urun_tanimi_label.grid(row=0, column=0, sticky="w", padx=5)
# urun_tanimi_entry = ttk.Entry(root)
# urun_tanimi_entry.grid(row=0, column=1, padx=5)

# seri_no_label = ttk.Label(root, text="Seri No:")
# seri_no_label.grid(row=1, column=0, sticky="w", padx=5)
# seri_no_entry = ttk.Entry(root)
# seri_no_entry.grid(row=1, column=1, padx=5)

# parca_no_label = ttk.Label(root, text="Parça No:")
# parca_no_label.grid(row=2, column=0, sticky="w", padx=5)
# parca_no_entry = ttk.Entry(root)
# parca_no_entry.grid(row=2, column=1, padx=5)

# # Create an Entry widget for the "Adet" field with integer validation
# adet_label = ttk.Label(root, text="Adet:")
# adet_label.grid(row=3, column=0, sticky="w", padx=5)
# adet_entry = ttk.Entry(root, validate="key", validatecommand=(root.register(validate_integer_input), "%P"))
# adet_entry.grid(row=3, column=1, padx=5)

# # Create an "Add Item" button
# add_button = ttk.Button(root, text="Ekle", command=oge_ekle)
# add_button.grid(row=4, column=0, columnspan=2, padx=5)

# # Create an "Düzenle" button
# edit_button = ttk.Button(root, text="Düzenle", command=oge_duzenle)
# edit_button.grid(row=5, column=0, columnspan=2, padx=5)

# # Create a "Delete Selected" button
# delete_selected_button = ttk.Button(root, text="Sil (Çoklu silme)", command=delete_selected_items)
# delete_selected_button.grid(row=6, column=0, columnspan=2, padx=5)

# # Create a "Refresh" button to reload the inventory
# refresh_button = ttk.Button(root, text="Yenile", command=load_inventory)
# refresh_button.grid(row=7, column=0, columnspan=2, padx=5)

# # Create a frame to contain the Treeview widget
# frame = ttk.Frame(root)
# frame.grid(row=0, column=2, rowspan=8, sticky="nsew", padx=5)

# # Create a Treeview widget to display the inventory with grid lines
# style = ttk.Style()
# style.configure("Treeview", font=("Proxima Nova", 12), rowheight=20, bd=1, relief="solid")
# style.configure("Treeview.Heading", font=("Proxima Nova", 12))

# inventory_treeview = ttk.Treeview(frame, columns=("Ürün Tanımı", "Seri No", "Parça No", "Adet"), show="headings", style="Treeview")
# inventory_treeview.heading("Ürün Tanımı", text="Ürün Tanımı", anchor="w")
# inventory_treeview.heading("Seri No", text="Seri No", anchor="w")
# inventory_treeview.heading("Parça No", text="Parça No", anchor="w")
# inventory_treeview.heading("Adet", text="Adet", anchor="w")
# inventory_treeview.grid(row=0, column=0, sticky='nsew')

# vsb = ttk.Scrollbar(frame, orient="vertical", command=inventory_treeview.yview)
# vsb.grid(row=0, column=1, sticky='ns')
# inventory_treeview.configure(yscrollcommand=vsb.set)

# frame.grid_rowconfigure(0, weight=1)
# frame.grid_columnconfigure(0, weight=1)

# # Initialize the inventory list
# inventory_list = []

# # Load the inventory initially
# load_inventory()

# # Set the window size to fill the screen
# root.state('zoomed')

# # Start the tkinter main loop
# root.mainloop()