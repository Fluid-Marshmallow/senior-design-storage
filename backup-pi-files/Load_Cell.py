import RPi.GPIO as GPIO
import time

import RPi.GPIO as GPIO
import time

# Value below is experimentally determined by seeing the digital
# output when A+ and A- are connected together

class Load_Cell:

    # Values below come from 20mV = 8388607 in HX711 ADC, and since we are using
    # 3.3V excitation, and load cell outputs 2mV/V, our max load cell voltage range
    # is 0 to 6.6VmV. So 6.6/20 = .33, and 8388607*.33 = 2768240
    
    MAX_DIGITAL_VALUE = 2768240 # corresponds to 3 ton compression
    MIN_DIGITAL_VALUE = -2768240 #corresponds to 3 ton tension
    LOAD_CELL_MAX_WEIGHT = 3000 #kg

    def __init__(self, dt_pin=6, sck_pin=5):
        self.DT = dt_pin
        self.SCK = sck_pin

        self.zero_offset = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dt_pin, GPIO.IN)
        GPIO.setup(sck_pin, GPIO.OUT)

        GPIO.output(sck_pin, 0)

        self.tare()


    def _read_hx711(self):
        while GPIO.input(self.DT) == 1:
            pass

        data = 0

        for _ in range(24):
            GPIO.output(self.SCK, 1)
            data <<= 1
            GPIO.output(self.SCK, 0)

            if GPIO.input(self.DT):
                data += 1

        # gain pulse (128x, channel A)
        GPIO.output(self.SCK, 1)
        GPIO.output(self.SCK, 0)

        if data & 0x800000:
            data -= 0x1000000

        return data
    
    def read_averaged_digital_value(self, samples=5):
        total=0
        for i in range(samples):
            total+=self._read_hx711()

        avg_value = (total // samples) - self.zero_offset

        return avg_value
    

    #Sets the 0 point of the load cell. Call when there is no load on the load cell
    def tare(self):
        self.zero_offset = self.read_averaged_digital_value(50)


    #Reads force from load cell. Change unit to netwons if newtons wanted
    def read_force(self, unit = "kilograms"):

        digital_val = self.read_averaged_digital_value()

        # 3000 because max digital value corresponds to 3000kg force
        force = self.LOAD_CELL_MAX_WEIGHT * (digital_val / self.MAX_DIGITAL_VALUE)

        #clamp force in case too high:
        if(force > self.LOAD_CELL_MAX_WEIGHT):
            force = self.LOAD_CELL_MAX_WEIGHT
        elif(force < -self.LOAD_CELL_MAX_WEIGHT):
            force = -self.LOAD_CELL_MAX_WEIGHT

        if(unit == "newtons"):
            force = force*9.80665

        return force

    def cleanup(self):
        GPIO.cleanup()