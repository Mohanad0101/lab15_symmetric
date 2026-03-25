#!/usr/bin/env python3
"""Один клиент за запуск: приём строки, ответ «ОТВЕТ: …» тем же шифром."""
import socket

from caesar_transport import (
    CAESAR_K,
    HOST,
    PORT,
    decrypt_from_transport,
    encrypt_for_transport,
    recv_line,
    send_line,
)

# При необходимости поменяйте здесь:
HOST_BIND = HOST
PORT_BIND = PORT
KEY = CAESAR_K


def main() -> None:
    print(f"Сервер: {HOST_BIND}:{PORT_BIND}, ключ k={KEY}")
    print("Ожидание одного подключения…")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST_BIND, PORT_BIND))
    server.listen(1)

    conn, addr = server.accept()
    server.close()

    print("Клиент:", addr)

    packed = recv_line(conn)
    print("Строка из сокета (начало):", packed[:80] + ("…" if len(packed) > 80 else ""))

    msg = decrypt_from_transport(packed, KEY)
    print("Расшифровано:", msg)

    reply = "ОТВЕТ: " + msg
    send_line(conn, encrypt_for_transport(reply, KEY))
    conn.close()
    print("Ответ отправлен, сервер завершён.")


if __name__ == "__main__":
    main()
