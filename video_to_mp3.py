import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy.editor import VideoFileClip
import os
import threading

class VideoToMP3Converter:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to MP3 Dönüştürücü")
        self.root.geometry("600x300")
        self.root.resizable(False, False)
        
        self.video_path = ""
        self.output_path = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Video Dosyası:", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.video_label = ttk.Label(main_frame, text="Henüz dosya seçilmedi", foreground="gray")
        self.video_label.grid(row=0, column=1, sticky=tk.W, padx=10)
        self.video_btn = ttk.Button(main_frame, text="Video Seç", command=self.select_video)
        self.video_btn.grid(row=0, column=2, padx=5)
        
        ttk.Label(main_frame, text="Kayıt Yeri:", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.output_label = ttk.Label(main_frame, text="Henüz konum seçilmedi", foreground="gray")
        self.output_label.grid(row=1, column=1, sticky=tk.W, padx=10)
        self.output_btn = ttk.Button(main_frame, text="Konum Seç", command=self.select_output)
        self.output_btn.grid(row=1, column=2, padx=5)
        
        self.start_btn = ttk.Button(main_frame, text="Başlat", command=self.start_conversion, state=tk.DISABLED)
        self.start_btn.grid(row=2, column=1, pady=20)
        
        self.progress = ttk.Progressbar(main_frame, length=400, mode='indeterminate')
        self.progress.grid(row=3, column=0, columnspan=3, pady=10)
        
        self.status_label = ttk.Label(main_frame, text="", font=('Arial', 9))
        self.status_label.grid(row=4, column=0, columnspan=3)
        
    def select_video(self):
        filetypes = (
            ('Video Dosyaları', '*.mp4 *.avi *.mkv *.mov *.flv *.wmv'),
            ('Tüm Dosyalar', '*.*')
        )
        filename = filedialog.askopenfilename(
            title='Video Dosyası Seç',
            filetypes=filetypes
        )
        if filename:
            self.video_path = filename
            self.video_label.config(text=os.path.basename(filename), foreground="black")
            self.check_ready()
            
    def select_output(self):
        filename = filedialog.asksaveasfilename(
            title='MP3 Dosyasını Kaydet',
            defaultextension='.mp3',
            filetypes=[('MP3 Dosyası', '*.mp3')]
        )
        if filename:
            self.output_path = filename
            self.output_label.config(text=os.path.basename(filename), foreground="black")
            self.check_ready()
            
    def check_ready(self):
        if self.video_path and self.output_path:
            self.start_btn.config(state=tk.NORMAL)
            
    def start_conversion(self):
        self.start_btn.config(state=tk.DISABLED)
        self.video_btn.config(state=tk.DISABLED)
        self.output_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.status_label.config(text="Dönüştürme işlemi devam ediyor...", foreground="blue")
        
        thread = threading.Thread(target=self.convert_video)
        thread.start()
        
    def convert_video(self):
        try:
            video = VideoFileClip(self.video_path)
            video.audio.write_audiofile(self.output_path, logger=None)
            video.close()
            
            self.root.after(0, self.conversion_success)
        except Exception as e:
            self.root.after(0, lambda: self.conversion_error(str(e)))
            
    def conversion_success(self):
        self.progress.stop()
        self.status_label.config(text="Dönüştürme başarıyla tamamlandı!", foreground="green")
        messagebox.showinfo("Başarılı", "Video MP3'e başarıyla dönüştürüldü!")
        self.reset_ui()
        
    def conversion_error(self, error_msg):
        self.progress.stop()
        self.status_label.config(text="Hata oluştu!", foreground="red")
        messagebox.showerror("Hata", f"Dönüştürme sırasında hata oluştu:\n{error_msg}")
        self.reset_ui()
        
    def reset_ui(self):
        self.start_btn.config(state=tk.DISABLED)
        self.video_btn.config(state=tk.NORMAL)
        self.output_btn.config(state=tk.NORMAL)
        self.video_path = ""
        self.output_path = ""
        self.video_label.config(text="Henüz dosya seçilmedi", foreground="gray")
        self.output_label.config(text="Henüz konum seçilmedi", foreground="gray")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToMP3Converter(root)
    root.mainloop()