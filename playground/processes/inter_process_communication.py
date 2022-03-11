from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from multiprocessing import current_process, Process
from multiprocessing.connection import Listener, Client
from threading import get_ident
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


def _server_main(port: int) -> NoReturn:
    print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Running in SERVER mode on port {port}")
    listener_process = Process(target=_server_listener, args=(port,))
    try:
        listener_process.start()
        print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Listener running, press any key to stop.")
        input()  # Wait for any key
    except KeyboardInterrupt:
        pass
    finally:
        print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Stopping listener...")
        listener_process.terminate()
        listener_process.join()
    print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Stopped server.")
    exit()


def _server_listener(port: int) -> None:
    address = ('localhost', port)
    listener = Listener(address, authkey=b'secret password')
    while True:
        print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Listening for connections...")
        conn = listener.accept()
        print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Connection accepted from {listener.last_accepted}")
        try:
            while True:
                msg = conn.recv()
                print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Connection received '{msg}'")
        except EOFError:
            print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Closing connection (EOF).")
            conn.close()
    # print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Closing listener.")
    # listener.close()


def _client_main(port: int) -> NoReturn:
    print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Running in SERVER mode on port {port}")
    address = ('localhost', port)
    print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Connecting to server...")
    conn = Client(address, authkey=b'secret password')
    print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Connection established.")
    while True:
        message = input("Enter to send message (blank to exit): ")
        if not message:
            break
        print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Sending message '{message}'.")
        conn.send(message)
    print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Closing connection.")
    conn.close()
    print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Stopping client.")
    exit()


def _main() -> NoReturn:
    arguments = _parse_arguments()
    print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] {arguments}")
    if arguments.mode == _Mode.SERVER:
        _server_main(arguments.port)
    elif arguments.mode == _Mode.CLIENT:
        _client_main(arguments.port)
    else:
        raise ValueError(f"Unknown mode {arguments.mode}")


if __name__ == "__main__":
    _main()
