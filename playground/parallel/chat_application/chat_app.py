from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from multiprocessing import current_process, Process
from multiprocessing.connection import Listener, Connection, Client
from random import shuffle
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
        _print(f"Waiting for chat client 1...")
        p1_conn = listener.accept()
        _print(f"Chat client 1 connected from {listener.last_accepted}")
        _print(f"Waiting for chat client 2...")
        p2_conn = listener.accept()
        _print(f"Chat client 2 connected from {listener.last_accepted}")
        connection_thread = Thread(target=_client_handler, args=(p1_conn, p2_conn, chat_room_number))
        connection_thread.start()


def _client_handler(conn_a: Connection, conn_b: Connection, chat_room_number: int) -> None:
    connections = [conn_a, conn_b]
    shuffle(connections)
    p1_conn, p2_conn = connections
    try:
        # Receive chat client names
        p1_name = p1_conn.recv()
        p2_name = p2_conn.recv()
        _print(f"[Room {chat_room_number}] Chat room spun up between P1 '{p1_name}' and P2 '{p2_name}'")
        # Send other chat client names
        p1_conn.send(p2_name)
        p2_conn.send(p1_name)
        # Send starting client name
        p1_conn.send(p1_name)
        p2_conn.send(p1_name)

        # Start main chat loop
        while True:
            msg = p1_conn.recv()
            _print(f"[Room {chat_room_number}] Forwarding from P1 to P2: '{msg}'")
            p2_conn.send(msg)
            msg = p2_conn.recv()
            _print(f"[Room {chat_room_number}] Forwarding from P2 to P1: '{msg}'")
            p1_conn.send(msg)
    except (EOFError, ConnectionResetError):
        _print(f"[Room {chat_room_number}] Closing connection (EOF).")
        p1_conn.close()
        p2_conn.close()


def _run_chat_client(port) -> NoReturn:
    print("-" * 50)
    name = _input_client_name("| ")
    address = ('localhost', port)
    conn = Client(address, authkey=b'secret password')
    print("| Connected to chat server.")
    print("| Waiting on another chat client...")

    try:
        # Send chat client name
        conn.send(name)
        # Receive other client name
        other_name = conn.recv()
        print(f"| Connected to '{other_name}'")
        # Receive starting client name
        starting_name = conn.recv()
        print(f"| Chat starts with {starting_name if starting_name != name else 'me'}")
        print("-" * 50)

        def prepend_names(sender: str, msg: str) -> str:
            return f"| {sender.rjust(max(len(other_name), 2))}: {msg}"

        if name == starting_name:
            message = input(prepend_names("Me", ""))
            conn.send(message)
        while True:
            message = conn.recv()
            print(prepend_names(other_name, message))
            message = input(prepend_names("Me", ""))
            if not message:
                break
            conn.send(message)
        conn.close()
    except (ConnectionResetError, EOFError):
        print("| Other client left chat.")
    except KeyboardInterrupt:
        pass
    finally:
        print("| Leaving chat.")
        conn.close()
    print("-" * 50)
    exit()


def _input_client_name(message_prefix: str = "") -> str:
    name = None
    while name is None:
        name = input(f"{message_prefix}Enter name (alphanumeric only): ")
        if not name.isalnum():
            name = None
            print(f"{message_prefix}    Error: name must be alpha numeric")
    return name


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
