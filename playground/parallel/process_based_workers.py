from datetime import datetime
from typing import Union
from multiprocessing import current_process, Process, Queue

from playground.parallel.fibonacci import fibonacci

WorkData = Union[int, str]
ResultData = str
_EXIT_FLAG = "__EXIT__"


# noinspection DuplicatedCode
def _main():
    work_queue: Queue[WorkData] = Queue()
    answer_queue: Queue[ResultData] = Queue()
    worker_process_count = int(input("How many worker processes? "))
    if worker_process_count <= 0:
        raise ValueError("Must have at least 1 worker process.")

    _print_prefixed("Spinning up worker and result processes...")
    worker_processes = [
        Process(target=_worker_process_main, args=(work_queue, answer_queue))
        for _ in range(worker_process_count)
    ]
    result_process = Process(target=_result_process_main, args=(answer_queue,))

    for worker_process in worker_processes:
        worker_process.start()
    result_process.start()
    _print_prefixed("Processes ready.")

    print("Enter numbers and press enter. Repeat as long as desired. Requests will be enqueued for asynchronous "
          "calculation. Answers will be printed once calculated. Enter 'exit' to quit.")
    try:
        while True:
            user_input = input()
            if user_input == "exit":
                break
            if not user_input.isnumeric() or int(user_input) <= 0:
                _print_prefixed(f"Skipping invalid input '{user_input}'")
                continue
            requested_number = int(user_input)
            work_queue.put_nowait(requested_number)
    except KeyboardInterrupt:
        pass

    _print_prefixed("Finishing outstanding calculations and stopping all processes...")
    for _ in range(worker_process_count):
        work_queue.put_nowait(_EXIT_FLAG)
    for worker_process in worker_processes:
        worker_process.join()
    answer_queue.put_nowait(_EXIT_FLAG)
    result_process.join()
    _print_prefixed("All processes re-joined, exiting.")


# noinspection DuplicatedCode
def _worker_process_main(work_queue: Queue, answer_queue: Queue) -> None:
    _print_prefixed("Worker process initialized.")
    while True:
        try:
            work = work_queue.get()
            if isinstance(work, str):
                if work == _EXIT_FLAG:
                    break
                else:
                    _print_prefixed(f"Unknown worker process command '{work}', skipping.")
                    continue
            desired_fibonacci_number = work
            _print_prefixed(f"Calculating Fibonacci({desired_fibonacci_number})...")
            start = datetime.now()
            result = fibonacci(desired_fibonacci_number)
            delta = datetime.now() - start
            _print_prefixed(f"Done in {delta.total_seconds()} seconds.")
            answer_queue.put_nowait(f"Fibonacci({desired_fibonacci_number}) is {result}")
        except ValueError as e:
            _print_prefixed(f"Failed! {e}")


def _result_process_main(answer_queue: Queue) -> None:
    _print_prefixed("Result process initialized.")
    while True:
        result = answer_queue.get()
        if result == _EXIT_FLAG:
            break
        truncated, remaining = result[:80], result[80:]
        output = truncated if not remaining else f"{truncated}... ({len(remaining)} more digits)"
        _print_prefixed(output)


def _print_prefixed(message: str) -> None:
    print(f"~~> [{current_process().ident} @ {datetime.utcnow()}] {message}")


if __name__ == "__main__":
    _main()
