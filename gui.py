import tkinter as tk
from tkinter import ttk, messagebox

from dijkstra import dijkstra, shortest_path
from encryption import generate_keys, encrypt_message, decrypt_message
from crc import crc16
from tcp_tahoe import simulate_tcp_tahoe

# -----------------------------
# IoT Network Topology
# -----------------------------
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1, 'E': 3},
    'E': {'D': 3}
}

nodes = list(graph.keys())

# -----------------------------
# GUI Functions
# -----------------------------
def send_message():
    start_node = start_var.get()
    end_node = end_var.get()
    message = message_entry.get()

    if not start_node or not end_node or not message:
        messagebox.showerror("Input Error", "Please fill all fields.")
        return

    try:
        # Routing
        _, prev = dijkstra(graph, start_node)
        path = shortest_path(prev, start_node, end_node)

        # Encryption
        public_key, private_key = generate_keys()
        encrypted = encrypt_message(message.encode(), public_key)
        decrypted = decrypt_message(encrypted, private_key)

        # CRC
        checksum = crc16(message.encode())

        # TCP Tahoe Simulation (returns list of tuples)
        tcp_log = simulate_tcp_tahoe(8, 3)

        # Output
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Shortest Path: {' -> '.join(path)}\n")
        output_text.insert(tk.END, f"Encrypted: {encrypted.hex()}\n")
        output_text.insert(tk.END, f"Decrypted: {decrypted}\n")
        output_text.insert(tk.END, f"CRC Checksum: {hex(checksum)}\n\n")
        output_text.insert(tk.END, "TCP Tahoe Simulation:\n")
        for i, (cwnd, status) in enumerate(tcp_log, 1):
            output_text.insert(tk.END, f"Packet {i} | CWND: {cwnd} | Status: {status}\n")

    except Exception as e:
        messagebox.showerror("Processing Error", str(e))

# -----------------------------
# GUI Layout
# -----------------------------
window = tk.Tk()
window.title("Secure IoT Routing GUI")
window.geometry("600x550")
window.resizable(False, False)

tk.Label(window, text="Start Node:").place(x=30, y=30)
tk.Label(window, text="End Node:").place(x=30, y=70)
tk.Label(window, text="Message:").place(x=30, y=110)

start_var = tk.StringVar()
end_var = tk.StringVar()

ttk.Combobox(window, textvariable=start_var, values=nodes, state="readonly").place(x=120, y=30)
ttk.Combobox(window, textvariable=end_var, values=nodes, state="readonly").place(x=120, y=70)

message_entry = tk.Entry(window, width=40)
message_entry.place(x=120, y=110)

tk.Button(window, text="Send Secure Message", command=send_message).place(x=210, y=150)

output_text = tk.Text(window, wrap=tk.WORD, width=70, height=20)
output_text.place(x=30, y=200)

window.mainloop()
