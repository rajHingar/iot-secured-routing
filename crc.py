def crc16(data: bytes, poly: int = 0x8408) -> int:
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if (crc & 0x0001):
                crc >>= 1
                crc ^= poly
            else:
                crc >>= 1
    return crc & 0xFFFF
