# Python in Parallel

## Invoking Another Script (or command)

The `subprocess` module can be very helpful for quickly spinning up a subprocess to execute some program, whether 
python or something else.
As per [the documentation](https://docs.python.org/3/library/subprocess.html#using-the-subprocess-module), the
recommended usage is the `run` method where possible, falling back to `Popen` otherwise:

> The recommended approach to invoking subprocesses is to use the `run()` function for all use cases it can handle. 
> For more advanced use cases, the underlying `Popen` interface can be used directly.

The `invoke_another_argument.py` python script in this module can be run to see example usages of these two approaches:
```shell
python invoke_another_script.py
```
Result:
```text
--- Invoke fibonacci.py with a command line argument using subprocess.run()
> stdout = run(["python", "fibonacci.py", "25"], text=True, capture_output=True).stdout
stdout: 75025

--- Invoke fibonacci.py with an argument passed to stdin using subprocess.run()
> stdout = run(["python", "fibonacci.py"], input="25", text=True, capture_output=True).stdout
stdout: 75025

--- Invoke fibonacci.py with a command line argument using subprocess.Popen
> stdout, _ = Popen(["python", "fibonacci.py", "25"], text=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT).communicate()
stdout: 75025

--- Invoke fibonacci.py with an argument passed to stdin using subprocess.Popen
> stdout, _ = Popen(["python", "fibonacci.py"], text=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate(input="25")
stdout: 75025
```