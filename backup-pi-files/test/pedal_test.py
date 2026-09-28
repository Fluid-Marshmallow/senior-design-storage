import spidev
import time
import matplotlib.pyplot as plt
from collections import deque

# Reference voltage
VREF = 5

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)  # bus 0, device 0
spi.max_speed_hz = 1000000

def read_channel(channel):
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be 0-7")

    start_bit = 0x04
    single_ended = 0x02

    command = start_bit | single_ended | (channel >> 2)
    second_byte = (channel & 0x03) << 6

    response = spi.xfer2([command, second_byte, 0x00])

    adc_value = ((response[1] & 0x0F) << 8) | response[2]
    return adc_value

def read_voltage(channel):
    adc_value = read_channel(channel)
    voltage = (adc_value / 4095.0) * VREF
    return voltage

# Plot setup
plt.ion()
fig, ax = plt.subplots()

time_window = 10  # seconds
sample_interval = 0.1  # seconds

max_points = int(time_window / sample_interval)

times = deque(maxlen=max_points)
voltages = deque(maxlen=max_points)

start_time = time.time()

try:
    while True:
        current_time = time.time() - start_time
        voltage = read_voltage(0)

        times.append(current_time)
        voltages.append(voltage)

        ax.clear()
        ax.plot(times, voltages)

        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Voltage (V)")
        ax.set_title("Live Voltage (10s Window)")
        ax.set_xlim(max(0, current_time - time_window), current_time)
        ax.set_ylim(0, VREF)

        plt.pause(0.001)

        time.sleep(sample_interval)

except KeyboardInterrupt:
    spi.close()
    print("Stopped")