from typing import Collection

from numpy import linspace, sin, pi


def generate_periodic_data(
        start: float = 0, stop: float = 10, count: int = 50,
        period: float = 5, amplitude: float = 1
) -> Collection[float]:
    linearly_spaced_values = linspace(start, stop, count)
    sin_period = 2 * pi
    sin_inputs = linearly_spaced_values / period * sin_period
    return sin(sin_inputs) * amplitude


def _main():
    data = generate_periodic_data()
    for index, value in zip(linspace(0, 10, 50), data):
        print(f"{round(index, 2)}: {round(value, 3)}")


if __name__ == "__main__":
    _main()
