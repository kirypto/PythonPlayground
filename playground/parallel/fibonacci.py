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
    if len(argv) != 2 or not argv[1].isnumeric():
        raise ValueError("Must provide exactly 1 integer argument.")
    fib_num = int(argv[1])
    print(fibonacci(fib_num))


if __name__ == "__main__":
    _main()
