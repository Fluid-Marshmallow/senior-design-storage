import RPi.GPIO as GPIO
import time
import serial
import struct
import threading

MAX_STEPPER_SPEED = 0.0008 # The minimum ms delay between steps

def start_motor_monitor(motor, interval=0.1):
    """
    Continuously prints the motor's current step and percent open.
    Runs in a background thread.
    """

    def monitor():
        while True:
            print(
                f"Current Step: {motor.current_step} | "
                f"Percent Open: {motor.percent_open:.2f}"
            )
            time.sleep(interval)

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()
    return thread



def ms_delay_to_RPS(seconds_per_step, steps_per_revolution):
    if(seconds_per_step < MAX_STEPPER_SPEED):
        seconds_per_step = MAX_STEPPER_SPEED

    seconds_per_revolution = (seconds_per_step * steps_per_revolution)
    return 1/seconds_per_revolution

# Use this function if you want to specify motor speed in RPS (Rotations per second)
# Simply put RPS as the argument, as well as steps per revolution, and function will
# Return the equivalent seconds/step value
def RPS_to_ms_delay(RPS,steps_per_revolution):

    steps_per_ms = RPS * steps_per_revolution
    ms_delay = 1/steps_per_ms

    if(ms_delay < MAX_STEPPER_SPEED):
        ms_delay = MAX_STEPPER_SPEED

    return ms_delay
    

class StepperMotor:
    def __init__(
        self,
        step_pin,
        dir_pin,
        current_step=0,
        percent_open=0.0,
        steps_per_revolution=200
    ):
        # Motor position
        self.current_step = current_step

        # Actuator state
        self.percent_open = percent_open

        # Motor configuration
        self.steps_per_revolution = steps_per_revolution
        self.steps_for_100_percent_open = 6*steps_per_revolution #6.5 turns from 0% to 100%, 6 as safety margin
        self.step_pin = step_pin
        self.dir_pin = dir_pin

        #Motor initialization
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)


    # -------------------------
    # Movement primitives
    # -------------------------
    def step_clockwise(self, steps, delay=MAX_STEPPER_SPEED*2):

        """
        Move the motor clockwise by a given number of steps.

        :param steps: Number of steps to move
        :param delay: Delay between step pulses (seconds)
        """

        # Set direction to counterclockwise
        GPIO.output(self.dir_pin, GPIO.HIGH)

        steps_to_go = steps

        for i in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)
            
            # Update internal position tracking
            if(i%10 == 0):
                self.current_step += 10
                steps_to_go -= 10
                self.percent_open = self.current_step/self.steps_for_100_percent_open

        # Update internal position tracking
        self.current_step += steps_to_go
        self.percent_open = self.current_step/self.steps_for_100_percent_open

        # self.current_step += steps
        #self.percent_open = self.current_step/self.steps_for_100_percent_open

        

    def step_counterclockwise(self, steps, delay=MAX_STEPPER_SPEED*2):
        """
        Move the motor counterclockwise by a given number of steps.

        :param steps: Number of steps to move
        :param delay: Delay between step pulses (seconds)
        """

        # Set direction to counterclockwise
        GPIO.output(self.dir_pin, GPIO.LOW)

        steps_to_go = steps

        for i in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)

            # Update internal position tracking
            if(i%10 == 0):
                self.current_step -= 10
                steps_to_go -= 10
                self.percent_open = self.current_step/self.steps_for_100_percent_open

        # Update internal position tracking
        self.current_step -= steps_to_go
        self.percent_open = self.current_step/self.steps_for_100_percent_open

    
    def set_percent_open(self, percent, delay = MAX_STEPPER_SPEED*2):
        """
        Move actuator to an absolute open percentage (0–100).
        Clockwise opens, counter-clockwise closes.
        """
        
        #Note that the step_clockwise and step_counterclockwise functions
        #update this object's percent_open parameter, so we don't need to
        #do it here

        # Guard against too high percent
        if(percent > 100 or percent < 0): return

        desired_step_value = round((percent/100.0)*self.steps_for_100_percent_open)
        change_in_steps = abs(desired_step_value - self.current_step)

        if(desired_step_value >= self.current_step):
            self.step_clockwise(change_in_steps,delay)
        else:
            self.step_counterclockwise(change_in_steps,delay)



    # -------------------------
    # Calibration
    # -------------------------
    def calibrate(self):
        """
        Reset position and move to half-open.
        """
        # Reset position
        self.current_step = 0
        self.percent_open = 0.0

        # Move to half of total steps
        half_steps = round(self.steps_for_100_percent_open / 2)
        self.step_clockwise(half_steps,delay=MAX_STEPPER_SPEED*2)
