import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

class ModernLinuxCenter:
    def __init__(self, root):
        self.root = root
        self.root.title("Linux Pro Tools & Store")
        self.root.geometry("900x650")
        self.root.configure(bg="#1a1a1a")

        # Stil Yapılandırması
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0)
        self.style.map("Treeview", background=[('selected', '#3498db')])

        # --- ANA DÜZEN ---
        # Yan Menü
        self.sidebar = tk.Frame(root, bg="#252526", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # İçerik Alanı
        self.content_frame = tk.Frame(root, bg="#1a1a1a")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_sidebar()
        self.show_home() # Varsayılan ekran

    def setup_sidebar(self):
        tk.Label(self.sidebar, text="MENÜ", font=("Arial", 12, "bold"), bg="#252526", fg="#888888").pack(pady=20)
        
        btn_opts = {"font": ("Arial", 10), "bg": "#252526", "fg": "white", "relief": "flat", "anchor": "w", "padx": 20}
        
        tk.Button(self.sidebar, text="🏠 Ana Sayfa", command=self.show_home, **btn_opts).pack(fill=tk.X, pady=5)
        tk.Button(self.sidebar, text="🛠️ Sistem Onarım", command=self.show_fixer, **btn_opts).pack(fill=tk.X, pady=5)
        tk.Button(self.sidebar, text="🛍️ Uygulama Mağazası", command=self.show_store, **btn_opts).pack(fill=tk.X, pady=5)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # --- EKRANLAR ---

    def show_home(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Linux Pro Yönetim Merkezi", font=("Arial", 22, "bold"), bg="#1a1a1a", fg="white").pack(pady=50)
        tk.Label(self.content_frame, text="Sisteminizi optimize etmek veya yeni uygulamalar kurmak için\nyan menüyü kullanın.", font=("Arial", 12), bg="#1a1a1a", fg="#aaaaaa").pack()

    def show_fixer(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Sistem Onarım Araçları", font=("Arial", 18, "bold"), bg="#1a1a1a", fg="#e67e22").pack(pady=20)
        
        btn_frame = tk.Frame(self.content_frame, bg="#1a1a1a")
        btn_frame.pack()

        actions = [
            ("Güncelle & Yükselt", "apt update && apt upgrade -y", "#3498db"),
            ("Bozuk Paketleri Düzelt", "apt install -f", "#e67e22"),
            ("Gereksizleri Temizle", "apt autoremove -y", "#27ae60"),
        ]

        for text, cmd, color in actions:
            tk.Button(btn_frame, text=text, bg=color, fg="white", width=25, height=2, command=lambda c=cmd: self.run_command(c)).pack(pady=10)

    def show_store(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Uygulama Mağazası", font=("Arial", 18, "bold"), bg="#1a1a1a", fg="#9b59b6").pack(pady=10)

        # Arama Alanı
        search_frame = tk.Frame(self.content_frame, bg="#1a1a1a")
        search_frame.pack(pady=10, fill=tk.X, padx=20)
        
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), bg="#2b2b2b", fg="white", insertbackground="white")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_apps()) # Enter tuşu ile arama

        tk.Button(search_frame, text="🔍 Ara", bg="#9b59b6", fg="white", command=self.search_apps).pack(side=tk.RIGHT, padx=5)

        # Liste Alanı
        self.tree = ttk.Treeview(self.content_frame, columns=("Uygulama Adı", "Açıklama"), show="headings")
        self.tree.heading("Uygulama Adı", text="Paket Adı")
        self.tree.heading("Açıklama", text="Açıklama")
        self.tree.column("Uygulama Adı", width=150)
        self.tree.column("Açıklama", width=450)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Button(self.content_frame, text="📥 Seçilen Uygulamayı Kur", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), height=2, command=self.install_selected).pack(pady=10, fill=tk.X, padx=20)

    # --- MANTIKSAL İŞLEMLER ---

    def search_apps(self):
        query = self.search_entry.get().strip()
        if not query:
            return

        # Eski sonuçları temizle
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            # apt-cache search komutunu çalıştır
            output = subprocess.check_output(f"apt-cache search {query}", shell=True, text=True)
            lines = output.strip().split('\n')

            if not lines or lines[0] == "":
                messagebox.showwarning("Sonuç Yok", f"'{query}' ile ilgili bir uygulama bulunamadı.\nLütfen tam veya doğru adını girin.")
                return

            for line in lines[:50]: # İlk 50 sonucu göster (hız için)
                if ' - ' in line:
                    name, desc = line.split(' - ', 1)
                    self.tree.insert("", tk.END, values=(name.strip(), desc.strip()))
        except:
            messagebox.showerror("Hata", "Arama sırasında bir hata oluştu.")

    def install_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Seçim Yapın", "Lütfen kurmak istediğiniz uygulamayı listeden seçin.")
            return

        app_name = self.tree.item(selected_item)['values'][0]
        confirm = messagebox.askyesno("Kurulum Onayı", f"{app_name} uygulamasını kurmak istediğinize emin misiniz?")
        if confirm:
            self.run_command(f"apt install {app_name} -y")

    def run_command(self, command):
        # Yeni bir pencerede logları göster
        log_win = tk.Toplevel(self.root)
        log_win.title("İşlem Yürütülüyor...")
        log_win.geometry("600x400")
        log_win.configure(bg="black")

        text_area = tk.Text(log_win, bg="black", fg="#00ff00", font=("Consolas", 10))
        text_area.pack(fill=tk.BOTH, expand=True)

        def work():
            full_cmd = f"pkexec {command}"
            process = subprocess.Popen(full_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                text_area.insert(tk.END, line)
                text_area.see(tk.END)
                log_win.update()
            process.wait()
            if process.returncode == 0:
                messagebox.showinfo("Başarılı", "İşlem başarıyla tamamlandı!")
            log_win.destroy()

        self.root.after(100, work)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernLinuxCenter(root)
    root.mainloop()
