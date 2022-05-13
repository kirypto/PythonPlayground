"""
Fibonacci number calculator module.
- The 'fibonacci' function can be imported from this module and used directly.
- A positive integer can be provided as a command line argument.
- If no numeric argument is provided, a single numeric argument will be read from stdin.
- In both of the above 2 cases, the corresponding fibonacci number will be calculated and printed to stdout.
"""
from sys import argv


def fibonacci(fibonacci_number: int) -> int:
    if fibonacci_number <= 0:
        raise ValueError("Must provide an integer argument greater than 0.")
    last, curr = 1, 1
    index = 2
    while index < fibonacci_number:
        last, curr = curr, last + curr
        index += 1
    return curr


def _main():
    if len(argv) == 1:
        fib_num_raw = input()
    elif len(argv) == 2:
        fib_num_raw = argv[1]
    else:
        raise ValueError(f"Exactly 1 integer argument must be provided, but {len(argv) - 1} were.")
    if not fib_num_raw.isnumeric():
        raise ValueError(f"Must provide an integer argument, was {fib_num_raw}.")

    print(fibonacci(int(fib_num_raw)))


if __name__ == "__main__":
    _main()
