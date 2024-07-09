import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import requests
import base64

def encrypt_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post('http://127.0.0.1:5001/encrypt', files=files)
        
        if response.status_code == 200:
            data = response.json()
            encrypted_file = data['encrypted_file']
            key = data['key']
            
            messagebox.showinfo("Success", f"File encrypted successfully!\nEncrypted file: {encrypted_file}\nKey: {key}")
        else:
            messagebox.showerror("Error", "Encryption failed!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def decrypt_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    key = simpledialog.askstring("Input", "Enter the key for decryption:")
    if not key:
        return

    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}
            data = {'key': key}
            response = requests.post('http://127.0.0.1:5002/decrypt', files=files, data=data)
        
        if response.status_code == 200:
            data = response.json()
            decrypted_file = data['decrypted_file']
            
            messagebox.showinfo("Success", f"File decrypted successfully!\nDecrypted file: {decrypted_file}")
        else:
            messagebox.showerror("Error", "Decryption failed!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Создание главного окна
root = tk.Tk()
root.title("File Encryptor/Decryptor")

# Создание кнопок
encrypt_button = tk.Button(root, text="Encrypt File", command=encrypt_file)
decrypt_button = tk.Button(root, text="Decrypt File", command=decrypt_file)

encrypt_button.pack(pady=20)
decrypt_button.pack(pady=20)

# Запуск главного цикла
root.mainloop()
