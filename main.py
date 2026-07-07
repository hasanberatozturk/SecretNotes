from email import message

from cryptography.fernet import Fernet
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import base64

window = Tk()
window.title("Secret Notes")
window.minsize(400,700)
window.resizable(width=False, height=False)

# Encryption and Decode

def get_key(password):
    password = password.ljust(32)[:32]
    return base64.urlsafe_b64encode(password.encode())


def save_encrypt():

    title = message_entry.get().strip()
    message = message_text.get(1.0, END).strip()
    password = password_entry.get()

    if message == "" or password == "":
        messagebox.showerror("Error", "Lütfen bir mesaj ve şifre giriniz!")
    else:
        try:
            key = get_key(password)

            f = Fernet(key)
            encrypted_message = f.encrypt(message.encode()).decode()


            with open("encrypted_message.txt", "a") as file:
                file.write(f'{title}|{encrypted_message}\n')

            message_entry.delete(0, END)
            message_text.delete("1.0", END)
            password_entry.delete(0, END)

        except ValueError:
            messagebox.showerror("Error", "Bir hata oluştu")

def decode():
    password = password_entry.get()

    if password == "":
        messagebox.showerror("Error","Şifre kısmını boş bırakmayınız!")
    else:
        try:
            key = get_key(password)
            f = Fernet(key)
            found = False

            with open("encrypted_message.txt", "r") as file:
                for line in file:
                    line = line.strip()
                    if "|" in line:
                        parts = line.split("|")
                        title = parts[0]
                        encrypted_message = parts[1]
                        try :
                            decode_message = f.decrypt(encrypted_message.encode()).decode()
                            message_text.delete("1.0", END)
                            message_text.insert(1.0, decode_message)
                            password_entry.delete(0, END)
                            found = True
                            break
                        except:
                           continue
            if not found:
                messagebox.showwarning("Warning","Bu şifreye ait bir kayıt bulunamadı!")
        except ValueError:
            messagebox.showerror("Error","Şifre Hatalı!")



# UI
img = ImageTk.PhotoImage(Image.open("topsecret.png"))
img_label = Label(window, image=img)
img_label.image = img
img_label.pack(side="top", padx=20, pady=20)

message_title=Label(window, text="Mesaj Başlığı")
message_title.pack()
message_entry = Entry()
message_entry.pack(side="top", padx=10, pady=10)

message_title2 = Label(window, text="Mesaj İçeriği",)
message_title2.pack()
message_text = Text(window,width=50,height=15)
message_text.pack(side="top", padx=30, pady=10)

password_title = Label(window, text="Şifreyi girin")
password_title.pack()
password_entry = Entry(show="*")
password_entry.pack(side="top", padx=10, pady=10)

encryption_btn = Button(text="Kaydet ve Şifrele",fg="white",bg="red",command=save_encrypt)
encryption_btn.pack(side="top", padx=20, pady=10)

decode_btn = Button(text="Şifreyi Çöz",fg="black",bg="green",command=decode)
decode_btn.pack(side="top")


window.mainloop()
