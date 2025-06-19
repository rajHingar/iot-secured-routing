def simulate_tcp_tahoe(num_packets=8, loss_index=4):
    cwnd = 1
    ssthresh = 8
    log = []
    i = 0

    while i < num_packets:
        if i == loss_index:
            log.append((cwnd, "Lost (Timeout)"))
            ssthresh = cwnd // 2 if cwnd > 1 else 1
            cwnd = 1
        else:
            log.append((cwnd, "Sent"))
            if cwnd < ssthresh:
                cwnd *= 2  # Slow start
            else:
                cwnd += 1  # Congestion avoidance
        i += 1

    return log
