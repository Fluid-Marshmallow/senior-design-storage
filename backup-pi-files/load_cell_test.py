import RPi.GPIO as GPIO
import time
from Load_Cell import Load_Cell

load_cell = Load_Cell()

for i in range(50):
    force_val = load_cell.read_force()
    #force_val = load_cell.read_averaged_digital_value()
    print(force_val)
    time.sleep(.5)

GPIO.cleanup()

# import RPi.GPIO as GPIO
# import time

# DT = 6
# SCK = 5

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(DT, GPIO.IN)
# GPIO.setup(SCK, GPIO.OUT)

# GPIO.output(SCK, 0)

# def read_hx711():
#     while GPIO.input(DT) == 1:
#         pass

#     data = 0

#     for _ in range(24):
#         GPIO.output(SCK, 1)
#         data <<= 1
#         GPIO.output(SCK, 0)

#         if GPIO.input(DT):
#             data += 1

#     # gain pulse (128x, channel A)
#     GPIO.output(SCK, 1)
#     GPIO.output(SCK, 0)

#     if data & 0x800000:
#         data -= 0x1000000

#     return data

# try:
#     # ---- tare ----
#     samples = 100
#     ZERO_OFFSET = sum(read_hx711() for _ in range(samples)) // samples
#     print("Zero offset:", ZERO_OFFSET)

#     # ---- averaging parameters ----
#     AVG_SAMPLES = 5     # number of readings to average
#     PRINT_DELAY = 0.05  # seconds between outputs

#     while True:
#         total = 0
#         for _ in range(AVG_SAMPLES):
#             total += read_hx711()

#         avg_value = (total // AVG_SAMPLES) - ZERO_OFFSET
#         print(avg_value)

#         time.sleep(PRINT_DELAY)

# except KeyboardInterrupt:
#     GPIO.cleanup()