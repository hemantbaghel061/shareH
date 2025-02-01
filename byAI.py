import os
import socket
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage, Label, Button, Entry, Toplevel

# Initialize main window
root = tk.Tk()
root.title("ShareH - File Transfer")
root.geometry("450x560+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False, False)

# Global filename variable
filename = ""

# Function to send files
def Send():
    window = Toplevel(root)
    window.title("Send")
    window.geometry('450x560+500+200')
    window.configure(bg="#f4fdfe")
    window.resizable(False, False)

    def select_file():
        global filename
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File", 
                                              filetypes=(("All Files", "*.*"), ("Text Files", "*.txt")))
        if filename:
            messagebox.showinfo("Selected File", f"File Selected: {os.path.basename(filename)}")

    def sender():
        if not filename:
            messagebox.showerror("Error", "Please select a file first!")
            return

        try:
            s = socket.socket()
            host = socket.gethostname()
            port = 8080
            s.bind((host, port))
            s.listen(1)
            messagebox.showinfo("Info", f"Waiting for connection... (Host: {host})")

            conn, addr = s.accept()
            with open(filename, "rb") as file:
                file_data = file.read()
                conn.sendall(file_data)

            messagebox.showinfo("Success", "File sent successfully!")
            s.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send file: {e}")

    # Icons and Layout
    send_icon = PhotoImage(file="send.png")
    window.iconphoto(False, send_icon)

    Label(window, text=f"Your ID: {socket.gethostname()}", bg='white', fg='black').place(x=140, y=290)
    
    Button(window, text="📂 Select File", width=15, font='arial 12 bold', bg="#fff", fg="#000", command=select_file).place(x=150, y=150)
    Button(window, text="📤 SEND", width=10, font='arial 12 bold', bg='#000', fg='#fff', command=sender).place(x=160, y=200)

    window.mainloop()

# Function to receive files
def Receive():
    window = Toplevel(root)
    window.title("Receive")
    window.geometry('450x560+500+200')
    window.configure(bg="#f4fdfe")
    window.resizable(False, False)

    def receiver():
        sender_id = sender_id_entry.get()
        file_name = file_name_entry.get()

        if not sender_id or not file_name:
            messagebox.showerror("Error", "Please enter both Sender ID and File Name")
            return

        try:
            s = socket.socket()
            port = 8080
            s.connect((sender_id, port))

            with open(file_name, "wb") as file:
                file_data = s.recv(1024 * 1024)  # Receive up to 1MB at a time
                file.write(file_data)

            messagebox.showinfo("Success", "File received successfully!")
            s.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to receive file: {e}")

    # Icons and Layout
    receive_icon = PhotoImage(file="receive.png")
    window.iconphoto(False, receive_icon)

    Label(window, text="Sender ID:", font=('arial', 12), bg='#f4fdfe').place(x=20, y=50)
    sender_id_entry = Entry(window, width=30, bg="white", font=("arial", 12))
    sender_id_entry.place(x=20, y=80)

    Label(window, text="Save File As:", font=('arial', 12), bg='#f4fdfe').place(x=20, y=130)
    file_name_entry = Entry(window, width=30, bg="white", font=("arial", 12))
    file_name_entry.place(x=20, y=160)

    Button(window, text="📥 Receive", font='arial 12 bold', bg="#39c790", fg="white", command=receiver).place(x=150, y=220)

    window.mainloop()

# Main Window Layout
Label(root, text="File Transfer by Hemant Baghel", font=('Arial', 16, 'bold'), bg='red', fg='white').pack(pady=20)

Button(root, text="📤 Send File", width=15, font='arial 12 bold', bg="blue", fg="white", command=Send).pack(pady=10)
Button(root, text="📥 Receive File", width=15, font='arial 12 bold', bg="green", fg="white", command=Receive).pack(pady=10)

root.mainloop()
