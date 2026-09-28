"""
Vehicle dynamics (tuned for stable gameplay + realistic truck feel)
"""

V_MIN = 0.10
V_MAX = 5.12
ACCEL_RESPONSE = 3.0

ENGINE_SCALE = 4.5  


def normalize_voltage(voltage):
    return max(0.0, min(1.0, (voltage - V_MIN) / (V_MAX - V_MIN)))


def pedal_to_target_accel(voltage, car):
    x = normalize_voltage(voltage)

    speed = car.current_speed
    curve = car.accel_curve

    if speed <= curve[0][0]:
        base_accel = curve[0][1]
    elif speed >= curve[-1][0]:
        base_accel = curve[-1][1]
    else:
        base_accel = curve[-1][1]
        for i in range(len(curve) - 1):
            s0, a0 = curve[i]
            s1, a1 = curve[i + 1]
            if s0 <= speed <= s1:
                t = (speed - s0) / (s1 - s0)
                base_accel = a0 + t * (a1 - a0)
                break

    return base_accel * (x ** 2) * ENGINE_SCALE


def brake_to_target_decel(voltage, car):
    x = normalize_voltage(voltage)
    return -car.max_accel * (x ** 2) * 1.5


def smooth_acceleration(current_accel, target_accel, dt):
    return current_accel + (target_accel - current_accel) * ACCEL_RESPONSE * dt


def compute_drag(speed, car):
    # FIXED: reduced drag so engine can actually overcome it
    return car.rolling_resistance * 0.1 + car.air_drag * (speed ** 2) * 0.01


def update_vehicle(car, gas_voltage, brake_voltage, dt):

    gas_accel = pedal_to_target_accel(gas_voltage, car)
    brake_accel = brake_to_target_decel(brake_voltage, car)

    target_accel = gas_accel + brake_accel

    car.current_accel = smooth_acceleration(car.current_accel, target_accel, dt)

    drag = compute_drag(car.current_speed, car)

    net_accel = car.current_accel - 6*drag

    car.current_speed += net_accel * dt

    if car.current_speed < 0:
        car.current_speed = 0
        car.current_accel = 0

    car.current_speed = min(car.max_speed, car.current_speed)