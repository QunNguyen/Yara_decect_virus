import tkinter as tk
from tkinter import filedialog, messagebox
import os
import yara
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import webbrowser
import subprocess
from collections import deque


# Định nghĩa các luật Yara
rules = yara.compile(filepath='rule_custom.yar')

class MalwareDetectedDialog(tk.Toplevel):
    def __init__(self, parent, file_path, matches):
        super().__init__(parent)

        self.title("Malware Detected")
        self.geometry('400x200')

        match_strings = [match.meta['description'] for match in matches]
        match_text = "\n".join(match_strings)

        msg = f"Malware found in {file_path}:\n{match_text}"

        label = tk.Label(self, text=msg, wraplength=350)  # Adjust wraplength as needed
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

class CuckooSubmissionDialog(tk.Toplevel):
    def __init__(self, parent, file_path):
        super().__init__(parent)

        self.title("File Submitted to Cuckoo")
        self.geometry('400x200')

        msg = f"File {file_path} has been submitted to Cuckoo Sandbox."

        label = tk.Label(self, text=msg, wraplength=350)
        label.pack()

        cuckoo_button = tk.Button(self, text="Go to Cuckoo", command=self.go_to_cuckoo)
        cuckoo_button.pack()

    def go_to_cuckoo(self):
        webbrowser.open('http://localhost:8000/analysis/pending/')



