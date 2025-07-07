import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import matplotlib.pyplot as plt
from openpyxl import Workbook

# Fungsi bantu format Rupiah
def format_rupiah(amount):
    return f"Rp{int(amount):,}".replace(",", ".")

class LaptopStrategyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Strategi Produk Laptop - Rp Indonesia")

        self.upgrades = []
        self.original_upgrades = []
        self.best_upgrades = []
        self.preview_data = []
        self.preview_page = 0
        self.items_per_page = 20

        # ================= LAYOUT UTAMA =================
        main_frame = ttk.Frame(root, padding=10)
        main_frame.pack(fill="both", expand=True)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="y")

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True)

        # ================= FORM INPUT =================
        ttk.Label(left_frame, text="Nama Upgrade:").grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(left_frame, width=30)
        self.name_entry.grid(row=0, column=1)

        ttk.Label(left_frame, text="Biaya Produksi (Rp):").grid(row=1, column=0, sticky="w")
        self.cost_entry = ttk.Entry(left_frame)
        self.cost_entry.grid(row=1, column=1)

        ttk.Label(left_frame, text="Harga Jual Tambahan (Rp):").grid(row=2, column=0, sticky="w")
        self.price_entry = ttk.Entry(left_frame)
        self.price_entry.grid(row=2, column=1)

        ttk.Button(left_frame, text="➕ Tambah Upgrade", command=self.add_upgrade).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(left_frame, text="📂 Upload CSV", command=self.upload_csv).grid(row=4, column=0, columnspan=2, pady=5)

        # ================= FILTER =================
        filter_frame = ttk.LabelFrame(left_frame, text="Filter Data", padding=10)
        filter_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Label(filter_frame, text="CPU_class:").grid(row=0, column=0)
        self.cpu_filter = ttk.Entry(filter_frame, width=15)
        self.cpu_filter.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Tahun:").grid(row=1, column=0)
        self.year_filter = ttk.Entry(filter_frame, width=10)
        self.year_filter.grid(row=1, column=1, padx=5)

        ttk.Button(filter_frame, text="🔍 Terapkan Filter", command=self.apply_filter).grid(row=2, column=0, columnspan=2, pady=5)

        # ================= TOMBOL AKSI =================
        action_frame = ttk.Frame(left_frame)
        action_frame.grid(row=6, column=0, columnspan=2, pady=10)

        ttk.Button(action_frame, text="📊 Hitung Strategi", command=self.calculate_strategy).grid(row=0, column=0, padx=2, pady=2)
        ttk.Button(action_frame, text="❌ Hapus Strategi", command=self.clear_strategy_results).grid(row=0, column=1, padx=2, pady=2)
        ttk.Button(action_frame, text="💾 Export 2 Terbaik", command=self.export_csv).grid(row=1, column=0, padx=2, pady=2)
        ttk.Button(action_frame, text="📤 Export Semua", command=self.export_excel_all).grid(row=1, column=1, padx=2, pady=2)
        ttk.Button(action_frame, text="📈 Grafik Profit", command=self.show_profit_chart).grid(row=2, column=0, columnspan=2, pady=2)
