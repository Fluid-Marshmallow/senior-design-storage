from simple_pid import PID
from Load_Cell import Load_Cell
from StepperMotor import StepperMotor

"""
#Constants
"""
# RPi Pins
HIGH_VOLUME_STEP_PIN = 20
HIGH_VOLUME_DIR_PIN = 21

LOW_VOLUME_STEP_PIN = 19
LOW_VOLUME_DIR_PIN = 26

LOAD_CELL_DT_PIN = 6
LOAD_CELL_SCK_PIN = 5

#PID Loop control valves

MAX_FORCE_CHANGE_PER_CYCLE = 1000 #in Newtons

#Force Maximums (For PID loop force to motor movement conversion)
MAX_TENSION_FORCE = 10000 # in Newtons
MAX_COMPRESSION_FORCE = 10000 #in Newtons

class Resistive_Load:
    def __init__(self):

        #Instantiate the PID control loop
        self.pid_controller = PID(Kp = 0.8, Ki = 0.1, Kd = 0.05)
        
        #Instantiate stepper motors to turn valves
        self.high_volume_motor = StepperMotor(step_pin=HIGH_VOLUME_STEP_PIN,
                                                           dir_pin =HIGH_VOLUME_DIR_PIN)
        self.low_volume_motor = StepperMotor(step_pin=LOW_VOLUME_STEP_PIN,
                                                          dir_pin=LOW_VOLUME_DIR_PIN)
        
        #Instantiate the load cell
        self.load_cell = Load_Cell(dt_pin=LOAD_CELL_DT_PIN,
                                   sck_pin=LOAD_CELL_SCK_PIN)
        
        #Set the max % the stepper can change on a single movement
        self.pid_controller.output_limits = (-MAX_FORCE_CHANGE_PER_CYCLE, MAX_FORCE_CHANGE_PER_CYCLE) 
        
        self.most_recent_0x82_message = None
        self.most_recent_0x85_message = None

    # Recieves an 0x82 or 0x85 CAN message and computes the reference force
    # from the message
    def calculate_reference_force(self, current_speed, id, data):
        # Calculates the reference force based on the 82/85 CAN message
        # and curves provided by client. Returns the reference force in N,
        # which is the desired force on the rack

        pass

    # This function takes a specific force value, which was computed by the pid()
    # function, and finds out how many % the motor needs to move in order to reach
    # this desired force
    def move_motor_percent_from_force(self, force):

        #We are assuming that 0% open is max force, and 100% open is 0 force. Linear mapping
        percent_to_move_motor = force/MAX_COMPRESSION_FORCE 

        #Setting limits - cannot move motor more than 5% on a single cycle
        if(percent_to_move_motor > 5 ):
            percent_to_move_motor = 5
        elif(percent_to_move_motor < -5):
            percent_to_move_motor = -5

        return percent_to_move_motor

    # Call this function once in main, at a certain rate, 
    # to handle all your desired PID updates
    def handle_pid_updates(self, id, data):

        # Calculates the reference force based on current vehicle speed and current steering wheel torque
        self.pid_controller.setpoint = self.calculate_reference_force(id,data)

        # Reads the current force on the rack from the load cell
        current_force = self.load_cell.read_force()

        # Uses PID terms to see the change in force that should occur to get closer to the reference force
        force_to_change = self.pid_controller(current_force)

        # Based off the force_to_change value, we need to know how much percent to move the motor to achieve
        # the desired force. See the move_motor_percent_from_force function to adjust how this is calculated.
        percent_to_move_motor = self.move_motor_percent_from_force(force_to_change)

        # Move motors
        self.high_volume_motor.set_percent_open(self.high_volume_motor.percent_open + percent_to_move_motor)

        # Mirror opposite motor to match force when pulling wheel back. Don't add percent_to_move_motor because
        # self.high_volume_motor's percent_open accounts for the change in the above function call.
        self.low_volume_motor.set_percent_open(self.high_volume_motor.percent_open) 
    




        
