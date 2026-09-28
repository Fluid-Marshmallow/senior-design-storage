import StepperMotor
import time

high_volume_motor = StepperMotor.StepperMotor(step_pin=20 ,dir_pin = 21)
low_volume_motor = StepperMotor.StepperMotor(step_pin=19, dir_pin=26)

#StepperMotor.start_motor_monitor(high_volume_motor)

#Assuming that 100% open is 10 turns.

# high_volume_motor.calibrate() # This should do 5 turns on the motor

# time.sleep(3)

# high_volume_motor.set_percent_open(60, delay=0.0008) #should do 1 turn
# time.sleep(3)
# high_volume_motor.set_percent_open(80, delay=0.0008) #should do 2 turnW
# time.sleep(3)
# high_volume_motor.set_percent_open(100) #should do 1 turn
# time.sleep(3)
# high_volume_motor.set_percent_open(20) #should do 8 inverse turn
# time.sleep(3)
# high_volume_motor.set_percent_open(0) #should do 2 turns
# time.sleep(3)
# high_volume_motor.set_percent_open(50)

StepperMotor.start_motor_monitor(low_volume_motor)

low_volume_motor.calibrate() # This should do 5 turns on the motor

time.sleep(3)

low_volume_motor.set_percent_open(60, delay=0.0008) #should do 1 turn
time.sleep(3)
low_volume_motor.set_percent_open(80, delay=0.0008) #should do 2 turnW
time.sleep(3)
low_volume_motor.set_percent_open(100) #should do 1 turn
time.sleep(3)
low_volume_motor.set_percent_open(20) #should do 8 inverse turn
time.sleep(3)
low_volume_motor.set_percent_open(0) #should do 2 turns
time.sleep(3)
low_volume_motor.set_percent_open(50)

print("simulation complete")


print("simulation complete")
