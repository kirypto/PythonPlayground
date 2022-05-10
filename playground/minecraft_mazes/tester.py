from argparse import ArgumentParser
from pathlib import Path
from subprocess import Popen, PIPE, STDOUT


def _main() -> None:
    parser = ArgumentParser(description="Solves the Minecraft maze problem")
    parser.add_argument("input", help="name of the input file")
    parser.add_argument("output", help="optional name of the output file")
    args = parser.parse_args()

    input_lines = Path(args.input).read_text("utf8")
    solver = Popen(['python', 'solver.py'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    result = solver.communicate(input=input_lines.encode("utf8"))[0].decode("utf8")

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


if __name__ == "__main__":
    _main()
