from argparse import ArgumentParser
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT
from typing import List


def _main() -> None:
    parser = ArgumentParser(description="Solves the Minecraft maze problem")
    parser.add_argument("input", help="name of the input file")
    parser.add_argument("--output", required=False, help="optional name of the output file")
    parser.add_argument("--pretty", required=False, action="store_true",
                        help="print the visual path as text. cannot be combined with '--output'")
    args = parser.parse_args()

    input_lines = Path(args.input).read_text("utf8")
    solver = Popen(['python', 'astar_solver.py'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    result = solver.communicate(input=input_lines.encode("utf8"))[0].decode("utf8")

    if args.output:
        expected_result = Path(args.output).read_text("utf8")
        is_correct = expected_result.splitlines() == result.splitlines()
        print("----- Input:")
        print(input_lines)
        print(f"----- Result {'(CORRECT)' if is_correct else '(INCORRECT)'}: ")
        print(result)
        if not is_correct:
            print("----- Expected:")
            print(expected_result)
            print("-----")
    elif args.pretty:
        print(result)
        print("----- Path: ('^' = start, '$' = end, '*' = path)")
        lines = input_lines.split()
        rows = int(lines[0])
        cols = int(lines[1])
        pretty_output: List[List[str]] = [[" " for _ in range(cols)] for _ in range(rows)]
        row, col = [int(char) for char in lines[-4:-2]]
        pretty_output[row][col] = "^"
        for move in result.splitlines():
            if move == "south":
                row += 1
            elif move == "north":
                row -= 1
            elif move == "east":
                col += 1
            elif move == "west":
                col -= 1
            else:
                break
            pretty_output[row][col] = "*"
        pretty_output[row][col] = "$"
        for pretty_row in pretty_output:
            print(" ".join(pretty_row))
    else:
        print("----- Result:")
        print(result)


if __name__ == "__main__":
    _main()
