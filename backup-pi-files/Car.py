# car.py

import can
from CAN_Node import CAN_Node
import time
from speed_calc import update_vehicle


class Car:

    def __init__(self, make="ford", model="f-150", year="2022",
                 terrain="asphalt", weather="sunny", current_speed=0,
                 accel_curve=None):

        self.make = make.lower()
        self.model = model.lower()
        self.year = year

        self.current_speed = current_speed
        self.current_accel = 0.0

        # Not using true physics mass scaling (kept for future upgrade)
        self.mass = 1800.0

        self.terrain = terrain.lower()
        self.weather = weather.lower()

        self.max_accel = 12.0
        self.max_speed = 60.0

        # FIXED baseline tuning
        self.rolling_resistance = 0.02
        self.air_drag = 0.01

        self.speed_scale_value = 1.0
        self.friction_scale_value = 1.0

        # More realistic F-150-like curve
        if accel_curve is None:
            self.accel_curve = [
                (0, 6.5),
                (10, 6.0),
                (20, 5.2),
                (30, 4.5),
                (40, 3.6),
                (50, 2.8),
                (60, 2.0),
                (70, 1.5),
                (80, 1.0),
                (85, 0.5)
            ]
        else:
            self.accel_curve = accel_curve

        self.update_physics()

        try:
            self.can_node = CAN_Node()
        except:
            print("ERROR: Failed to establish CAN connection")

    def update_physics(self):

        terrain_map = {
            "asphalt": 1.0,
            "rocky": 1.3,
            "ice": 0.5,
        }

        weather_map = {
            "sunny": 1.0,
            "rainy": 0.85,
            "snowy": 0.6,
        }

        terrain_factor = terrain_map.get(self.terrain, 1.0)
        weather_factor = weather_map.get(self.weather, 1.0)

        self.rolling_resistance = 0.02 * terrain_factor
        self.max_accel = 12.0 * weather_factor

        self.air_drag = 0.01 if self.terrain != "ice" else 0.008

        if self.model == "f-150":
            self.max_speed = 85.0

        self.speed_scale_value = weather_factor
        self.friction_scale_value = terrain_factor

    def update(self, gas_voltage, brake_voltage, dt):
        update_vehicle(self, gas_voltage, brake_voltage, dt)

    def set_make(self, make):
        self.make = make.lower()

    def set_model(self, model):
        self.model = model.lower()
        self.update_physics()

    def set_year(self, year):
        self.year = year

    def set_terrain(self, terrain):
        self.terrain = terrain.lower()
        self.update_physics()

    def set_weather(self, weather):
        self.weather = weather.lower()
        self.update_physics()

    def set_speed(self, speed):
        if speed < 0:
            raise ValueError("Speed cannot be negative.")
        self.current_speed = speed

    def get_effective_speed(self):
        return self.current_speed * self.speed_scale_value

    def CAN_send_speed(self, speed):
        return self.can_node.CAN_send_speed(speed)

    def CAN_recieve_message(self,id,timeout=0.001):
        return self.can_node.CAN_recieve_message(id=id,timeout=timeout)

    def __str__(self):
        return (
            f"{self.year} {self.make} {self.model}\n"
            f"Terrain: {self.terrain}, Weather: {self.weather}\n"
            f"Speed: {self.current_speed:.2f} mph\n"
            f"Accel: {self.current_accel:.2f}\n"
            f"Max Speed: {self.max_speed}\n"
        )