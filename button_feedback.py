import Jetson.GPIO as GPIO
import os
import time
import subprocess

# Set up the GPIO mode
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
trigger_pin = 18           # Pin number that will be connected to GND

# Set up the trigger pin as input with a pull-up resistor (reads HIGH by default)
GPIO.setup(trigger_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Flag to track if the command is running
command_running = False
process = None

try:
    print("Waiting for GPIO connection...")

    while True:
        # Check if the pins are connected (reads LOW when connected to GND)
        if GPIO.input(trigger_pin) == GPIO.LOW:
            if not command_running:
                print("Pins connected - starting command.")
                # Start the command as a subprocess
                process = subprocess.Popen(["echo", "Hello from NVIDIA Jetson!"], stdout=subprocess.PIPE)
                command_running = True
        else:
            if command_running:
                print("Pins disconnected - stopping command.")
                # Terminate the command
                process.terminate()
                process.wait()  # Ensure the process has terminated
                command_running = False

        # Short delay to debounce connection
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped manually")

finally:
    # Cleanup GPIO settings
    if process:
        process.terminate()  # Ensure the process is terminated on exit
    GPIO.cleanup()
