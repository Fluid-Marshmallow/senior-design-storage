import lgpio
import time

# Pin definitions
STEP_PIN = 18
DIR_PIN = 21

# Initialize GPIO once
h = lgpio.gpiochip_open(0)

lgpio.gpio_claim_output(h, STEP_PIN)
lgpio.gpio_claim_output(h, DIR_PIN)


def move_steps(steps, frequency, direction=1):
    """
    Move stepper motor a specific number of steps.

    Args:
        steps (int): Number of steps to move
        frequency (float): Steps per second (Hz)
        direction (int): 1 or 0 for direction
    """

    if steps <= 0 or frequency <= 0:
        raise ValueError("Steps and frequency must be positive")

    # Set direction
    lgpio.gpio_write(h, DIR_PIN, direction)

    # Calculate runtime
    run_time = steps / frequency

    # Start PWM (50% duty cycle)
    lgpio.tx_pwm(h, STEP_PIN, frequency, 50)

    # Wait for motion to complete
    time.sleep(run_time)

    # Stop PWM
    lgpio.tx_pwm(h, STEP_PIN, 0, 0)

    lgpio.gpio_write(h, STEP_PIN, 0)


# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    try:
        print("Move forward 200 steps")
        move_steps(steps=200, frequency=500, direction=1)

        time.sleep(1)

        print("Move backward 200 steps")
        move_steps(steps=200, frequency=500, direction=0)

    finally:
        lgpio.gpiochip_close(h)