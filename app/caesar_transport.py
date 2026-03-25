"""Цезарь mod 65536 + строка десятичных кодов для TCP (как в ноутбуке)."""
import socket

UNICODE_MOD = 65536  # как в ноутбуке: сдвиг по mod 65536
CAESAR_K = 1234
HOST = "127.0.0.1"
PORT = 9009


def _wrap(x: int) -> int:
    return x % UNICODE_MOD


def caesar_encrypt(k: int, m: str) -> str:
    return "".join(chr(_wrap(ord(c) + k)) for c in m)


def caesar_decrypt(k: int, c: str) -> str:
    return "".join(chr(_wrap(ord(c) - k)) for c in c)


def pack_text_as_decimal_codes(s: str) -> str:
    return " ".join(str(ord(c)) for c in s)


def unpack_decimal_codes_to_text(s: str) -> str:
    s = s.strip()
    if not s:
        return ""
    return "".join(chr(_wrap(int(x))) for x in s.split())


def encrypt_for_transport(plain: str, k: int = CAESAR_K) -> str:
    return pack_text_as_decimal_codes(caesar_encrypt(k, plain))


def decrypt_from_transport(packed: str, k: int = CAESAR_K) -> str:
    return caesar_decrypt(k, unpack_decimal_codes_to_text(packed))


def send_line(sock: socket.socket, line: str) -> None:
    sock.sendall((line + "\n").encode("utf-8"))


def recv_line(sock: socket.socket) -> str:
    buf = bytearray()
    while True:
        b = sock.recv(1)
        if not b:
            raise ConnectionError("соединение закрыто")
        if b == b"\n":
            break
        buf.extend(b)
    return buf.decode("utf-8")
