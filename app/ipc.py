import socket

from app.paths import SHOW_SOCKET


def request_show():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect(str(SHOW_SOCKET))
        sock.sendall(b"show")
    finally:
        sock.close()
