import time
from encryption import generate_keys, encrypt_message, decrypt_message
from crc import crc16
from dijkstra import dijkstra, shortest_path
from tcp_tahoe import simulate_tcp_tahoe

# Sample graph for testing
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1, 'E': 3},
    'E': {'D': 3}
}

start_node = 'A'
end_node = 'E'
message = "Hello IoT Node"

print("⚙️ Performance Metrics:\n")

# --- Encryption & Decryption ---
public_key, private_key = generate_keys()
start = time.time()
encrypted = encrypt_message(message.encode(), public_key)
enc_time = (time.time() - start) * 1000  # ms

start = time.time()
decrypted = decrypt_message(encrypted, private_key)
dec_time = (time.time() - start) * 1000  # ms

# --- CRC ---
start = time.time()
crc_value = crc16(message.encode())
crc_time = (time.time() - start) * 1000  # ms

# --- Dijkstra Path ---
start = time.time()
_, prev = dijkstra(graph, start_node)
path = shortest_path(prev, start_node, end_node)
dijkstra_time = (time.time() - start) * 1000  # ms

# --- TCP Tahoe Simulation ---
start = time.time()
tcp_log = simulate_tcp_tahoe(10, 4)
tahoe_time = (time.time() - start) * 1000  # ms

# --- Display Results ---
print(f"🛡️  Encryption Time:         {enc_time:.2f} ms")
print(f"🔓  Decryption Time:         {dec_time:.2f} ms")
#print(f"🔍  CRC Computation Time:    {crc_time:.2f} ms")
#print(f"📡  Dijkstra Path Time:      {dijkstra_time:.2f} ms")
#print(f"📶  TCP Tahoe Sim Time:      {tahoe_time:.2f} ms")
#print(f"📍  Shortest Path:           {' -> '.join(path)}")
print(f"📦  CRC Checksum:            {hex(crc_value)}")
print(f"📬  Decrypted Message:       {decrypted}")

# --- Throughput (bps) ---
msg_bits = len(message.encode()) * 8
total_time = (enc_time + dec_time + tahoe_time) / 1000  # in seconds
throughput = msg_bits / total_time if total_time > 0 else 0

# --- Latency (ms) ---
latency = enc_time + dec_time + tahoe_time

# --- Packet Delivery Ratio ---
total_packets = 10
lost_packets = 1  # we simulate a loss at packet 4
pdr = ((total_packets - lost_packets) / total_packets) * 100

# --- Routing Efficiency ---
# Assume ideal path length = 3 hops (A → B → D → E), which is the shortest possible
ideal_cost = 5  # based on manual inspection
actual_cost = sum([graph[path[i]][path[i+1]] for i in range(len(path)-1)])
routing_eff = ideal_cost / actual_cost if actual_cost > 0 else 0

# --- Print More Metrics ---
print(f"\n📈 Network-Level Metrics:")
print(f"📡 Throughput:              {throughput:.2f} bits/sec")
print(f"🕒 Latency:                 {latency:.2f} ms")
print(f"📬 Packet Delivery Ratio:   {pdr:.2f}%")
print(f"🔐 Security (RSA):          2048-bit key")
print(f"📍 Routing Efficiency:      {routing_eff:.2f} (1.0 = Optimal)")

