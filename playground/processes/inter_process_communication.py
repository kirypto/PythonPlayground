from argparse import ArgumentParser
from dataclasses import dataclass
from enum import Enum
from multiprocessing import current_process
from threading import get_ident
from datetime import datetime
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
    pass


def _client_main(port: int) -> NoReturn:
    print(f"~~> [{current_process().ident}::{get_ident()}@{datetime.utcnow()}] Running in SERVER mode on port {port}")
    pass


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
