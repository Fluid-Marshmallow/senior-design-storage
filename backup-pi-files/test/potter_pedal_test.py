from curses import raw

import spidev
import time

device = 0
bus = 0
src_vlt = 5

#Enable SPI
spi = spidev.SpiDev()
spi.open(bus,device)
spi.max_speed_hz = 100000

def read_pedal_voltage():
    # 4 is two devices change to 6 if one
    # 64 is reading fron channel 1
    MOSI_Data = [0x6, 0b01000000, 0x00]
    MISO_Data = spi.xfer(MOSI_Data)

    raw = ((MISO_Data[1] & 0x0F) << 8) + MISO_Data[2]
    volt = raw * 5 / 4096
    return volt

def read_brake_voltage():
    # 4 is two devices change to 6 if one
    # 128 is reading fron channel 2
    MOSI_Data = [0x6, 0b10000000, 0x00]
    MISO_Data = spi.xfer(MOSI_Data)

    raw = ((MISO_Data[1] & 0x0F) << 8) + MISO_Data[2]
    volt = raw * 5 / 4096
    return volt


while True:
    gas = read_pedal_voltage()
    brake = read_brake_voltage()
    print( gas," ")


    time.sleep(0.1)