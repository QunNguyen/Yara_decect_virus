import tkinter as tk
from tkinter import filedialog, messagebox
import os
import yara

# Định nghĩa các luật Yara
rules = yara.compile(filepath='APT_APT1.yar')

class MalwareDetectedDialog(tk.Toplevel):
    def __init__(self, parent, file_path, matches):
        super().__init__(parent)

        self.title("Malware Detected")
        self.geometry('400x200')

        msg = f"Malware found in {file_path}:\n"
        for match in matches:
            msg += f"- {match.rule}\n"

        label = tk.Label(self, text=msg)
        label.pack()

        delete_button = tk.Button(self, text="Delete File", command=lambda: self.delete_file(file_path))
        delete_button.pack()

    def delete_file(self, file_path):
        result = messagebox.askquestion("Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            os.remove(file_path)
            print("File deleted.")
        else:
            print("File not deleted.")

        self.destroy()


class MalwareScanner:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Malware Scanner")
        self.window.geometry('800x600')

        self.file_path_var = tk.StringVar()

        self.upload_entry = tk.Entry(self.window, textvariable=self.file_path_var, width=100)
        self.upload_entry.pack()

        self.upload_button = tk.Button(self.window, text="Upload File or Folder", command=self.upload)
        self.upload_button.pack()

        self.scan_button = tk.Button(self.window, text="Scan", command=self.scan, state=tk.DISABLED, bg='yellow', height=2, width=2)
        self.scan_button.pack()

        self.file_path = None

    def upload(self):
        self.file_path = filedialog.askopenfilename()
        if not self.file_path:
            self.file_path = filedialog.askdirectory()
        if self.file_path:
            self.file_path_var.set(self.file_path)
            self.scan_button.config(state=tk.NORMAL)

    def scan(self):
        if not self.file_path:
            return

        if os.path.isdir(self.file_path):
            for root, _, files in os.walk(self.file_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.check_file(file_path)
        else:
            self.check_file(self.file_path)

    def check_file(self, file_path):
        matches = rules.match(file_path)
        if not matches:
            MalwareDetectedDialog(self.window, file_path, matches)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = MalwareScanner()
    app.run()
