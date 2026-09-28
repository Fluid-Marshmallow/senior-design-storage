import can
import time

bus = can.interface.Bus(channel='can0', bustype='socketcan')
count = 0
while True:
    msg = can.Message(
        arbitration_id=0x415,
        data=[0x00, 0x00, 0xD0, 0xF8, 0x0F, 0xFF, 0x0F, 0xFF],
        is_extended_id=False
    )
    
    try:
        bus.send(msg)
        count = count+1
        print(f"Sent. Count = {count}")

    except can.CanError:
        print("Error sending")
    
    time.sleep(0.01)