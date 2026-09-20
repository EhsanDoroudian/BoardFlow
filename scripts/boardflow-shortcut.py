#!/usr/bin/env python3
import os
import socket
from pathlib import Path

SOCKET_PATH = Path(os.environ.get("XDG_RUNTIME_DIR", str(Path.home() / ".cache" / "boardflow"))) / "boardflow.show.sock"


def trigger():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect(str(SOCKET_PATH))
        sock.sendall(b"show")
    except OSError:
        raise SystemExit(0)
    finally:
        sock.close()


if __name__ == "__main__":
    trigger()
