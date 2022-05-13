"""
Example of inter-process communication.
- Message passing from a client process to a server process on a specified port.
- Multiple clients can connect to the server simultaneously, as each are handled on a separate thread.
- Server can be run by invoking `python inter_process_communication.py server`
- Clients can be run by invoking `python inter_process_communication.py client`
    - Once connected, client script will receive messages via stdin and forward to the server.
"""
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from multiprocessing import current_process, Process
from multiprocessing.connection import Listener, Client, Connection
from threading import get_ident, Thread
from typing import NoReturn


class _Mode(Enum):
    SERVER = "server"
    CLIENT = "client"


@dataclass
class _Arguments:
    mode: _Mode
    port: int


def _parse_arguments() -> _Arguments:
    parser = ArgumentParser(description="Inter-Process Communication Example")
    parser.add_argument("mode", choices=["server", "client"], help="Run in client or server mode")
    parser.add_argument("-p", "--port", type=int, default=31337, help="Port to communicate on.")
    args = parser.parse_args()

    return _Arguments(_Mode(args.mode), args.port)


def _print_prefixed(message: str) -> None:
    print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] {message}")


def _server_main(port: int) -> NoReturn:
    _print_prefixed(f"Running in SERVER mode on port {port}")
    listener_process = Process(target=_server_listener, args=(port,))
    try:
        listener_process.start()
        _print_prefixed("Listener running, press any key to stop.")
        input()  # Wait for any key
    except KeyboardInterrupt:
        pass
    finally:
        _print_prefixed("Stopping listener...")
        listener_process.terminate()
        listener_process.join()
    _print_prefixed("Stopped server.")
    exit()


def _server_listener(port: int) -> None:
    address = ("localhost", port)
    listener = Listener(address, authkey=b'secret password')
    while True:
        _print_prefixed("Listening for connections...")
        conn = listener.accept()
        _print_prefixed(f"Connection accepted from {listener.last_accepted}")
        connection_thread = Thread(target=_connection_handler, args=(conn,))
        connection_thread.start()


def _connection_handler(conn: Connection) -> None:
    try:
        while True:
            msg = conn.recv()
            _print_prefixed(f"Connection received '{msg}'")
    except EOFError:
        _print_prefixed("Closing connection (EOF).")
        conn.close()


def _client_main(port: int) -> NoReturn:
    _print_prefixed(f"Running in SERVER mode on port {port}")
    address = ('localhost', port)
    _print_prefixed(f"Connecting to server...")
    conn = Client(address, authkey=b'secret password')
    _print_prefixed(f"Connection established.")
    while True:
        message = input("Enter to send message (blank to exit): ")
        if not message:
            break
        _print_prefixed(f"Sending message '{message}'.")
        conn.send(message)
    _print_prefixed(f"Closing connection.")
    conn.close()
    _print_prefixed(f"Stopping client.")
    exit()


def _main() -> NoReturn:
    arguments = _parse_arguments()
    _print_prefixed(f"{arguments}")
    if arguments.mode == _Mode.SERVER:
        _server_main(arguments.port)
    elif arguments.mode == _Mode.CLIENT:
        _client_main(arguments.port)
    else:
        raise ValueError(f"Unknown mode {arguments.mode}")


if __name__ == "__main__":
    _main()
