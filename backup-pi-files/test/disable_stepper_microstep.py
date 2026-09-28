import serial
import time

# ------------------------
# User configuration
# ------------------------
UART_PORT = "/dev/serial0"   # e.g., Raspberry Pi UART
BAUDRATE = 115200
TMC_ADDRESS = 0              # Driver address (default 0)

# ------------------------
# CHOPCONF microstep mask
# ------------------------
# CHOPCONF register: microstep (MRES) bits 24-28
# 0b00000 = full step
MRES_FULL_STEP = 0b01001111111000000000000010001100

# Register addresses
CHOPCONF_ADDR = 0x6C

# ------------------------
# Helper functions
# ------------------------
def calc_crc(data_bytes):
    """
    Calculate 8-bit CRC for TMC packets
    """
    crc = 0
    for b in data_bytes:
        crc ^= b
    return crc & 0xFF

def build_write_packet(addr, register, value):
    """
    Build a TMC2209 UART write packet
    Format: [Sync, Addr, Reg, Data0..3, CRC]
    """

    data = [
        0x05,        # Sync
        addr & 0xF,  # Driver address (4 bits)
        register & 0xFF,
        (value >> 24) & 0xFF,
        (value >> 16) & 0xFF,
        (value >> 8) & 0xFF,
        value & 0xFF
    ]
    crc = calc_crc(data)
    data.append(crc)
    return bytes(data)

# ------------------------
# Main routine
# ------------------------
def disable_microstepping():
    # Open UART
    with serial.Serial(UART_PORT, BAUDRATE, timeout=0.1) as ser:
        # Compose packet
        packet = build_write_packet(CHOPCONF_ADDR, CHOPCONF_ADDR, MRES_FULL_STEP)
        
        # Send packet
        ser.write(packet)
        time.sleep(0.1)
        
        print("Microstepping disabled: full-step mode set.")

# ------------------------
# Run script
# ------------------------
if __name__ == "__main__":
    disable_microstepping()