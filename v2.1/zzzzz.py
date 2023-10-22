import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import os

class InventoryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("PersioN Envanter Takip Programı v1.0")
        self.firma_yerleri = ["Tamgör", "SDT", "SDT-Tamgör"]
        self.durumlar = ["Yeni", "Kullanılmış", "Arızalı"]

        self.create_widgets()
        self.reload_inventory()

    def create_widgets(self):
        self.create_main_frame()
        self.create_treeview()
        self.create_buttons()

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

    def create_treeview(self):
        columns = ("Ürün Tanımı", "Seri No", "Parça No", "Firma Yeri", "Adet", "Durum")
        self.treeview = ttk.Treeview(self.main_frame, columns=columns, show="headings")
        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=150)
        self.treeview.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        vsb = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.treeview.yview)
        vsb.grid(row=0, column=2, sticky='ns')
        self.treeview.configure(yscrollcommand=vsb.set)

    def create_buttons(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Ekle", command=self.add_item).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Düzenle", command=self.edit_item).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Sil (Çoklu silme)", command=self.delete_selected_items).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Yenile", command=self.reload_inventory).grid(row=0, column=3, padx=5)

    def add_item(self):
        item_data = self.show_item_dialog("Ekle")
        if item_data:
            self.add_item_to_inventory(item_data)

    def edit_item(self):
        selected_index = self.treeview.selection()
        if not selected_index:
            messagebox.showerror("Hata", "Düzenlecek öğe seçiniz!")
            return

        selected_index = selected_index[0]
        item_data = self.show_item_dialog("Düzenle", self.get_item_data(selected_index))
        if item_data:
            self.update_item_in_inventory(selected_index, item_data)

    def show_item_dialog(self, title, item_data=None):
        dialog = simpledialog.Dialog(self.root, title=title)
        dialog.geometry("300x200")
        ttk.Label(dialog, text="Ürün Tanımı:").pack()
        urun_tanimi = simpledialog.askstring(title, "Ürün Tanımı:", initialvalue=item_data[0] if item_data else "")
        if urun_tanimi is None:
            return None  # Kullanıcı pencereyi kapattıysa işlemi iptal et
        seri_no = simpledialog.askstring(title, "Seri No:", initialvalue=item_data[1] if item_data else "")
        parca_no = simpledialog.askstring(title, "Parça No:", initialvalue=item_data[2] if item_data else "")
        firma_yeri = simpledialog.askstring(title, "Firma Yeri:", initialvalue=item_data[3] if item_data else "")
        adet = simpledialog.askinteger(title, "Adet:", initialvalue=item_data[4] if item_data else 0)
        durum = simpledialog.askstring(title, "Durum:", initialvalue=item_data[5] if item_data else "", 
                              parent=self.root)
        return urun_tanimi, seri_no, parca_no, firma_yeri, adet, durum

    def add_item_to_inventory(self, item_data):
        with open('inventory.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(item_data)
        self.reload_inventory()
        messagebox.showinfo("Başarılı", "Öğe başarıyla envantere eklendi!")

    def update_item_in_inventory(self, selected_index, item_data):
        item_data = list(item_data)
        self.treeview.item(selected_index, values=item_data)

        inventory_list = self.get_inventory()
        inventory_list[int(selected_index.lstrip('I'))] = item_data

        with open('inventory.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for item in inventory_list:
                writer.writerow(item)

        messagebox.showinfo("Başarılı", "Öğe başarıyla düzenlendi!")

    def delete_selected_items(self):
        selected_indices = self.treeview.selection()
        if not selected_indices:
            messagebox.showerror("Hata", "Lütfen silinecek öğe/öğeleri seçiniz!")
            return

        # Seçilen indeksleri öğe numaralarına dönüştürme
        oge_nolar = [int(selected_index.lstrip('I')) for selected_index in selected_indices]

        # Dizin çakışmalarını önlemek için seçili öğeleri ters sırayla silme
        inventory_list = self.get_inventory()
        for oge_no in sorted(oge_nolar, reverse=True):
            selected_index = f'I{oge_no}'
            self.treeview.delete(selected_index)
            inventory_list.pop(oge_no)

        with open('inventory.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for item in inventory_list:
                writer.writerow(item)

        messagebox.showinfo("Başarılı", "Öğe/Öğeler başarıyla silindi!")

    def reload_inventory(self):
        self.treeview.delete(*self.treeview.get_children())
        inventory_list = self.get_inventory()
        for i, row in enumerate(inventory_list):
            self.treeview.insert('', 'end', values=row, iid=f'I{i}')

    def get_inventory(self):
        inventory_list = []
        file_name = 'inventory.csv'

        # Check if the file exists, and create it if it doesn't
        if not os.path.exists(file_name):
            open(file_name, 'w').close()

        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                inventory_list.append(row)

        return inventory_list

    def get_item_data(self, selected_index):
        inventory_list = self.get_inventory()
        return inventory_list[int(selected_index.lstrip('I'))]

def main():
    root = tk.Tk()
    app = InventoryManager(root)
    root.state('zoomed')
    root.mainloop()

if __name__ == "__main__":
    main()
