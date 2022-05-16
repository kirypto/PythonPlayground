"""
Simple example of invoking another script or command via the subprocess module. Four ways are demonstrated:
- Invoking a script with a command line argument using submodule.run()
- Invoking a script with an argument passed to stdin using submodule.run()
- Invoking a script with a command line argument using Popen
- Invoking a script with an argument passed to stdin using Popen
"""
from subprocess import run, PIPE, STDOUT, Popen


def _main():
    print("--- Invoke fibonacci.py with a command line argument using submodule.run()")
    print('> stdout = run(["python", "fibonacci.py", "25"], text=True, capture_output=True).stdout')
    stdout = run(["python", "fibonacci.py", "25"], text=True, capture_output=True).stdout
    print(f"stdout: {stdout}")

    print("--- Invoke fibonacci.py with an argument passed to stdin using submodule.run()")
    print('> stdout = run(["python", "fibonacci.py"], input="25", text=True, capture_output=True).stdout')
    stdout = run(["python", "fibonacci.py"], input="25", text=True, capture_output=True).stdout
    print(f"stdout: {stdout}")

    print("--- Invoke fibonacci.py with a command line argument using Popen")
    print('> stdout, _ = Popen(["python", "fibonacci.py", "25"], text=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT).communicate()')
    stdout, _ = Popen(["python", "fibonacci.py", "25"], text=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT).communicate()
    print(f"stdout: {stdout}")

    print("--- Invoke fibonacci.py with an argument passed to stdin using Popen")
    print('> stdout, _ = Popen(["python", "fibonacci.py"], text=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate(input="25")')
    stdout, _ = Popen(["python", "fibonacci.py"], text=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate(input="25")
    print(f"stdout: {stdout}")


if __name__ == "__main__":
    _main()
