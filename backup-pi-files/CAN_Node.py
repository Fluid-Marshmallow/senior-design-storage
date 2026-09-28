# This object recieves CAN messages from the bus and stores
# the messages in its own buffer. These messages are then
# processed by various functions inside the object. If more
# functions are needed, they can be added to this object.

import can
import time
from collections import deque
import subprocess


class CAN_Node:
    def __init__(self):

        subprocess.run(["sudo", "ip", "link", "set", "can0", "down"], check=False)
        subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate", "500000"], check=True)

        self.bus = can.interface.Bus(channel='can0', bustype='socketcan')
        self.buffer = deque(maxlen=100)
        self.allowed_codes_rx = [0x82,0x85,0x84]

        self.CAN_speed_message_count = 0

    def CAN_send_speed(self, speed):
        """
        #Speed is given as a float in mph. The conversion for the
        #message goes as follows: 60mph -> 6000 for bytes 1 and 2.
        #40mph -> 4000 for bytes 1 and 2, etc.
        #Bytes 3 and 4 are ??
        """

        #Adjusting speed for message
        adjusted_speed = round(speed*100)

        # Convert speed to 2 bytes for message bytes 0 and 1
        byte_0 = (adjusted_speed >> 8) & 0xFF
        byte_1 = adjusted_speed & 0xFF

        #Initalize data list to send
        data_list = [0x00, 0x00, 0xD0, 0xF8, 0x0F, 0xFF, 0x0F, 0xFF]

        #adjust data list based on changed values
        data_list[0] = byte_0
        data_list[1] = byte_1

        #Create CAN message
        msg = can.Message(
                arbitration_id=0x415,
                data=data_list,
                is_extended_id=False
            )
            
        #Send CAN message
        try:
            self.bus.send(msg)
            self.CAN_speed_message_count += 1
            print(f"Sent. Count = {self.CAN_speed_message_count}")

        except can.CanError:
            print("CAN Error: Error sending speed (x415) message. Ensure everything plugged in correctly")

    def CAN_recieve_message(self,id,timeout = 0.001):
        """
        Reads a CAN message, filters by CAN ID,
        stores it in the buffer, and returns an 8-byte data list.
        """
        msg = self.bus.recv(timeout=timeout)

        if msg is not None and msg.arbitration_id == id:
            # Convert data to 8-byte list (zero padded)
            data = list(msg.data)
            data.extend([0x00] * (8 - len(data)))

            self.buffer.append(data)
            return data

        return None
