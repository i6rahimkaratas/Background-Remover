from rembg import remove
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading

class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arka Plan Kaldırıcı")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        self.input_path = None
        self.output_path = None
        
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(main_frame, text="Fotoğraf Arka Plan Kaldırıcı", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        input_frame = tk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(input_frame, text="Giriş Fotoğrafı:", font=("Arial", 10)).pack(anchor=tk.W)
        
        input_select_frame = tk.Frame(input_frame)
        input_select_frame.pack(fill=tk.X, pady=5)
        
        self.input_label = tk.Label(input_select_frame, text="Fotoğraf seçilmedi", 
                                     bg="#f0f0f0", anchor=tk.W, padx=10, pady=8)
        self.input_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.select_btn = tk.Button(input_select_frame, text="Fotoğraf Seç", 
                                     command=self.select_input, bg="#4CAF50", 
                                     fg="white", padx=20, pady=8, font=("Arial", 10))
        self.select_btn.pack(side=tk.RIGHT)
        
        output_frame = tk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(output_frame, text="Kayıt Konumu:", font=("Arial", 10)).pack(anchor=tk.W)
        
        output_select_frame = tk.Frame(output_frame)
        output_select_frame.pack(fill=tk.X, pady=5)
        
        self.output_label = tk.Label(output_select_frame, text="Otomatik belirlenecek", 
                                      bg="#f0f0f0", anchor=tk.W, padx=10, pady=8)
        self.output_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.output_btn = tk.Button(output_select_frame, text="Konum Seç", 
                                     command=self.select_output, bg="#2196F3", 
                                     fg="white", padx=20, pady=8, font=("Arial", 10))
        self.output_btn.pack(side=tk.RIGHT)
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=20)
        
        self.status_label = tk.Label(main_frame, text="Başlamak için fotoğraf seçin", 
                                     font=("Arial", 10), fg="#666")
        self.status_label.pack(pady=10)
        
        self.remove_btn = tk.Button(main_frame, text="Arka Planı Kaldır", 
                                     command=self.remove_background, 
                                     bg="#FF5722", fg="white", 
                                     font=("Arial", 12, "bold"), 
                                     padx=40, pady=12, state=tk.DISABLED)
        self.remove_btn.pack(pady=10)
    
    def select_input(self):
        file_path = filedialog.askopenfilename(
            title="Fotoğraf Seç",
            filetypes=[
                ("Resim Dosyaları", "*.jpg *.jpeg *.png *.bmp *.webp"),
                ("Tüm Dosyalar", "*.*")
            ]
        )
        
        if file_path:
            self.input_path = file_path
            filename = os.path.basename(file_path)
            self.input_label.config(text=filename)
            self.remove_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Hazır! Arka planı kaldırmak için butona tıklayın")
            
            if self.output_path is None:
                name, ext = os.path.splitext(file_path)
                self.output_path = f"{name}_no_bg.png"
                self.output_label.config(text=os.path.basename(self.output_path))
    
    def select_output(self):
        if self.input_path:
            default_name = os.path.splitext(os.path.basename(self.input_path))[0] + "_no_bg.png"
        else:
            default_name = "output_no_bg.png"
        
        file_path = filedialog.asksaveasfilename(
            title="Kayıt Konumu Seç",
            defaultextension=".png",
            initialfile=default_name,
            filetypes=[
                ("PNG Dosyası", "*.png"),
                ("Tüm Dosyalar", "*.*")
            ]
        )
        
        if file_path:
            self.output_path = file_path
            self.output_label.config(text=os.path.basename(file_path))
    
    def remove_background(self):
        if not self.input_path:
            messagebox.showerror("Hata", "Lütfen önce bir fotoğraf seçin!")
            return
        
        self.remove_btn.config(state=tk.DISABLED)
        self.select_btn.config(state=tk.DISABLED)
        self.output_btn.config(state=tk.DISABLED)
        self.progress.start(10)
        self.status_label.config(text="İşleniyor... Lütfen bekleyin", fg="#FF5722")
        
        thread = threading.Thread(target=self.process_image)
        thread.start()
    
    def process_image(self):
        try:
            with open(self.input_path, 'rb') as inp:
                input_data = inp.read()
            
            output_data = remove(input_data)
            
            with open(self.output_path, 'wb') as out:
                out.write(output_data)
            
            self.root.after(0, self.on_success)
            
        except Exception as e:
            self.root.after(0, lambda: self.on_error(str(e)))
    
    def on_success(self):
        self.progress.stop()
        self.status_label.config(text="✓ Başarılı! Arka plan kaldırıldı", fg="#4CAF50")
        self.remove_btn.config(state=tk.NORMAL)
        self.select_btn.config(state=tk.NORMAL)
        self.output_btn.config(state=tk.NORMAL)
        
        messagebox.showinfo("Başarılı", 
                           f"Arka plan başarıyla kaldırıldı!\n\nKaydedildi: {self.output_path}")
    
    def on_error(self, error_msg):
        self.progress.stop()
        self.status_label.config(text="✗ Hata oluştu", fg="#F44336")
        self.remove_btn.config(state=tk.NORMAL)
        self.select_btn.config(state=tk.NORMAL)
        self.output_btn.config(state=tk.NORMAL)
        
        messagebox.showerror("Hata", f"İşlem sırasında bir hata oluştu:\n\n{error_msg}")

def main():
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
