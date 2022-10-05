"""
Sample program for making an LED blink once per second.

Hardware:
- Pi
- LED
- 100 ohm resistor

GPIO setup:
- Connect GPIO pin #8 to resistor
- Connect other side of resistor to LED
- Connect other side of LED to a ground GPIO pin
Visually:  GPIO pin #8  -->  Resistor  -->  LED  -->  GPIO ground pin

Run this script, cancel with ctrl+c
"""

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)
try:
    while True:
        print("+", end="", flush=True)  # Print '+' signifying light should be off
        GPIO.output(8, GPIO.HIGH)  # Turn on
        sleep(1)

        print("-", end="", flush=True)  # Print '-' signifying light should be off
        GPIO.output(8, GPIO.LOW)  # Turn off
        sleep(1)
except KeyboardInterrupt:
    GPIO.output(8, GPIO.LOW)
finally:
    print("")  # Print newline so next prompt is not on same line as prints above
    GPIO.cleanup()  # Reset all GPIO changes made by this script
