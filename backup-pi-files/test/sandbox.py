
MAX_STEPPER_SPEED = 0.0008 # The minimum ms delay between steps

def ms_delay_to_RPS(seconds_per_step, steps_per_revolution):
    if(seconds_per_step < MAX_STEPPER_SPEED):
        seconds_per_step = MAX_STEPPER_SPEED

    seconds_per_revolution = (seconds_per_step * steps_per_revolution)
    return 1/seconds_per_revolution




def RPS_to_ms_delay(RPS,steps_per_revolution):

    steps_per_ms = RPS * steps_per_revolution
    ms_delay = 1/steps_per_ms

    if(ms_delay < MAX_STEPPER_SPEED):
        ms_delay = MAX_STEPPER_SPEED

    return ms_delay
    

x = RPS_to_ms_delay(6.25,200)
print(x)

y = ms_delay_to_RPS(.0008,200)
print(y)



