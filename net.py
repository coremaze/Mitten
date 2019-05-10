def recv2(sock, size):
    buf = b''
    while len(buf) < size:
        buf += sock.recv(size - len(buf))
    return buf
