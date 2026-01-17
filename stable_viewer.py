import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class SDMetadataViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("SD AI Prompt Explorer & Gallery")
        self.root.geometry("1400x900")
        self.root.configure(bg="#1e1e1e")

        self.current_folder = ""
        self.current_prompt = ""
        self.all_data = [] # Lista di dizionari: {'path', 'filename', 'prompt', 'thumb'}
        self.thumbnails_refs = [] # Per il garbage collector

        # --- Layout ---
        
        # 1. Sidebar Sinistra
        self.sidebar = tk.Frame(self.root, width=320, bg="#2b2b2b")
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.btn_open = tk.Button(self.sidebar, text="📂 Seleziona Cartella", command=self.load_folder, 
                                 bg="#4e5154", fg="white", font=("Segoe UI", 9, "bold"))
        self.btn_open.pack(fill=tk.X, padx=10, pady=10)

        # BARRA DI RICERCA
        search_frame = tk.Frame(self.sidebar, bg="#2b2b2b")
        search_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        tk.Label(search_frame, text="🔍 Cerca nel prompt:", bg="#2b2b2b", fg="#aaa", font=("Segoe UI", 8)).pack(anchor="w")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_gallery)
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, bg="#1e1e1e", fg="white", insertbackground="white", borderwidth=0)
        self.search_entry.pack(fill=tk.X, ipady=3)

        # Galleria con Scrollbar
        self.canvas_container = tk.Frame(self.sidebar, bg="#2b2b2b")
        self.canvas_container.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.canvas_container, bg="#2b2b2b", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.canvas_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2b2b2b")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # 2. Area Centrale (Anteprima)
        self.preview_area = tk.Frame(self.root, bg="#181818")
        self.preview_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.img_label = tk.Label(self.preview_area, bg="#181818")
        self.img_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 3. Pannello Destra (Metadati)
        self.right_panel = tk.Frame(self.root, width=400, bg="#2b2b2b")
        self.right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.info_panel = tk.Text(self.right_panel, bg="#1e1e1e", fg="#a9b7c6", wrap=tk.WORD, 
                                 padx=15, pady=15, font=("Segoe UI", 10), borderwidth=0)
        self.info_panel.pack(fill=tk.BOTH, expand=True)
        self.btn_copy = tk.Button(self.right_panel, text="📋 Copia Prompt Positivo", command=self.copy_to_clipboard, 
                                 bg="#365880", fg="white", state=tk.DISABLED, pady=10, font=("Segoe UI", 9, "bold"))
        self.btn_copy.pack(fill=tk.X, padx=10, pady=10)

    def get_prompt_only(self, path):
        try:
            with Image.open(path) as img:
                return img.info.get("parameters", "").split("\n")[0].lower()
        except: return ""

    def load_folder(self):
        folder = filedialog.askdirectory()
        if not folder: return
        self.current_folder = folder
        self.all_data = []
        
        files = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])
        
        # Mostra un piccolo avviso se i file sono molti
        if len(files) > 50:
            messagebox.showinfo("Caricamento", f"Sto indicizzando {len(files)} immagini. Potrebbe volerci un istante...")

        for filename in files:
            path = os.path.join(folder, filename)
            prompt = self.get_prompt_only(path)
            
            # Crea miniatura
            try:
                img = Image.open(path)
                img.thumbnail((180, 180))
                thumb = ImageTk.PhotoImage(img)
                self.all_data.append({'path': path, 'filename': filename, 'prompt': prompt, 'thumb': thumb})
            except: continue
        
        self.filter_gallery()

    def filter_gallery(self, *args):
        query = self.search_var.get().lower()
        # Pulisce la galleria
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.thumbnails_refs = []

        for item in self.all_data:
            if query in item['prompt'] or query in item['filename'].lower():
                self.add_to_grid(item)

    def add_to_grid(self, item):
        frame = tk.Frame(self.scrollable_frame, bg="#2b2b2b", pady=10)
        frame.pack(fill=tk.X)
        
        btn = tk.Button(frame, image=item['thumb'], command=lambda p=item['path'], f=item['filename']: self.show_image(p, f),
                       bg="#2b2b2b", activebackground="#4b6eaf", borderwidth=0)
        btn.pack()
        self.thumbnails_refs.append(item['thumb'])

        short_name = (item['filename'][:25] + '..') if len(item['filename']) > 25 else item['filename']
        tk.Label(frame, text=short_name, bg="#2b2b2b", fg="#888888", font=("Segoe UI", 8)).pack()

    def show_image(self, path, filename):
        img = Image.open(path)
        w, h = self.preview_area.winfo_width(), self.preview_area.winfo_height()
        if w < 100: w, h = 800, 800
        img.thumbnail((w-40, h-40))
        photo = ImageTk.PhotoImage(img)
        self.img_label.config(image=photo)
        self.img_label.image = photo
        self.display_metadata(path, filename)

    def display_metadata(self, path, filename):
        self.current_prompt = ""
        try:
            with Image.open(path) as img:
                info = img.info
                text = f"FILE: {filename}\n" + "="*40 + "\n"
                if "parameters" in info:
                    params = info["parameters"]
                    parts = params.split("\n")
                    self.current_prompt = parts[0]
                    text += f"\nPROMPT POSITIVO:\n{self.current_prompt}\n"
                    for part in parts[1:]:
                        if "Negative prompt:" in part:
                            text += f"\nNEGATIVE PROMPT:\n{part.replace('Negative prompt: ', '')}\n"
                        elif "Steps:" in part:
                            text += f"\nDETTAGLI TECNICI:\n{part}"
                else: text += "\nNessun metadato trovato."

                self.info_panel.config(state=tk.NORMAL)
                self.info_panel.delete('1.0', tk.END)
                self.info_panel.insert(tk.END, text)
                self.info_panel.config(state=tk.DISABLED)
                self.btn_copy.config(state=tk.NORMAL if self.current_prompt else tk.DISABLED)
        except Exception as e: print(e)

    def copy_to_clipboard(self):
        if self.current_prompt:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.current_prompt)
            old_text = self.btn_copy["text"]
            self.btn_copy.config(text="✅ Copiato!", bg="#2d8a4e")
            self.root.after(1000, lambda: self.btn_copy.config(text=old_text, bg="#365880"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SDMetadataViewer(root)
    root.mainloop()
