# main.py
import time
from Simulation import Simulation
from Car import Car
from Resistive_Load import Resistive_Load

def main():
    # Create car object with default simulator conditions
    simulation_car = Car()
    simulation_resistive_load = Resistive_Load()

    # Launch Simulation and GUI with the Car object
    simulation = Simulation(simulation_car,simulation_resistive_load)

    # No blocking while loop needed; GUI uses after() to update itself
    # Any simulation logic should be inside Gui.update_speed() or called via root.after()

if __name__ == "__main__":
    main()


# keeping these comments but these need to go inside the update speed functions
    #Poll for inputs

        #Poll for gas pedal inputs
        #poll for load cell inputs
        #Recieve steering wheel torque CAN message

    #Calculations

        #Calculate new vehicle speed based on inputs from pedals, and save into car object
        #Calculate reference force based off steering wheel torque and current speed

    #Output
        
        #Handle GUI updates:
        # -show new vehicle speed 
        # -update graphs
        #Send vehicle speed on CAN bus
        #do PID control for Resistive Load/move motors to get load closer to reference force


