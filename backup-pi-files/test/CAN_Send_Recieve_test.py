import time
from Car import Car   # adjust import if filename differs

SEND_INTERVAL = 0.020   # 1 ms
RECV_INTERVAL = 0.020   # 1 ms
TEST_DURATION = 5.0     # seconds

SPEED_TEST_VALUE = 30.0 # mph
TX_CAN_ID = 0x415
RX_CAN_ID = 0x85

def format_can_frame(can_id, data):
    """
    Formats CAN ID and 8-byte data list as a HEX string.
    """
    data_hex = " ".join(f"{byte:02X}" for byte in data)
    return f"ID: 0x{can_id:03X} | DATA: {data_hex}"

def build_speed_data(speed):
    """
    Rebuilds the exact speed payload used by CAN_Node.
    """
    adjusted_speed = round(speed * 100)

    byte_0 = (adjusted_speed >> 8) & 0xFF
    byte_1 = adjusted_speed & 0xFF

    data = [byte_0, byte_1, 0xD0, 0xF8, 0x0F, 0xFF, 0x0F, 0xFF]
    return data

def main():
    car = Car()

    sent_frames = []
    recv_frames = []

    start_time = time.perf_counter()
    next_send_time = start_time
    next_recv_time = start_time

    while (time.perf_counter() - start_time) < TEST_DURATION:
        now = time.perf_counter()

        # SEND speed message every 1 ms
        if now >= next_send_time:
            car.CAN_send_speed(SPEED_TEST_VALUE)

            tx_data = build_speed_data(SPEED_TEST_VALUE)
            sent_frames.append((TX_CAN_ID, tx_data))

            next_send_time += SEND_INTERVAL

        # RECEIVE CAN ID 0x82 message every 1 ms
        if now >= next_recv_time:
            data = car.can_node.CAN_recieve_message(
                id=RX_CAN_ID,
                timeout=0.001
            )
            if data is not None:
                recv_frames.append((RX_CAN_ID, data))

            next_recv_time += RECV_INTERVAL

    # ---- RESULTS ----
    print("\n================ TEST RESULTS ================\n")

    print("Sent CAN Messages:")
    print(f"Total Sent: {len(sent_frames)}\n")
    for can_id, data in sent_frames:
        print(format_can_frame(can_id, data))

    print("\n----------------------------------------------\n")

    print("Received CAN Messages:")
    print(f"Total Received: {len(recv_frames)}\n")
    for can_id, data in recv_frames:
        print(format_can_frame(can_id, data))

    print("\n==============================================\n")

if __name__ == "__main__":
    main()