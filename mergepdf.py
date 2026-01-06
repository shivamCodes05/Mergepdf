import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from pypdf import PdfReader, PdfWriter

pdf_files = []

def add_files(event=None):
    files = root.tk.splitlist(event.data)
    for file in files:
        if file.lower().endswith(".pdf") and file not in pdf_files:
            pdf_files.append(file)
            listbox.insert(tk.END, os.path.basename(file))

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        for file in os.listdir(folder):
            if file.lower().endswith(".pdf"):
                full_path = os.path.join(folder, file)
                if full_path not in pdf_files:
                    pdf_files.append(full_path)
                    listbox.insert(tk.END, file)

def merge_pdfs():
    if not pdf_files:
        messagebox.showerror("Error", "No PDFs added")
        return

    output = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not output:
        return

    password = password_entry.get().strip()

    writer = PdfWriter()

    try:
        for pdf in pdf_files:
            reader = PdfReader(pdf)
            if reader.is_encrypted:
                reader.decrypt("")
            for page in reader.pages:
                writer.add_page(page)

        if password:
            writer.encrypt(password)

        with open(output, "wb") as f:
            writer.write(f)

        messagebox.showinfo("Success", "PDFs merged successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_all():
    pdf_files.clear()
    listbox.delete(0, tk.END)

# ---------------- GUI ----------------

root = TkinterDnD.Tk()
root.title("PDF Merger – Drag & Drop | Batch | Password")
root.geometry("520x450")

tk.Label(root, text=" Drag & Drop PDF Files Below", font=("Arial", 12)).pack(pady=5)

listbox = tk.Listbox(root, width=60, height=10)
listbox.pack(pady=5)
listbox.drop_target_register(DND_FILES)
listbox.dnd_bind("<<Drop>>", add_files)

tk.Button(root, text=" Select Folder (Batch Merge)", command=select_folder).pack(pady=5)

tk.Label(root, text=" Output PDF Password (Optional)").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

tk.Button(root, text=" Merge PDFs", bg="green", fg="white", width=20, command=merge_pdfs).pack(pady=10)
tk.Button(root, text=" Clear All", command=clear_all).pack()

root.mainloop()
