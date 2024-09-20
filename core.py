import tkinter as tk
from tkinter import filedialog, messagebox
from functions import (
    vigenere_cipher, 
    playfair_cipher, 
    hill_cipher
)

class CipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cipher Tools")
        self.root.configure(bg='#2E2E2E')
        
        self.cipher_var = tk.StringVar(value="vigenere")
        self.mode_var = tk.StringVar(value="encrypt")
        
        frame = tk.Frame(root, bg='#2E2E2E')
        frame.pack(pady=20)

        tk.Label(frame, text="Select Cipher:", bg='#2E2E2E', fg='white').pack()
        tk.Radiobutton(frame, text="Vigenere", variable=self.cipher_var, value="vigenere", bg='#2E2E2E', fg='white', selectcolor='#2E2E2E').pack(anchor=tk.W)
        tk.Radiobutton(frame, text="Playfair", variable=self.cipher_var, value="playfair", bg='#2E2E2E', fg='white', selectcolor='#2E2E2E').pack(anchor=tk.W)
        tk.Radiobutton(frame, text="Hill", variable=self.cipher_var, value="hill", bg='#2E2E2E', fg='white', selectcolor='#2E2E2E').pack(anchor=tk.W)

        tk.Label(frame, text="Select Mode:", bg='#2E2E2E', fg='white').pack()
        tk.Radiobutton(frame, text="Encrypt", variable=self.mode_var, value="encrypt", bg='#2E2E2E', fg='white', selectcolor='#2E2E2E').pack(anchor=tk.W)
        tk.Radiobutton(frame, text="Decrypt", variable=self.mode_var, value="decrypt", bg='#2E2E2E', fg='white', selectcolor='#2E2E2E').pack(anchor=tk.W)

        self.input_text = tk.Text(frame, height=5, width=40, bg='#444444', fg='white', insertbackground='white', bd=1, relief=tk.SOLID)
        tk.Label(frame, text="Input Text:", bg='#2E2E2E', fg='white').pack()
        self.input_text.pack(pady=5)

        self.key_entry = tk.Entry(frame, width=40, bg='#444444', fg='white', insertbackground='white')
        tk.Label(frame, text="Key (Min 12 characters):", bg='#2E2E2E', fg='white').pack()
        self.key_entry.pack(pady=5)

        self.load_button = tk.Button(frame, text="Load .txt file", command=self.load_file, bg='#555555', fg='white')
        self.load_button.pack(pady=5)

        self.execute_button = tk.Button(frame, text="gasin", command=self.execute_cipher, bg='#555555', fg='white')
        self.execute_button.pack(pady=5)

        self.output_text = tk.Text(frame, height=5, width=40, bg='#444444', fg='white', insertbackground='white', bd=1, relief=tk.SOLID)
        tk.Label(frame, text="Output Text:", bg='#2E2E2E', fg='white').pack()
        self.output_text.pack(pady=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(tk.END, file.read())

    def execute_cipher(self):
        cipher_type = self.cipher_var.get()
        mode = self.mode_var.get()
        text = self.input_text.get(1.0, tk.END).strip()
        key = self.key_entry.get().strip()

        if len(key) < 12:
            messagebox.showerror("waduh!", "Password harus terdiri dari minimal 12 karakter!")
            return

        if cipher_type == "vigenere":
            result = vigenere_cipher(text, key, mode)
        elif cipher_type == "playfair":
            result = playfair_cipher(text, key, mode)
        elif cipher_type == "hill":
            key_matrix = [[3, 3], [2, 5]]
            result = hill_cipher(text, key_matrix, mode)
        
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = CipherApp(root)
    root.mainloop()