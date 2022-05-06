from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from multiprocessing import current_process, Process
from multiprocessing.connection import Listener, Connection, Client
from threading import get_ident, Thread
from typing import NoReturn


class _Mode(Enum):
    SERVER = "server"
    CLIENT = "client"


@dataclass
class _Arguments:
    mode: _Mode
    port: int


def _main() -> NoReturn:
    arguments = _parse_arguments()
    if arguments.mode == _Mode.SERVER:
        _run_chat_server(arguments.port)
    elif arguments.mode == _Mode.CLIENT:
        _run_chat_client(arguments.port)
    else:
        raise ValueError(f"Unknown mode {arguments.mode}")


def _run_chat_server(port) -> NoReturn:
    _print(f"Running chat server on port {port}.")
    client_listener_process = Process(target=_client_listener, args=(port,))
    try:
        client_listener_process.start()
        _print("Client listener running, press any key to stop.")
        input()  # Wait for any key
    except KeyboardInterrupt:
        pass
    finally:
        _print("Stopping listener...")
        client_listener_process.terminate()
        client_listener_process.join()
    _print("Stopped server.")
    exit()


def _client_listener(port: int) -> None:
    address = ('localhost', port)
    listener = Listener(address, authkey=b'secret password')
    _print("Listening for clients...")
    chat_room_number: int = 0
    while True:
        chat_room_number += 1
        _print(f"Waiting for player 1...")
        p1_conn = listener.accept()
        _print(f"Player 1 connected from {listener.last_accepted}")
        _print(f"Waiting for player 2...")
        p2_conn = listener.accept()
        _print(f"Player 2 connected from {listener.last_accepted}")
        connection_thread = Thread(target=_client_handler, args=(p1_conn, p2_conn, chat_room_number))
        connection_thread.start()


def _client_handler(p1_conn: Connection, p2_conn: Connection, chat_room_number: int) -> None:
    try:
        p1_conn.send("Enter message: ")
        while True:
            msg = p1_conn.recv()
            _print(f"[Room {chat_room_number}] Forwarding from P1 to P2: '{msg}'")
            p2_conn.send(f"Player 1: '{msg}'\nEnter reply: ")
            msg = p2_conn.recv()
            _print(f"[Room {chat_room_number}] Forwarding from P2 to P1: '{msg}'")
            p1_conn.send(f"Player 2: '{msg}'\nEnter reply: ")
    except (EOFError, ConnectionResetError):
        _print(f"[Room {chat_room_number}] Closing connection (EOF).")
        p1_conn.close()
        p2_conn.close()


def _run_chat_client(port) -> NoReturn:
    _print("Running in SERVER mode on port {port}")
    address = ('localhost', port)
    _print("Connecting to server...")
    conn = Client(address, authkey=b'secret password')
    _print("Connection established.")
    try:
        while True:
            prompt = conn.recv()
            message = input(prompt)
            if not message:
                break
            conn.send(message)
        conn.close()
    except (ConnectionResetError, EOFError):
        _print("Other player closed the connection")
    except KeyboardInterrupt:
        pass
    finally:
        _print("Closing connection.")
        conn.close()
    exit()


def _print(msg: str) -> None:
    proc_thread_id = f"{current_process().ident}::{get_ident()}".ljust(13)
    print(f"~~> [{proc_thread_id} @ {datetime.utcnow()}] {msg}")


def _parse_arguments() -> _Arguments:
    parser = ArgumentParser(description="Inter-Process Communication Example")
    parser.add_argument("mode", choices=["server", "client"], help="Run in client or server mode")
    parser.add_argument("-p", "--port", type=int, default=31337, help="Port to communicate on.")
    args = parser.parse_args()

    return _Arguments(_Mode(args.mode), args.port)


if __name__ == "__main__":
    _main()
