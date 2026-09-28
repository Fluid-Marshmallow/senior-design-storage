import RPi.GPIO as GPIO
import time

# -----------------------------
# Pin Configuration (BCM mode)
# -----------------------------
STEP_PIN = 20
DIR_PIN = 21

# -----------------------------
# Setup
# -----------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)

# -----------------------------
# User Settings
# -----------------------------
STEPS = 2000            # number of steps to move
DELAY = 0.0008          # delay between steps (seconds)
DIRECTION = True       # True = one direction, False = opposite

# -----------------------------
# Set direction
# -----------------------------
GPIO.output(DIR_PIN, GPIO.HIGH if DIRECTION else GPIO.LOW)

print("Starting stepper movement...")

try:
    for i in range(STEPS):
        # Rising edge
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(DELAY)

        # Falling edge
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(DELAY)

    print("Movement complete.")

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    GPIO.cleanup()
    print("GPIO cleaned up.")