1
        # ================= HASIL STRATEGI + SCROLL =================
        result_frame = ttk.Frame(right_frame)
        result_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.result_box = tk.Text(result_frame, height=30, width=80, wrap="none")
        self.result_box.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_box.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_box.config(yscrollcommand=scrollbar.set)

        # Navigasi Halaman CSV
        preview_frame = ttk.Frame(right_frame)
        preview_frame.pack(pady=5)
        ttk.Button(preview_frame, text="⬅ Prev", command=self.prev_page).pack(side="left", padx=5)
        ttk.Button(preview_frame, text="Next ➡", command=self.next_page).pack(side="left", padx=5)

    def add_upgrade(self):
        try:
            name = self.name_entry.get()
            cost = float(self.cost_entry.get())
            price = float(self.price_entry.get())
            gross = price - cost

            self.upgrades.append({
                "name": name,
                "cost": cost,
                "price": price,
                "gross_profit": gross
            })

            self.result_box.insert(tk.END, f"✔ {name} ditambahkan (Profit: {format_rupiah(gross)})\n")
            self.result_box.see(tk.END)
            self.name_entry.delete(0, tk.END)
            self.cost_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "Masukkan angka yang valid untuk biaya dan harga!")

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")], title="Pilih file CSV")
        if not file_path:
            return

        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                data = list(reader)

            if not data:
                raise ValueError("File kosong.")

            headers = data[0]
            rows = data[1:]
            self.preview_data = [headers] + rows
            self.preview_page = 0
            self.show_preview_page()

            cost_idx = 0  # default ke kolom pertama
            price_idx = headers.index("price") if "price" in headers else -1
            cpu_idx = headers.index("CPU_class") if "CPU_class" in headers else -1
            year_idx = headers.index("year") if "year" in headers else -1
            storage_idx = headers.index("Storage") if "Storage" in headers else -1

            if price_idx == -1:
                messagebox.showwarning("Kolom Tidak Ditemukan", "Kolom 'price' wajib ada dalam file.")
                return

            self.upgrades.clear()
            self.original_upgrades.clear()

            for row in rows:
                try:
                    memory_val = row[cost_idx] if cost_idx < len(row) else ""
                    storage_val = row[storage_idx] if storage_idx >= 0 and storage_idx < len(row) else ""
                    name = f"{memory_val}GB + {storage_val}"
                    cost = float(memory_val) * 100000
                    price = float(row[price_idx])
                    cpu = row[cpu_idx] if cpu_idx >= 0 else ""
                    year = row[year_idx] if year_idx >= 0 else ""
                    gross = price - cost
                    item = {
                        "name": name,
                        "cost": cost,
                        "price": price,
                        "gross_profit": gross,
                        "CPU_class": cpu,
                        "year": year
                    }
                    self.upgrades.append(item)
                    self.original_upgrades.append(item)
                except:
                    continue

            self.result_box.insert(tk.END, f"\n📊 Data berhasil diunggah dan diproses.\n")
            self.result_box.see(tk.END)

        except Exception as e:
            messagebox.showerror("Gagal Membaca CSV", f"Terjadi kesalahan: {e}")

    def apply_filter(self):
        cpu = self.cpu_filter.get().strip().lower()
        year = self.year_filter.get().strip()

        self.upgrades = [item for item in self.original_upgrades if
                         (cpu in item["CPU_class"].lower() if cpu else True) and
                         (year == item["year"] if year else True)]

        messagebox.showinfo("Filter Diterapkan", f"{len(self.upgrades)} item ditemukan.")
        self.clear_strategy_results()

    def show_preview_page(self):
        self.result_box.insert(tk.END, "\n📄 Pratinjau Data ({} - {}):\n".format(
            self.preview_page * self.items_per_page + 1,
            min((self.preview_page + 1) * self.items_per_page, len(self.preview_data) - 1)
        ))
        self.result_box.insert(tk.END, " | ".join(self.preview_data[0]) + "\n")
        self.result_box.insert(tk.END, "-" * 80 + "\n")
        for row in self.preview_data[1 + self.preview_page * self.items_per_page:1 + (self.preview_page + 1) * self.items_per_page]:
            self.result_box.insert(tk.END, " | ".join(row) + "\n")
        self.result_box.see(tk.END)

    def next_page(self):
        max_page = (len(self.preview_data) - 1) // self.items_per_page
        if self.preview_page < max_page:
            self.preview_page += 1
            self.result_box.insert(tk.END, "\n")
            self.show_preview_page()

    def prev_page(self):
        if self.preview_page > 0:
            self.preview_page -= 1
            self.result_box.insert(tk.END, "\n")
            self.show_preview_page()

    def calculate_strategy(self):
        if len(self.upgrades) < 2:
            messagebox.showwarning("Data Kurang", "Masukkan minimal 2 upgrade untuk menghitung strategi.")
            return

        sorted_upgrades = sorted(self.upgrades, key=lambda x: x["gross_profit"], reverse=True)
        self.best_upgrades = sorted_upgrades[:2]
        others = sorted_upgrades[2:]

        self.result_box.insert(tk.END, "\n📈 Strategi Produk Terbaik:\n")
        self.result_box.insert(tk.END, "Base Model: Laptop Standar\n\n")

        for i, u in enumerate(self.best_upgrades, 1):
            self.result_box.insert(tk.END, f"{i}. {u['name']}\n")
            self.result_box.insert(tk.END, f"   ➤ Biaya Produksi    : {format_rupiah(u['cost'])}\n")
            self.result_box.insert(tk.END, f"   ➤ Harga Tambahan    : {format_rupiah(u['price'])}\n")
            self.result_box.insert(tk.END, f"   ➤ Gross Profit      : {format_rupiah(u['gross_profit'])}\n\n")

        if others:
            self.result_box.insert(tk.END, "\n🚫 Upgrade Lain (Profit Lebih Rendah):\n")
            for u in others:
                self.result_box.insert(tk.END, f"✖ {u['name']} (Profit: {format_rupiah(u['gross_profit'])})\n")

        self.result_box.see(tk.END)

    def clear_strategy_results(self):
        self.best_upgrades.clear()
        self.result_box.insert(tk.END, "\n🧹 Hasil strategi dihapus.\n")
        self.result_box.see(tk.END)

    def export_csv(self):
        if not self.best_upgrades:
            messagebox.showinfo("Belum Dihitung", "Silakan hitung strategi dulu sebelum mengekspor.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")], title="Simpan 2 Strategi Terbaik")
        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Nama", "Biaya", "Harga", "Gross Profit"])
                for u in self.best_upgrades:
                    writer.writerow([u['name'], int(u['cost']), int(u['price']), int(u['gross_profit'])])
            messagebox.showinfo("Berhasil", f"2 upgrade terbaik disimpan ke:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Gagal Menyimpan", f"Terjadi kesalahan: {e}")

    def export_excel_all(self):
        if not self.upgrades:
            messagebox.showinfo("Kosong", "Belum ada data untuk diekspor.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")], title="Simpan Semua Data ke Excel")
        if not file_path:
            return

        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Strategi Laptop"

            ws.append(["Nama Upgrade", "Biaya Produksi", "Harga Tambahan", "Gross Profit"])

            for u in self.upgrades:
                ws.append([u['name'], int(u['cost']), int(u['price']), int(u['gross_profit'])])

            wb.save(file_path)
            messagebox.showinfo("Berhasil", f"Data lengkap disimpan ke Excel:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Gagal Simpan Excel", f"Error: {e}")

    def show_profit_chart(self):
        if not self.upgrades:
            messagebox.showinfo("Kosong", "Belum ada data untuk ditampilkan.")
            return

        sort_by_profit = sorted(self.upgrades, key=lambda x: x['gross_profit'], reverse=True)

        names = [u['name'] for u in sort_by_profit]
        profits = [u['gross_profit'] for u in sort_by_profit]

        plt.figure(figsize=(10, 6))
        plt.barh(names, profits, color='skyblue')
        plt.xlabel("Gross Profit (Rp)")
        plt.title("Grafik Gross Profit Seluruh Upgrade")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

# =============== JALANKAN GUI ===============
if __name__ == "__main__":
    root = tk.Tk()
    app = LaptopStrategyApp(root)
    root.mainloop()
