# pedal_key_test.py

pedal_voltage = 0.0
brake_voltage = 0.0

MAX_VOLTAGE = 3.3
STEP = 0.1

def read_pedal_voltage():
    return pedal_voltage

def read_break_voltage():
    return brake_voltage

def increase_pedal():
    global pedal_voltage
    pedal_voltage = min(MAX_VOLTAGE, pedal_voltage + STEP)

def decrease_pedal():
    global pedal_voltage
    pedal_voltage = max(0.0, pedal_voltage - STEP)

def increase_brake():
    global brake_voltage
    brake_voltage = min(MAX_VOLTAGE, brake_voltage + STEP)

def decrease_brake():
    global brake_voltage
    brake_voltage = max(0.0, brake_voltage - STEP)