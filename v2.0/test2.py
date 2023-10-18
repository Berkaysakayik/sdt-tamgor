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

    def add_item():
        class AddItemDialog(simpledialog.Dialog):
            def body(self, master):
                self.title("Ekle")
                ctk.CTkLabel(master, text="Ürün Tanımı:").grid(row=0, column=0, sticky="w")
                ctk.CTkLabel(master, text="Seri No:").grid(row=1, column=0, sticky="w")
                ctk.CTkLabel(master, text="Parça No:").grid(row=2, column=0, sticky="w")
                ctk.CTkLabel(master, text="Firma Yeri:").grid(row=3, column=0, sticky="w")
                ctk.CTkLabel(master, text="Adet:").grid(row=4, column=0, sticky="w")
                ctk.CTkLabel(master, text="Durum:").grid(row=5, column=0, sticky="w")

                self.urun_tanimi_entry = ctk.CTkEntry(master)
                self.seri_no_entry = ctk.CTkEntry(master)
                self.parca_no_entry = ctk.CTkEntry(master)
                self.firma_yeri_entry = ctk.CTkComboBox(master, values=firma_yerleri)
                self.adet_entry = ctk.CTkEntry(master, validate="key", validatecommand=(master.register(self.validate_integer_input), "%P"))
                self.durum_entry = ctk.CTkComboBox(master, values=durumlar)

                self.urun_tanimi_entry.grid(row=0, column=1)
                self.seri_no_entry.grid(row=1, column=1)
                self.parca_no_entry.grid(row=2, column=1)
                self.firma_yeri_entry.grid(row=3, column=1)
                self.adet_entry.grid(row=4, column=1)
                self.durum_entry.grid(row=5, column=1)

            def validate_integer_input(self, P):
                if P == "" or P.isdigit():
                    return True
                else:
                    return False

            def apply(self):
                new_urun_tanimi = self.urun_tanimi_entry.get()
                new_seri_no = self.seri_no_entry.get()
                new_parca_no = self.parca_no_entry.get()
                new_firma_yeri = self.firma_yeri_entry.get()
                new_adet = self.adet_entry.get()
                new_durum = self.durum_entry.get()

                if new_urun_tanimi and new_seri_no and new_parca_no and new_firma_yeri and new_adet:
                    with open('inventory.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([new_urun_tanimi, new_seri_no, new_parca_no, new_firma_yeri, new_adet, new_durum])
                    self.clear_entries()
                    reload_inventory()
                else:
                    messagebox.showerror("Hata", "Tüm alanların doldurulması zorunludur!")

            def clear_entries(self):
                self.urun_tanimi_entry.delete(0, 'end')
                self.seri_no_entry.delete(0, 'end')
                self.parca_no_entry.delete(0, 'end')
                self.adet_entry.delete(0, 'end')

        add = AddItemDialog(root)
        if add.result:
            reload_inventory()

    def edit_item():
        selected_index = inventory_tabview.index("current")
        if selected_index == "":
            messagebox.showerror("Hata", "Düzenlecek öğe seçiniz!")
            return

        item_data = inventory_list[int(selected_index)]

        class EditDialog(simpledialog.Dialog):
            def body(self, master):
                self.title("Düzenle")
                ctk.CTkLabel(master, text="Ürün Tanımı:").grid(row=0, column=0, sticky="w")
                ctk.CTkLabel(master, text="Seri No:").grid(row=1, column=0, sticky="w")
                ctk.CTkLabel(master, text="Parça No:").grid(row=2, column=0, sticky="w")
                ctk.CTkLabel(master, text="Firma Yeri:").grid(row=3, column=0, sticky="w")
                ctk.CTkLabel(master, text="Adet:").grid(row=4, column=0, sticky="w")
                ctk.CTkLabel(master, text="Durum:").grid(row=5, column=0, sticky="w")

                self.new_urun_tanimi = ctk.CTkEntry(master)
                self.new_urun_tanimi.grid(row=0, column=1)
                self.new_urun_tanimi.insert(0, item_data[0] if item_data[0] is not None else "")

                self.new_seri_no = ctk.CTkEntry(master)
                self.new_seri_no.grid(row=1, column=1)
                self.new_seri_no.insert(0, item_data[1] if item_data[1] is not None else "")

                self.new_parca_no = ctk.CTkEntry(master)
                self.new_parca_no.grid(row=2, column=1)
                self.new_parca_no.insert(0, item_data[2] if item_data[2] is not None else "")

                self.new_firma_yeri_var = tk.StringVar()
                self.new_firma_yeri_combobox = ctk.CTkComboBox(master, textvariable=self.new_firma_yeri_var, values=firma_yerleri)
                self.new_firma_yeri_combobox.grid(row=3, column=1)
                self.new_firma_yeri_combobox.insert(0, item_data[3] if item_data[3] is not None else "")

                self.new_adet = ctk.CTkEntry(master)
                self.new_adet.grid(row=4, column=1)
                self.new_adet.insert(0, item_data[4] if item_data[4] is not None else "")

                self.new_durum_var = ctk.CTkComboBox(master, values=durumlar)
                self.new_durum_var.grid(row=5, column=1)
                self.new_durum_var.insert(0, item_data[5] if item_data[5] is not None else "")

            def apply(self):
                new_urun_tanimi = self.new_urun_tanimi.get()
                new_seri_no = self.new_seri_no.get()
                new_parca_no = self.new_parca_no.get()
                new_firma_yeri = self.new_firma_yeri_var.get()
                new_adet = self.new_adet.get()
                new_durum = self.new_durum_var.get()

                if new_urun_tanimi and new_seri_no and new_parca_no and new_adet:
                    item_data[0] = new_urun_tanimi
                    item_data[1] = new_seri_no
                    item_data[2] = new_parca_no
                    item_data[3] = new_firma_yeri
                    item_data[4] = new_adet
                    item_data[5] = new_durum
                    inventory_tabview.set_tab_text(selected_index, new_urun_tanimi)
                    inventory_tabview.tab_items[selected_index] = item_data
                    with open('inventory.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        for _, item in inventory_tabview.tab_items.items():
                            writer.writerow(item)
                    self.result = True
                    self.destroy()
                    messagebox.showinfo("Başarılı", "Öğe başarıyla düzenlendi!")
                else:
                    messagebox.showerror("Hata", "Tüm alanların doldurulması zorunludur!")

        edit_dialog = EditDialog(root)
        if edit_dialog.result:
            reload_inventory()

    def delete_selected_items():
        selected_tab = inventory_tabview.index("current")
        if selected_tab == "":
            messagebox.showerror("Hata", "Lütfen silinecek öğeyi seçiniz!")
            return

        inventory_tabview.delete_tab(selected_tab)
        del inventory_list[selected_tab]
        with open('inventory.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for _, item in inventory_list.items():
                writer.writerow(item)
        messagebox.showinfo("Başarılı", "Öğe başarıyla silindi.")

    def reload_inventory():
        inventory_list.clear()
        inventory_tabview.clear_tabs()
        file_name = 'inventory.csv'

        if not os.path.exists(file_name):
            open(file_name, 'w').close()

        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                tab_text = row[0]
                item_data = list(row)
                inventory_tabview.create_tab(tab_text, item_data)
                inventory_list[tab_text] = item_data

    def search():
        search_query = search_entry.get().strip().lower()
        if not search_query:
            for tab_text, item_data in inventory_list.items():
                inventory_tabview.tab_items[tab_text] = item_data
        else:
            for tab_text, item_data in inventory_list.items():
                if any(search_query in str(data).strip().lower() for data in item_data):
                    inventory_tabview.tab_items[tab_text] = item_data
                else:
                    inventory_tabview.hide_tab(tab_text)

    frame = ctk.CTkFrame(root)
    frame.grid(row=1, column=0)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    search_frame = ctk.CTkFrame(root)
    search_frame.grid(row=0, column=0, columnspan=4)

    search_label = ctk.CTkLabel(search_frame, text="Ara:")
    search_label.grid(row=0, column=0, padx=5, pady=5)

    search_entry = ctk.CTkEntry(search_frame)
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    search_button = ctk.CTkButton(search_frame, text="Ara", command=search)
    search_button.grid(row=0, column=2, padx=5, pady=5)

    style = ttk.Style()
    style.configure("Treeview", font=("Proxima Nova", 12), rowheight=40, bd=1, relief="solid")
    style.configure("Treeview.Heading", font=("Proxima Nova", 12))

    inventory_tabview = ctk.CTkTabview(root)
    inventory_tabview.grid(row=1, column=0, padx=5, pady=5, sticky='nsew', columnspan=6)

    vsb = ctk.CTkScrollbar(root, command=inventory_tabview)
    vsb.grid(row=1, column=4, sticky='ns')
    inventory_tabview.configure(yscrollcommand=vsb.set)

    button_frame = ctk.CTkFrame(root)
    button_frame.grid(row=2, column=0, columnspan=4)

    add_button = ctk.CTkButton(button_frame, text="Ekle", command=add_item)
    add_button.grid(row=0, column=0, padx=5, pady=5)

    edit_button = ctk.CTkButton(button_frame, text="Düzenle", command=edit_item)
    edit_button.grid(row=0, column=1, padx=5, pady=5)

    delete_selected_button = ctk.CTkButton(button_frame, text="Sil (Çoklu silme)", command=delete_selected_items)
    delete_selected_button.grid(row=0, column=2, padx=5, pady=5)

    refresh_button = ctk.CTkButton(button_frame, text="Yenile", command=reload_inventory)
    refresh_button.grid(row=0, column=3, padx=5, pady=5)

    inventory_list = {}
    reload_inventory()

    root.state('zoomed')
    root.mainloop()

if __name__ == "__main__":
    main()
