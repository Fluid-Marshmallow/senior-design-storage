
import RPi.GPIO as GPIO
import time

# GPIO pin setup (BCM numbering)
STEP_PIN = 19   # Physical pin 35
DIR_PIN = 26    # Physical pin 37

GPIO.setmode(GPIO.BCM)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)

# Initial direction
GPIO.output(DIR_PIN, GPIO.HIGH)

def step_motor(steps=1, delay=0.001):
    for _ in range(steps):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(delay)

try:
    print("Commands:")
    print("  step <number>  -> move motor")
    print("  dir            -> toggle direction")
    print("  quit           -> exit")

    direction = True

    while True:
        cmd = input(">> ").strip().lower()
        parts = cmd.split()

        if len(parts) > 0 and parts[0] == "step":
            if len(parts) == 2 and parts[1].isdigit():
                steps = int(parts[1])
                step_motor(steps)
                print(f"Moved {steps} steps")
            else:
                print("Usage: step <number>")

        elif cmd == "dir":
            direction = not direction
            GPIO.output(DIR_PIN, GPIO.HIGH if direction else GPIO.LOW)
            print(f"Direction set to {'HIGH' if direction else 'LOW'}")

        elif cmd == "quit":
            break

        else:
            print("Unknown command")

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()