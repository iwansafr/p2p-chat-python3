import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Fungsi untuk menangani penerimaan pesan
def receive_messages(sock, text_area):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, f"Peer: {message}\n")
                text_area.config(state=tk.DISABLED)
        except:
            break

# Fungsi untuk mengirim pesan
def send_message(sock, input_field, text_area):
    message = input_field.get()
    if message:
        sock.send(message.encode())
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, f"You: {message}\n")
        text_area.config(state=tk.DISABLED)
        input_field.delete(0, tk.END)

# Fungsi untuk membuat antarmuka
def create_gui(sock):
    window = tk.Tk()
    window.title("P2P Chat")

    # Area teks
    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state=tk.DISABLED, width=50, height=20)
    text_area.pack(padx=10, pady=10)

    # Input pesan
    input_frame = tk.Frame(window)
    input_frame.pack(padx=10, pady=5, fill=tk.X)
    input_field = tk.Entry(input_frame, width=40)
    input_field.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
    send_button = tk.Button(input_frame, text="Send", command=lambda: send_message(sock, input_field, text_area))
    send_button.pack(side=tk.RIGHT, padx=5, pady=5)

    # Thread untuk menerima pesan
    threading.Thread(target=receive_messages, args=(sock, text_area), daemon=True).start()

    window.mainloop()

# Fungsi utama untuk menghubungkan peer
def connect_peer(ip, port, is_server=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if is_server:
        sock.bind((ip, port))
        sock.listen(1)
        print(f"Listening on {ip}:{port}")
        conn, addr = sock.accept()
        print(f"Connected to {addr}")
        create_gui(conn)
    else:
        sock.connect((ip, port))
        print(f"Connected to {ip}:{port}")
        create_gui(sock)

# Menentukan apakah ini server atau client
role = input("Are you server or client? (s/c): ").lower()
if role == 's':
    connect_peer("0.0.0.0", 12345, is_server=True)
else:
    peer_ip = input("Enter peer IP: ")
    connect_peer(peer_ip, 12345)
