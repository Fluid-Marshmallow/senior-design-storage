import tkinter as tk
from tkinter import ttk
import random
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from pedal_input import read_pedal_voltage, read_brake_voltage
from Resistive_Load import Resistive_Load
#from Car import Car  # make sure you have car.py with the updated Car class

class Simulation:
    def __init__(self, car, resistive_load):
        self.running = False
        self.initial_start = False
        self.car = car
        self.resistive_load = resistive_load

        # Realistic time tracking
        self.last_update_time = time.time()
        self.t = 0  # simulation time in seconds

        # Track whether each required input has been selected
        self.inputs_ready = {
            "make": False,
            "model": False,
            "year": False,
            "terrain": False,
            "weather": False,
        }

        # Data storage for graphs
        self.assist_efforts = []
        self.speed_data = []
        self.force_on_axle = []
        self.time_data = []

        self.frozen_speed = 0
        self.frozen_time = 0

        self.root = tk.Tk()
        self.root.title("EVS Steering Simulator")

        self.root.focus_set()

        self._build_gui()
        self._build_graphs()

        #Schedule all events (all functions below will run at specified Hz)
        self.update_speed()
        self.CAN_send_speed()
        self.CAN_recieve_messages()
        #self.handle_pid_updates()

        # Run Main loop
        self.root.mainloop()

    # Button callbacks
    def start(self):
        """
        Start the simulation if all inputs are ready
        """
        if not all(self.inputs_ready.values()):
            self.label.config(text="Please select all inputs before starting.",
                              fg="red")
            print("Start failed: not all inputs ready")
            return
        
        # Disable all combo boxes
        for combo in self.combos:
            combo.config(state="disabled")
        
        if (not self.initial_start):
            # Tell user to fully close both valves:
            popup = tk.Toplevel(self.root)
            popup.title("Calibration Step")
            popup.grab_set()  # make popup modal

            tk.Label(popup, text="Please fully close both resistive load valves to calibrate system", font=("Arial", 24)).pack(padx=30, pady=20)

            tk.Button(
                popup,
                text="Both resistive load valves have been fully closed",
                font=("Arial", 16),
                command=popup.destroy
            ).pack(pady=20)

            self.root.wait_window(popup)

            #At this point, both valves have been closed
            self.resistive_load.high_volume_motor.calibrate()
            self.resistive_load.low_volume_motor.calibrate()
            self.initial_start = True

            # 1s delay before continuing
            self.root.after(1000)



        self.label.config(text="Simulation Running...")
        self.running = True
        print("Started")

    def stop(self):
        """
        Stop the simulation and re-enable input selectors
        """
        self.running = False

        self.frozen_speed = self.car.current_speed
        self.frozen_time = self.t
        self.last_update_time = time.time()

        # Re-enable combo boxes
        for combo in self.combos:
            combo.config(state="readonly")
        self.label.config(text="Simulation Stopped.")

        self.last_update_time = time.time()  # reset time tracking for when simulation is restarted

        self.running = False
        print("Stopped")

    # Combobox selection handler
    def select(self, event):
        """
        Update Car object when user selects a new value in a combo box
        """
        combo = event.widget
        value = combo.get()
        prop = combo.car_property

        # Update car object
        if prop == "make":
            self.car.set_make(value)
        elif prop == "model":
            self.car.set_model(value)
        elif prop == "year":
            self.car.set_year(value)
        elif prop == "terrain":
            self.car.set_terrain(value)
        elif prop == "weather":
            self.car.set_weather(value)

        # Mark this input as ready
        self.inputs_ready[prop] = True

        # Enable start button if all inputs are ready
        if all(self.inputs_ready.values()):
            self.start_button.config(state="normal")

        # Echo output
        msg = f"{prop.capitalize()} changed to: {value}"
        print(msg)


    # GUI construction
    def _build_gui(self):
        style = ttk.Style()
        style.configure("TCombobox", font=("Arial", 20))

        big_font = ("Arial", 20)

        labels = ["Car Make:", "Car Model:", "Car Year:", "Terrain:", "Weather:"]
        for col, text in enumerate(labels):
            tk.Label(self.root, text=text, font=big_font).grid(
                row=0, column=col, padx=5, pady=5
            )

        self._combo(1, 0, ["Ford"], "Select Car Make", "make")
        self._combo(1, 1, ["F-150"], "Select Car Model", "model")
        self._combo(1, 2, ["2022"], "Select Car Year", "year")
        self._combo(1, 3, ["Rocky", "Ice", "Asphalt"], "Select Terrain", "terrain")
        self._combo(1, 4, ["Sunny", "Rainy", "Snowy"], "Select Weather", "weather")

        tk.Label(self.root, text="Current Speed:", font=("Arial", 40)).grid(
            row=2, column=0, columnspan=2
        )
        tk.Label(self.root, text="(mph)", font=("Arial", 40)).grid(
            row=3, column=0, columnspan=2
        )

        self.speed_var = tk.StringVar(value="0")

        tk.Label(self.root, textvariable=self.speed_var, font=("Arial", 200)).grid(
            row=4, rowspan=3, column=0, columnspan=2, padx=10, pady=20
        )

        self.start_button = tk.Button(
            self.root,
            text="START",
            font=("Arial", 40),
            bg="green",
            fg="white",
            width=12,
            height=5,
            command=self.start,
            state="disabled",
        )
        self.start_button.grid(row=3, column=2, rowspan=2, columnspan=2, padx=20, pady=20)

        tk.Button(
            self.root,
            text="STOP",
            font=("Arial", 40),
            bg="red",
            fg="white",
            width=12,
            height=5,
            command=self.stop,
        ).grid(row=3, column=4, rowspan=2, columnspan=2, padx=20, pady=20)

        self.label = tk.Label(self.root, text="", font=big_font)
        self.label.grid(row=6, column=0, columnspan=6)

    def _combo(self, row, col, values, text, car_property):
        """
        Helper function to create a combo box and bind its event
        """
        combo = ttk.Combobox(
            self.root, values=values, state="readonly", font=("Arial", 20)
        )
        combo.set(text)
        combo.grid(row=row, column=col, padx=5, pady=5)
        combo.car_property = car_property
        combo.bind("<<ComboboxSelected>>", self.select)

        if not hasattr(self, "combos"):
            self.combos = []
        self.combos.append(combo)

    # Graphs
    def _build_graphs(self):
        """
        Initialize matplotlib graphs for assist efforts, speed, and force on axle
        """
        self.fig1, self.ax1, self.line1 = self._create_graph(
            "Assist Efforts:", "Time (s)", "Assist Level", 0
        )
        self.fig2, self.ax2, self.line2 = self._create_graph(
            "Speed:", "Time (s)", "Speed (mph)", 2
        )
        self.fig3, self.ax3, self.line3 = self._create_graph(
            "Force on Axle:", "Time (s)", "Force", 4
        )

        self.fig1.tight_layout()
        self.fig2.tight_layout()
        self.fig3.tight_layout()

    def _create_graph(self, title, xlabel, ylabel, col):
        tk.Label(self.root, text=title, font=("Arial", 20)).grid(
            row=7, column=col, columnspan=2
        )

        fig = plt.Figure(figsize=(5, 3))
        ax = fig.add_subplot(111)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        line, = ax.plot([], [], lw=2)

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().grid(
            row=8, rowspan=4, column=col, columnspan=2
        )

        setattr(self, f"canvas{col}", canvas)

        return fig, ax, line

    # Data updates
    def update_data(self, dt):
        """
        Updates the data arrays for plotting.
        Maintains a sliding window of the last 50 points.
        """
        self.root.focus_set()

        if self.running == True:
            # Simulated placeholder data
            self.assist_efforts.append(random.randint(0, 100))
            self.force_on_axle.append(random.randint(0, 100))

            # Real speed from Car object
            self.speed_data.append(self.car.current_speed)

            # Update time using realistic dt
            self.t += dt
            self.time_data.append(self.t)

            # Keep last 50 points in the sliding window
            if len(self.time_data) > 50:
                self.assist_efforts.pop(0)
                self.speed_data.pop(0)
                self.force_on_axle.pop(0)
                self.time_data.pop(0)

    def update_graphs(self):
        """
        Clear and redraw graphs
        """
        if self.running:
            # Update line data instead of clearing axes
            self.line1.set_data(self.time_data, self.assist_efforts)
            self.line2.set_data(self.time_data, self.speed_data)
            self.line3.set_data(self.time_data, self.force_on_axle)

            # Rescale axes dynamically
            self.ax1.relim()
            self.ax1.autoscale_view()

            self.ax2.relim()
            self.ax2.autoscale_view()

            self.ax3.relim()
            self.ax3.autoscale_view()

            # Draw efficiently
            self.canvas0.draw_idle()
            self.canvas2.draw_idle()
            self.canvas4.draw_idle()


    """
    Main Loop : ALL OF THE FUNCTIONS BELOW RUN AT A SCHEDULED INTERVAL
    """

    def update_speed(self):
        """
        Real-time vehicle update loop.
        Reads pedal/brake, updates vehicle physics, updates speed display, and refreshes graphs.
        dt is computed based on real elapsed time.
        """

        if self.running:

            # Compute realistic dt since last update
            current_time = time.time()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time

            # Read pedal voltage only while running
            gas_voltage = read_pedal_voltage()
            brake_voltage = read_brake_voltage()

            # Update vehicle physics
            self.car.update(gas_voltage, brake_voltage, dt)

            # Update speed display in mph
            self.speed_var.set(str(round(self.car.current_speed, 1)))

            self.t += dt

            # Update graphs with realistic time step
            self.update_data(dt)
            self.update_graphs()

        else:
            self.speed_var.set(str(round(self.frozen_speed, 1)))

        # Always reschedule the loop, but it will do nothing when not running
        self.root.after(10, self.update_speed)


    def CAN_send_speed(self):
        if(self.running):
            print("Calling CAN_send_speed()")

            self.car.CAN_send_speed(self.car.current_speed)

        # Schedule next update every 20ms
        self.root.after(20, self.CAN_send_speed) #20ms delay


    #Assumes that the ECU will never send corrupted data
    def CAN_recieve_messages(self):
        if self.running:

            code_0x82_data = self.car.CAN_recieve_message(id=0x82, timeout=0.001)
            code_0x85_data = self.car.CAN_recieve_message(id=0x85, timeout=0.001)

            if code_0x82_data is not None:
                self.resistive_load.most_recent_0x82_message = code_0x82_data

            if code_0x85_data is not None:
                self.resistive_load.most_recent_0x85_message = code_0x85_data

        self.root.after(20, self.CAN_recieve_messages)


    def handle_pid_updates(self):
        print("Calling handle_pid_updates()")

        #Uncomment below lines when PID is ready to be used
        # if(self.running):
        #     self.resistive_load.handle_pid_updates()

        # #Schedule next update every 100ms
        #self.root.after(100,self.handle_pid_updates)

        pass