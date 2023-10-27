import tkinter
import tkinter.messagebox
import customtkinter
import tkinter as tk
from tkinter import ttk  # Treeview widget için
from tkinter import messagebox
import csv
import os


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.inventory_list = []

        # configure window
        self.title("PersioN Envanter Takip Programı")
        self.geometry(f"{1500}x{680}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        #  sidebar frame  widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="PERSION", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_Ekle = customtkinter.CTkButton(self.sidebar_frame, text="Ekle",command=self.add_item)
        self.sidebar_Ekle.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_Düzenle = customtkinter.CTkButton(self.sidebar_frame,text="Düzenle", command=self.edit_item)
        self.sidebar_Düzenle.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_Sil = customtkinter.CTkButton(self.sidebar_frame,text="Sil(Çoklu silme)", command=self.delete_item)
        self.sidebar_Sil.grid(row=3, column=0, padx=20, pady=10)        
        self.sidebar_Yenile = customtkinter.CTkButton(self.sidebar_frame,text="Yenile", command=self.reload_inventory)
        self.sidebar_Yenile.grid(row=4, column=0, padx=20, pady=10)


        # create main entry and button
        self.entry_ara = customtkinter.CTkEntry(self, placeholder_text="Aramak istediğiniz ürünü giriniz.")
        self.entry_ara.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_ara = customtkinter.CTkButton(master=self,text="ARA", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),command=self.search_item)
        self.main_button_ara.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.check1_var = tk.IntVar()
        self.check2_var = tk.IntVar()
        self.check3_var = tk.IntVar()

        self.result_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.result_frame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(10, 10), sticky="nsew")

        self.check1 = customtkinter.CTkCheckBox(self.result_frame, text="SDT", variable=self.check1_var)
        self.check2 = customtkinter.CTkCheckBox(self.result_frame, text="TAMGÖR", variable=self.check2_var)
        self.check3 = customtkinter.CTkCheckBox(self.result_frame, text="ORTAKLIK", variable=self.check3_var)

        self.check1.grid(row=0, column=0, padx=(20, 0), pady=(20, 0))
        self.check2.grid(row=0, column=1, padx=(20, 0), pady=(20, 0))
        self.check3.grid(row=0, column=2, padx=(20, 0), pady=(20, 0))

        



        # create treeview
        self.style = ttk.Style()
        self.style.configure("Treeview", font=("Proxima Nova", 10), rowheight=40, relief="solid")
        self.inventory_treeview = ttk.Treeview(self, columns=("Ürün Tanımı", "Seri No", "Parça No", "Adet",  "Şirket", "Durum"), show="headings", style="Treeview",padding=20)
        self.inventory_treeview.heading("Ürün Tanımı", text="Ürün Tanımı", anchor="w")
        self.inventory_treeview.heading("Seri No", text="Seri No", anchor="w")
        self.inventory_treeview.heading("Parça No", text="Parça No", anchor="w")
        self.inventory_treeview.heading("Adet", text="Adet", anchor="w")
        self.inventory_treeview.heading("Şirket", text="Şirket", anchor="w")
        self.inventory_treeview.heading("Durum", text="Durum", anchor="w")

        self.inventory_treeview.column("Ürün Tanımı", width=150, anchor="w")  # İlk sütun için genişlik ve hizalama ayarlandı
        self.inventory_treeview.column("Seri No", width=50, anchor="w")
        self.inventory_treeview.column("Parça No", width=50, anchor="w")
        self.inventory_treeview.column("Adet", width=20, anchor="w")
        self.inventory_treeview.column("Şirket", width=30, anchor="w")
        self.inventory_treeview.column("Durum", width=30, anchor="w")
        self.inventory_treeview.grid(column=0, row=0, sticky="s")
        self.inventory_treeview.columnconfigure(0, weight=1)

        self.inventory_treeview.grid(row=0, column=1,  padx=(0, 0), pady=(0, 0), sticky="nsew")
        
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.inventory_treeview.yview)
        vsb.grid(row=0, column=2, sticky='ns')
        self.inventory_treeview.configure(yscrollcommand=vsb.set)
        self.reload_inventory()
 

    def add_item(self):
        self.new_frame = customtkinter.CTkFrame(self)
        self.new_frame.grid(row=0, column=3, padx=(10, 20), pady=(10, 0), sticky="nsew")
        self.logo_label = customtkinter.CTkLabel(self.new_frame, text="EKLE", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(10, 10))

        self.entry1lbl = customtkinter.CTkLabel(master=self.new_frame,text="Ürün Tanımı:"  )
        self.entry1lbl.grid(row=1, column=0, pady=(10, 0), padx=5, sticky="n")
        self.entry1 = customtkinter.CTkEntry(master=self.new_frame)
        self.entry1.grid(row=1, column=1, pady=(10, 0), padx=10, sticky="n")
        self.entry2lbl = customtkinter.CTkLabel(master=self.new_frame,text="Seri No:"  )
        self.entry2lbl.grid(row=2, column=0, pady=(10, 0), padx=10, sticky="n")
        self.entry2 = customtkinter.CTkEntry(master=self.new_frame)
        self.entry2.grid(row=2, column=1, pady=(10, 0), padx=10, sticky="n")
        self.entry3lbl = customtkinter.CTkLabel(master=self.new_frame,text="Parça No:")
        self.entry3lbl.grid(row=3, column=0, pady=(10, 0), padx=10, sticky="n")
        self.entry3 = customtkinter.CTkEntry(master=self.new_frame)
        self.entry3.grid(row=3, column=1, pady=(10, 0), padx=10, sticky="n")
        self.label4 = customtkinter.CTkLabel(master=self.new_frame, text="Adet:")
        self.label4.grid(row=4, column=0, padx=5, pady=(10, 0),sticky="n")
        self.entry4 = customtkinter.CTkEntry(master=self.new_frame, validate="key", validatecommand=(self.new_frame.register(self.validate_integer_input), "%P"))
        self.entry4.grid(row=4, column=1, pady=(10, 0), padx=5, sticky="n")
  
        self.appearance_mode_label = customtkinter.CTkLabel(master=self.new_frame, text="Firma Yeri:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(master=self.new_frame ,values=["SDT", "TAMGÖR", "ORTAKLIK"])
        self.appearance_mode_optionemenu.grid(row=5, column=1, padx=20, pady=(20, 10))
        self.appearance_mode_label1 = customtkinter.CTkLabel(master=self.new_frame, text="Durum:", anchor="w")
        self.appearance_mode_label1.grid(row=6, column=0, padx=20, pady=(20, 0))
        self.appearance_mode_optionemenu1 = customtkinter.CTkOptionMenu(master=self.new_frame ,values=["Yeni", "Kullanılmış", "Arızalı"])
        self.appearance_mode_optionemenu1.grid(row=6, column=1, padx=20, pady=(20, 10))
        
        self.add_buton=customtkinter.CTkButton(master=self.new_frame, text="Tamam",command=self.apply ,width=50)
        self.add_buton.grid(row=7, column=0, padx=20, pady=(20, 0))


    def validate_integer_input(self, P):
        if P == "" or P.isdigit():
            return True
        else:
            return False


    def apply(self):
                new_urun_tanimi = self.entry1.get()
                new_seri_no = self.entry2.get()
                new_parca_no = self.entry3.get()
                new_adet = self.entry4.get()
                new_firma_yeri = self.appearance_mode_optionemenu.get()
                new_durum = self.appearance_mode_optionemenu1.get()

                if new_urun_tanimi and new_seri_no and new_parca_no and new_firma_yeri and new_adet:
                    with open('inventory.csv', 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([new_urun_tanimi, new_seri_no, new_parca_no,new_adet,new_firma_yeri , new_durum])
                    self.clear_entries()
                    messagebox.showinfo("Başarılı", "Öğe başarıyla envantere eklendi!")
                    self.reload_inventory()
                else:
                    messagebox.showerror("Hata", "Tüm alanların doldurulması zorunludur!")

    def clear_entries(self):
                self.entry1.delete(0, 'end')
                self.entry2.delete(0, 'end')
                self.entry3.delete(0, 'end')
                self.entry4.delete(0, 'end')

    def reload_inventory(self):
        # Clear the inventory_list to avoid duplicates
        self.inventory_list.clear()

        self.inventory_treeview.delete(*self.inventory_treeview.get_children())

        file_name = 'inventory.csv'

        # Check if the file exists, and create it if it doesn't
        if not os.path.exists(file_name):
            open(file_name, 'w').close()

        with open(file_name, 'r', encoding='UTF-8') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                self.inventory_treeview.insert('', 'end', values=row, iid=f'I{i}')
                self.inventory_list.append(list(row))

    def edit_item(self):
        self.selected_index = self.inventory_treeview.selection()

        if not self.selected_index:
            messagebox.showerror("Hata", "Düzenlecek öğe seçiniz!")
            return

        self.selected_index = self.inventory_treeview.selection()[0]
        self.item_data = self.inventory_list[int(self.selected_index.lstrip('I'))]

        self.new_frame = customtkinter.CTkFrame(self)
        self.new_frame.grid(row=0, column=3, padx=(10, 20), pady=(10, 0), sticky="nsew")
        self.logo_label = customtkinter.CTkLabel(self.new_frame, text="EKLE", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(10, 10))

        self.entry1lbl = customtkinter.CTkLabel(master=self.new_frame,text="Ürün Tanımı:"  )
        self.entry1lbl.grid(row=1, column=0, pady=(10, 0), padx=5, sticky="n")
        self.entry1 = customtkinter.CTkEntry(master=self.new_frame)
        self.entry1.grid(row=1, column=1, pady=(10, 0), padx=10, sticky="n")
        self.entry1.insert(0, self.item_data[0] if self.item_data[0] is not None else "")

        self.entry2lbl = customtkinter.CTkLabel(master=self.new_frame,text="Seri No:"  )
        self.entry2lbl.grid(row=2, column=0, pady=(10, 0), padx=10, sticky="n")
        self.entry2 = customtkinter.CTkEntry(master=self.new_frame)
        self.entry2.grid(row=2, column=1, pady=(10, 0), padx=10, sticky="n")
        self.entry2.insert(0, self.item_data[1] if self.item_data[1] is not None else "")


        self.entry3lbl = customtkinter.CTkLabel(master=self.new_frame,text="Parça No:")
        self.entry3lbl.grid(row=3, column=0, pady=(10, 0), padx=10, sticky="n")
        self.entry3 = customtkinter.CTkEntry(master=self.new_frame)
        self.entry3.grid(row=3, column=1, pady=(10, 0), padx=10, sticky="n")
        self.entry3.insert(0, self.item_data[2] if self.item_data[2] is not None else "")

 
        self.label4 = customtkinter.CTkLabel(master=self.new_frame, text="Adet:")
        self.label4.grid(row=4, column=0, padx=5, pady=(10, 0),sticky="n")
        self.entry4 = customtkinter.CTkEntry(master=self.new_frame, validate="key", validatecommand=(self.new_frame.register(self.validate_integer_input), "%P"))
        self.entry4.grid(row=4, column=1, pady=(10, 0), padx=5, sticky="n")
        self.entry4.insert(0, self.item_data[3] if self.item_data[3] is not None else "")

  
        self.appearance_mode_label = customtkinter.CTkLabel(master=self.new_frame, text="Firma Yeri:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(master=self.new_frame ,values=["SDT", "TAMGÖR", "ORTAKLIK"])
        self.appearance_mode_optionemenu.grid(row=5, column=1, padx=20, pady=(20, 10))
        self.appearance_mode_optionemenu.set(self.item_data[4] if self.item_data[4] is not None else "")


        self.appearance_mode_label1 = customtkinter.CTkLabel(master=self.new_frame, text="Durum:", anchor="w")
        self.appearance_mode_label1.grid(row=6, column=0, padx=20, pady=(20, 0))
        self.appearance_mode_optionemenu1 = customtkinter.CTkOptionMenu(master=self.new_frame ,values=["Yeni", "Kullanılmış", "Arızalı"])
        self.appearance_mode_optionemenu1.grid(row=6, column=1, padx=20, pady=(20, 10))
        self.appearance_mode_optionemenu1.set(self.item_data[5] if self.item_data[5] is not None else "")
        
        self.add_buton=customtkinter.CTkButton(master=self.new_frame, text="Tamam",command=self.editapply ,width=50)
        self.add_buton.grid(row=7, column=0, padx=20, pady=(20, 0))

    def editapply(self):
        new_urun_tanimi = self.entry1.get()
        new_seri_no = self.entry2.get()
        new_parca_no = self.entry3.get()
        new_firma_yeri = self.entry4.get()
        new_adet = self.appearance_mode_optionemenu.get()
        new_durum = self.appearance_mode_optionemenu1.get()

        if new_urun_tanimi and new_seri_no and new_parca_no and new_adet:
            self.item_data[0] = new_urun_tanimi
            self.item_data[1] = new_seri_no
            self.item_data[2] = new_parca_no
            self.item_data[3] = new_firma_yeri
            self.item_data[4] = new_adet
            self.item_data[5] = new_durum
            self.inventory_treeview.item(self.selected_index, values=self.item_data)
            with open('inventory.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for item in self.inventory_list:
                    writer.writerow(item)
            self.result = True
            messagebox.showinfo("Başarılı", "Öğe başarıyla düzenlendi!")
        else:
            messagebox.showerror("Hata", "Tüm alanların doldurulması zorunludur!")

    def delete_item(self):
        selected_indices = self.inventory_treeview.selection()
        if not selected_indices:
            messagebox.showerror("Hata", "Lütfen silinecek öğe/öğeleri seçiniz!")
            return

        # Seçilen indeksleri öğe numaralarına dönüştürme
        oge_nolar = [int(selected_index.lstrip('I')) for selected_index in selected_indices]

        # Dizin çakışmalarını önlemek için seçili öğeleri ters sırayla silme
        for oge_no in sorted(oge_nolar, reverse=True):
            self.selected_index = f'I{oge_no}'
            self.inventory_treeview.delete(self.selected_index)
            self.inventory_list.pop(oge_no)

        with open('inventory.csv', 'w', newline='', encoding="UTF-8") as file:
            writer = csv.writer(file)
            for item in self.inventory_list:
                writer.writerow(item)

        messagebox.showinfo("Başarılı", "Öğe/Öğeler başarıyla silindi.")

    # def search_item(self):
    #     search_query = self.entry_ara.get().strip().lower()
    #     self.inventory_treeview.delete(*self.inventory_treeview.get_children())  # Mevcut sonuçları temizle

    #     if not search_query:
    #         # Boş arama kutusu, tüm öğeleri göster
    #         self.reload_inventory()
    #     else:
    #         # Arama sorgusuyla sadece belirli sütunlarda eşleşen öğeleri göster
    #         for i, item_data in enumerate(self.inventory_list):
    #             product_description = item_data[0].strip().lower()
    #             serial_number = item_data[1].strip().lower()
    #             part_number = item_data[2].strip().lower()

    #             if search_query in product_description or search_query in serial_number or search_query in part_number:
    #                 item_index = f'I{i}'
    #                 self.inventory_treeview.insert('', 'end', values=item_data, iid=item_index)

    def search_item(self):
        search_query = self.entry_ara.get().strip().lower()
        company_filter = (
            self.check1_var.get(),
            self.check2_var.get(),
            self.check3_var.get()
        )

        self.inventory_treeview.delete(*self.inventory_treeview.get_children())  # Mevcut sonuçları temizle

        if not search_query:
            # Boş arama kutusu, sonuçları temizle
            self.reload_inventory()

        # Arama sorgusuyla sadece belirli sütunlarda ve seçilen şirketlere göre eşleşen öğeleri göster
        for i, item_data in enumerate(self.inventory_list):
            product_description = item_data[0].strip().lower()
            serial_number = item_data[1].strip().lower()
            part_number = item_data[2].strip().lower()
            company = item_data[4].strip().lower()

            # Kullanıcı tarafından seçilen filtrelere göre öğeleri kontrol et
            if (
                (
                    (self.check1_var.get() == 1 and "SDT" in company) or
                    (self.check2_var.get() == 1 and "TAMGÖR" in company) or
                    (self.check3_var.get() == 1 and "ORTAKLIK" in company)
                )
                and
                (search_query in product_description or
                search_query in serial_number or
                search_query in part_number)
            ):
                item_index = f'I{i}'
                self.inventory_treeview.insert('', 'end', values=item_data, iid=item_index)










    def exit_application(self):
        self.destroy()  # Arayüzü kapat

    def validate_integer_input(self, P):
        if P == "" or P.isdigit():
            return True
        else:
            return False

if __name__ == "__main__":
    app = App()
    app.mainloop()
