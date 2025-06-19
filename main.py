from dijkstra import dijkstra, shortest_path
from encryption import generate_keys, encrypt_message, decrypt_message
from crc import crc16
from tcp_tahoe import simulate_tcp_tahoe

# ---- Network Graph Definition ----
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1, 'E': 3},
    'E': {'D': 3}
}

start = 'A'
end = 'E'

# ---- Dijkstra Routing ----
distances, predecessors = dijkstra(graph, start)
path = shortest_path(predecessors, start, end)

print(f"\Path from {start} to {end}: {path}")

# ---- Encryption + Decryption ----
message = "Hello IoT Node"
public_key, private_key = generate_keys()

encrypted = encrypt_message(message.encode(), public_key)
print("\nEncrypted Message:")
print(encrypted.hex())

decrypted = decrypt_message(encrypted, private_key)
print("\nDecrypted Message:")
print(decrypted.decode())

# ---- CRC ----
checksum = crc16(message.encode())
print(f"\nCRC Checksum: {hex(checksum)}")

# ---- TCP Tahoe Simulation ----
tcp_log = simulate_tcp_tahoe(8, 4)

print("\n--- Simulating TCP Tahoe Congestion Control ---\n")
print("TCP Tahoe Simulation:")
for i, (cwnd, status) in enumerate(tcp_log, 1):
    print(f"Packet {i} | CWND: {cwnd} | Status: {status}")

from network_visual import draw_topology
draw_topology(graph, path)