class MalwareScanner:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Malware Scanner")
        self.window.geometry('800x600')
        self.dialog_queue = deque()
        self.current_dialog = None

        title = tk.Label(self.window, text="Malware Scanner", font=("Helvetica", 24), pady=10)
        title.pack()

        self.file_path_var = tk.StringVar()

        self.upload_entry = tk.Entry(self.window, textvariable=self.file_path_var, width=50, font=("Helvetica", 12))
        self.upload_entry.pack()

        self.upload_button = tk.Button(self.window, text="Upload File or Folder", command=self.upload, bg="blue", fg="white", font=("Helvetica", 12), pady=5)
        self.upload_button.pack()

        self.scan_button = tk.Button(self.window, text="Scan", command=self.scan, state=tk.DISABLED, bg='yellow', height=2, width=10, font=("Helvetica", 12))
        self.scan_button.pack(pady=5)

        self.auto_scan_button = tk.Button(self.window, text="Auto Scan", command=self.auto_scan, state=tk.DISABLED, bg='green', fg='white', height=2, width=12, font=("Helvetica", 12))
        self.auto_scan_button.pack()

        self.observer = None

        self.file_path = None

        # Load Yara rules
        # self.rules = []
        self.rules = yara.compile(filepath='rule_custom.yar')

        # path_folder = 'rules_test'
        # for name in os.listdir(path_folder):
        #     for root, _, files in os.walk(f'{path_folder}/{name}'):
        #         for file in files:
        #             if file.endswith('.yar') or file.endswith('.yara'):
        #                 try:
        #                     file_path = os.path.join(root, file)
        #                     self.rules.append(yara.compile(filepath=file_path))
        #                 except:
        #                     print(f'Error: {file_path}')
                        # file_path = os.path.join(root, file)
                        # self.rules.append(yara.compile(filepath=file_path))

    
    
    def upload(self):
        choice = messagebox.askquestion("Upload", "Would you like to upload a file (Yes) or a directory (No)?", icon='question')
        if choice == 'yes':
            file_path = filedialog.askopenfilename()
        else:
            file_path = filedialog.askdirectory()

        if file_path:
            self.file_path = file_path
            self.file_path_var.set(file_path)
            self.scan_button.config(state=tk.NORMAL)
            self.auto_scan_button.config(state=tk.NORMAL)

    
    def scan(self):
        if self.scan_button.cget('text') == "Scan":
            self.scan_button.config(text='Stop Scan')
            if not self.file_path:
                return
            if os.path.isdir(self.file_path):
                for root, _, files in os.walk(self.file_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        self.check_file(file_path)
            else:
                self.check_file(self.file_path)
        else:
            self.scan_button.config(text='Scan')

    def auto_scan(self):
        if self.auto_scan_button.cget('text') == "Auto Scan":
            self.auto_scan_button.config(text='Stop Auto Scan')
            event_handler = AutoScanHandler(self)
            self.observer = Observer()
            self.observer.schedule(event_handler, self.file_path, recursive=True)
            self.observer.start()
        else:
            self.auto_scan_button.config(text='Auto Scan')
            self.observer.stop()
            self.observer.join()

    # def check_file(self, file_path):
    #     for rule in self.rules:
    #         matches = rule.match(file_path)
    #         if matches:
    #             MalwareDetectedDialog(self.window, file_path, matches)
    
    # def check_file(self, file_path):
    #     matches = rules.match(file_path)
    #     if matches:
    #         print("Malware found in", file_path)
    #         MalwareDetectedDialog(self.window, file_path, matches)
    #         self.submit_to_cuckoo(file_path)
    #     # else:
    #     #     print("No malware found in", file_path)
    #     #     self.submit_to_cuckoo(file_path)

    # def check_file(self, file_path):
    #     matches = rules.match(file_path)
    #     if matches:
    #         print("Malware found in", file_path)
    #         MalwareDetectedDialog(self.window, file_path, matches)
    #     else:
    #         print("No malware found in", file_path)
    #         self.submit_to_cuckoo(file_path)
    #         CuckooSubmissionDialog(self.window, file_path)

    def check_file(self, file_path):
        matches = rules.match(file_path)
        if matches:
            print("Malware found in", file_path)
            self.dialog_queue.append((MalwareDetectedDialog, (self.window, file_path, matches)))
        else:
            print("No malware found in", file_path)
            self.submit_to_cuckoo(file_path)
            self.dialog_queue.append((CuckooSubmissionDialog, (self.window, file_path)))

        if self.current_dialog is None or not self.current_dialog.winfo_exists():
            self.show_next_dialog()


    def show_next_dialog(self):
        if not self.dialog_queue:
            return

        DialogClass, args = self.dialog_queue.popleft()
        self.current_dialog = DialogClass(*args)

    # After 100ms, check if the dialog has been destroyed and if so, show the next one.
        self.window.after(100, self.check_dialog)

    def check_dialog(self):
        if self.current_dialog is None or not self.current_dialog.winfo_exists():
            self.current_dialog = None
            self.show_next_dialog()
        else:
            # Check again in 100ms.
            self.window.after(100, self.check_dialog)

    # def submit_to_cuckoo(self, file_path):
    #     with open(file_path, 'rb') as file:
    #         multipart_file = {'file': (os.path.basename(file_path), file)}
    #         response = requests.post('http://localhost:8000/submit/api/filetree', files=multipart_file)
    #         print("-----",response)
    #         # if response.ok:
    #         CuckooSubmissionDialog(self.window, file_path)
    

    def submit_to_cuckoo(self, file_path):
        try:
            cuckoo_path = "/home/anhnp/anaconda3/envs/sandbox/bin/cuckoo"  # Replace this with the actual path
            current_path = os.getcwd()
            file_path = file_path.replace(f'{current_path}/', '')
            os.system(f'{cuckoo_path} submit {file_path}')
            print(file_path)
            # subprocess.check_output([cuckoo_path, 'submit', file_path])
            # subprocess.run(f'{cuckoo_path} submit {file_path}', shell=True, check=True)

            print("File submitted successfully")
        except subprocess.CalledProcessError as e:
            print("Failed to submit file: ", e)


    def run(self):
        self.window.mainloop()

class AutoScanHandler(FileSystemEventHandler):
    def __init__(self, scanner):
        super().__init__()
        self.scanner = scanner

    def on_modified(self, event):
        if event.is_directory:
            for root, _, files in os.walk(event.src_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.scanner.check_file(file_path)
        else:
            self.scanner.check_file(event.src_path)
if __name__ == "__main__":
    app = MalwareScanner()
    app.run()
