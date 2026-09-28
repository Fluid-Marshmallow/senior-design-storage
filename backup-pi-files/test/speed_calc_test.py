from speed_calc import update_vehicle
import time

# ---------------- TEST PARAMETERS ----------------
dt = 0.1  # timestep (seconds)
speed = 0.0
accel = 0.0

# Test pedal voltages: from 0.8 (min) to 4.2 (max)
test_voltages = [
    0.8, 0.9, 1.2, 1.5, 1.8, 2.0, 2.5, 3.0, 3.5, 4.0, 4.2
]

# ---------------- RUN TEST ----------------
print(f"{'Voltage':>8} | {'Speed':>8} | {'Accel':>8}")
print("-" * 30)

for voltage in test_voltages:
    # Run simulation for a few timesteps to see gradual acceleration
    for _ in range(10):
        speed, accel = update_vehicle(voltage, speed, accel, dt)
        print(f"{voltage:>8.2f} | {speed:>8.2f} | {accel:>8.2f}")
        time.sleep(0.05)  # just to slow print, optional

    print("-" * 30)