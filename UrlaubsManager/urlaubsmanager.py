import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import threading
try:
    import paramiko
except ImportError:
    messagebox.showerror("Fehler", "Das paramiko Modul fehlt. Bitte installieren Sie es.")
    paramiko = None

DATA_FILE = "praxis_daten.json"
SFTP_FILE = "sftp_config.json"

DEFAULT_DATA = {
    "status": "auto",
    "von": "",
    "bis": "",
    "wiederDaAb": "",
    "bannerText": "Praxisurlaub",
    "vertretungen": [],
    "notdienst": {
        "titel": "Ärztlicher Bereitschaftsdienst",
        "hinweis": "Außerhalb unserer Sprechzeiten wenden Sie sich bitte an den ärztlichen Bereitschaftsdienst unter der bundesweit einheitlichen Rufnummer 116 117.",
        "telefon": "116 117"
    }
}

DEFAULT_SFTP = {
    "host": "ssh.strato.de",
    "port": 22,
    "user": "hautarzt-dr-rahemipour.de",
    "password": "",
    "path": "/neu/urlaub-config.js"
}

def load_json(filepath, default_data):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for k, v in default_data.items():
                    if k not in data:
                        data[k] = v
                return data
        except:
            return default_data.copy()
    return default_data.copy()

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def generate_js(data):
    js = "/**\n * Automatisch generiert vom UrlaubsManager\n */\n\n"
    js += "const urlaubConfig = " + json.dumps(data, indent=4, ensure_ascii=False) + ";\n"
    return js

class VertretungDialog(tk.Toplevel):
    def __init__(self, parent, vertretung=None):
        super().__init__(parent)
        self.title("Vertretung bearbeiten" if vertretung else "Neue Vertretung")
        self.geometry("450x350")
        self.result = None
        
        self.entries = {}
        fields = [
            ("name", "Name der Praxis/Arzt"),
            ("fach", "Fachrichtung (optional)"),
            ("adresse", "Adresse"),
            ("telefon", "Telefon (Anzeige, z.B. 09131 12345)"),
            ("telefonLink", "Telefon für Klick (z.B. +49913112345)"),
            ("hinweis", "Hinweis (optional)")
        ]
        
        row = 0
        for key, label in fields:
            ttk.Label(self, text=label).grid(row=row, column=0, padx=10, pady=5, sticky="e")
            ent = ttk.Entry(self, width=30)
            ent.grid(row=row, column=1, padx=10, pady=5, sticky="we")
            if vertretung and key in vertretung:
                ent.insert(0, vertretung[key])
            self.entries[key] = ent
            row += 1
            
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Speichern", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Abbrechen", command=self.destroy).pack(side=tk.LEFT, padx=5)
        
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)
        
    def save(self):
        self.result = {k: v.get() for k, v in self.entries.items()}
        self.destroy()

class UrlaubsManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hautarztpraxis Erlangen - UrlaubsManager")
        self.geometry("600x550")
        
        style = ttk.Style(self)
        style.theme_use('clam')
        
        self.data = load_json(DATA_FILE, DEFAULT_DATA)
        self.sftp_config = load_json(SFTP_FILE, DEFAULT_SFTP)
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.create_tab_allgemein()
        self.create_tab_vertretungen()
        self.create_tab_notdienst()
        self.create_tab_sftp()
        
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.btn_upload = ttk.Button(btn_frame, text="Speichern & Hochladen", command=self.upload_thread)
        self.btn_upload.pack(side=tk.RIGHT, ipadx=10, ipady=5)
        
    def create_tab_allgemein(self):
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Allgemein")
        
        ttk.Label(frame, text="Status (Wichtig!):").grid(row=0, column=0, sticky="e", pady=5)
        self.var_status = tk.StringVar(value=self.data.get("status", "auto"))
        cb_status = ttk.Combobox(frame, textvariable=self.var_status, values=["auto", "an", "aus"], state="readonly", width=15)
        cb_status.grid(row=0, column=1, sticky="w", pady=5)
        ttk.Label(frame, text="(auto = nach Datum, an = immer an, aus = immer aus)").grid(row=0, column=2, padx=5, sticky="w")
        
        ttk.Label(frame, text="Von (JJJJ-MM-TT):").grid(row=1, column=0, sticky="e", pady=5)
        self.var_von = tk.StringVar(value=self.data.get("von", ""))
        ttk.Entry(frame, textvariable=self.var_von, width=15).grid(row=1, column=1, sticky="w", pady=5)
        
        ttk.Label(frame, text="Bis (JJJJ-MM-TT):").grid(row=2, column=0, sticky="e", pady=5)
        self.var_bis = tk.StringVar(value=self.data.get("bis", ""))
        ttk.Entry(frame, textvariable=self.var_bis, width=15).grid(row=2, column=1, sticky="w", pady=5)
        
        ttk.Label(frame, text="Wieder da ab:").grid(row=3, column=0, sticky="e", pady=5)
        self.var_wieder = tk.StringVar(value=self.data.get("wiederDaAb", ""))
        ttk.Entry(frame, textvariable=self.var_wieder, width=40).grid(row=3, column=1, columnspan=2, sticky="w", pady=5)
        
        ttk.Label(frame, text="Banner-Text (oben):").grid(row=4, column=0, sticky="e", pady=15)
        self.var_banner = tk.StringVar(value=self.data.get("bannerText", ""))
        ttk.Entry(frame, textvariable=self.var_banner, width=40).grid(row=4, column=1, columnspan=2, sticky="w", pady=15)
        
    def create_tab_vertretungen(self):
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Vertretungen")
        
        self.listbox = tk.Listbox(frame, height=10)
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.update_vertretungen_list()
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Hinzufügen", command=self.add_vertretung).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Bearbeiten", command=self.edit_vertretung).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Löschen", command=self.delete_vertretung).pack(side=tk.LEFT, padx=5)

    def update_vertretungen_list(self):
        self.listbox.delete(0, tk.END)
        for v in self.data.get("vertretungen", []):
            self.listbox.insert(tk.END, f"{v.get('name', 'Unbekannt')} - {v.get('adresse', '')}")
            
    def add_vertretung(self):
        d = VertretungDialog(self)
        if d.result:
            self.data.setdefault("vertretungen", []).append(d.result)
            self.update_vertretungen_list()
            
    def edit_vertretung(self):
        sel = self.listbox.curselection()
        if not sel: return
        idx = sel[0]
        d = VertretungDialog(self, self.data["vertretungen"][idx])
        if d.result:
            self.data["vertretungen"][idx] = d.result
            self.update_vertretungen_list()

    def delete_vertretung(self):
        sel = self.listbox.curselection()
        if not sel: return
        idx = sel[0]
        if messagebox.askyesno("Löschen", "Vertretung wirklich löschen?"):
            del self.data["vertretungen"][idx]
            self.update_vertretungen_list()
            
    def create_tab_notdienst(self):
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Notdienst")
        
        nd = self.data.get("notdienst", {})
        
        ttk.Label(frame, text="Titel:").grid(row=0, column=0, sticky="e", pady=5)
        self.var_nd_titel = tk.StringVar(value=nd.get("titel", ""))
        ttk.Entry(frame, textvariable=self.var_nd_titel, width=40).grid(row=0, column=1, sticky="w", pady=5)
        
        ttk.Label(frame, text="Telefon:").grid(row=1, column=0, sticky="e", pady=5)
        self.var_nd_tel = tk.StringVar(value=nd.get("telefon", ""))
        ttk.Entry(frame, textvariable=self.var_nd_tel, width=20).grid(row=1, column=1, sticky="w", pady=5)
        
        ttk.Label(frame, text="Hinweistext:").grid(row=2, column=0, sticky="e", pady=5)
        self.txt_nd_hinweis = tk.Text(frame, height=5, width=40)
        self.txt_nd_hinweis.grid(row=2, column=1, sticky="w", pady=5)
        self.txt_nd_hinweis.insert(tk.END, nd.get("hinweis", ""))
        
    def create_tab_sftp(self):
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Server-Verbindung")
        
        ttk.Label(frame, text="Server (Host):").grid(row=1, column=0, sticky="e", pady=5)
        self.var_sftp_host = tk.StringVar(value=self.sftp_config.get("host", ""))
        ttk.Entry(frame, textvariable=self.var_sftp_host, width=30).grid(row=1, column=1, sticky="w", pady=5)
        
        ttk.Label(frame, text="Benutzername:").grid(row=2, column=0, sticky="e", pady=5)
        self.var_sftp_user = tk.StringVar(value=self.sftp_config.get("user", ""))
        ttk.Entry(frame, textvariable=self.var_sftp_user, width=30).grid(row=2, column=1, sticky="w", pady=5)
        
        ttk.Label(frame, text="Passwort:").grid(row=3, column=0, sticky="e", pady=5)
        self.var_sftp_pass = tk.StringVar(value=self.sftp_config.get("password", ""))
        ttk.Entry(frame, textvariable=self.var_sftp_pass, show="*", width=30).grid(row=3, column=1, sticky="w", pady=5)
        
        ttk.Label(frame, text="Port:").grid(row=4, column=0, sticky="e", pady=5)
        self.var_sftp_port = tk.StringVar(value=str(self.sftp_config.get("port", 22)))
        ttk.Entry(frame, textvariable=self.var_sftp_port, width=10).grid(row=4, column=1, sticky="w", pady=5)
        
        ttk.Label(frame, text="Ziel-Pfad:").grid(row=5, column=0, sticky="e", pady=5)
        self.var_sftp_path = tk.StringVar(value=self.sftp_config.get("path", "/neu/urlaub-config.js"))
        ttk.Entry(frame, textvariable=self.var_sftp_path, width=30).grid(row=5, column=1, sticky="w", pady=5)
        
    def save_current_state(self):
        self.data["status"] = self.var_status.get()
        self.data["von"] = self.var_von.get()
        self.data["bis"] = self.var_bis.get()
        self.data["wiederDaAb"] = self.var_wieder.get()
        self.data["bannerText"] = self.var_banner.get()
        
        self.data["notdienst"] = {
            "titel": self.var_nd_titel.get(),
            "telefon": self.var_nd_tel.get(),
            "hinweis": self.txt_nd_hinweis.get("1.0", tk.END).strip()
        }
        
        save_json(DATA_FILE, self.data)
        
        self.sftp_config["host"] = self.var_sftp_host.get()
        self.sftp_config["user"] = self.var_sftp_user.get()
        self.sftp_config["password"] = self.var_sftp_pass.get()
        try:
            self.sftp_config["port"] = int(self.var_sftp_port.get())
        except:
            self.sftp_config["port"] = 22
        self.sftp_config["path"] = self.var_sftp_path.get()
        
        save_json(SFTP_FILE, self.sftp_config)

    def upload_thread(self):
        if not paramiko:
            messagebox.showerror("Fehler", "Paramiko fehlt. Hochladen nicht möglich.")
            return
            
        self.save_current_state()
        js_content = generate_js(self.data)
        
        with open("urlaub-config.js", "w", encoding="utf-8") as f:
            f.write(js_content)
            
        self.btn_upload.config(state=tk.DISABLED, text="Lade hoch...")
        
        def task():
            try:
                transport = paramiko.Transport((self.sftp_config["host"], self.sftp_config["port"]))
                transport.connect(username=self.sftp_config["user"], password=self.sftp_config["password"])
                sftp = paramiko.SFTPClient.from_transport(transport)
                
                sftp.put("urlaub-config.js", self.sftp_config["path"])
                sftp.close()
                transport.close()
                
                self.after(0, lambda: messagebox.showinfo("Erfolg", "Erfolgreich gespeichert und hochgeladen!"))
            except Exception as e:
                self.after(0, lambda e=e: messagebox.showerror("Upload Fehler", f"Fehler:\n{str(e)}"))
            finally:
                self.after(0, lambda: self.btn_upload.config(state=tk.NORMAL, text="Speichern & Hochladen"))
                
        threading.Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    app = UrlaubsManagerApp()
    app.mainloop()
