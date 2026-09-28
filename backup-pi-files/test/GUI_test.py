import tkinter as tk
from tkinter import ttk
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def select(event):
    # Get the selected item from the combobox and update the label
    selected_item = combo_box.get()
    label.config(text=f"Selected item: {selected_item}")
    print("Selected item:", selected_item)

# Create main window
root = tk.Tk()
root.title("EVS Steering Simulator")

style = ttk.Style()
style.configure("TCombobox", font=("Arial", 20))  # Sets font for both entry and dropdown

big_font = ("Arial", 20)  # Font name and size

# Labels for columns
tk.Label(root, text="Car Make:", font=big_font).grid(row=0, column=0, padx=5, pady=5)
tk.Label(root, text="Car Model:", font=big_font).grid(row=0, column=1, padx=5, pady=5)
tk.Label(root, text="Car Year:", font=big_font).grid(row=0, column=2, padx=5, pady=5)
tk.Label(root, text="Terrain:", font=big_font).grid(row=0, column=3, padx=5, pady=5)
tk.Label(root, text="Weather:", font=big_font).grid(row=0, column=4, padx=5, pady=5)

# Combobox for car make
combo_box = ttk.Combobox(root, values=["Ford"], state="readonly", font=big_font)
combo_box.set("Select Car Make")
combo_box.grid(row=1, column=0, padx=5, pady=5)
combo_box.bind("<<ComboboxSelected>>", select)

# Combobox for car model;
combo_box2 = ttk.Combobox(root, values=["F-150"], state="readonly", font=big_font)
combo_box2.set("Select Car Model")
combo_box2.grid(row=1, column=1, padx=5, pady=5)
combo_box2.bind("<<ComboboxSelected>>", select)

# Combobox for car year;
combo_box3 = ttk.Combobox(root, values=["2020", "2021", "2022"], state="readonly", font=big_font)
combo_box3.set("Select Car Year")
combo_box3.grid(row=1, column=2, padx=5, pady=5)
combo_box3.bind("<<ComboboxSelected>>", select)

# Combobox for Terrain;
combo_box4 = ttk.Combobox(root, values=["Rocky", "Ice", "Asphalt"], state="readonly", font=big_font)
combo_box4.set("Select Terrain")
combo_box4.grid(row=1, column=3, padx=5, pady=5)
combo_box4.bind("<<ComboboxSelected>>", select)

# Combobox for weather;
combo_box5 = ttk.Combobox(root, values=["Sunny", "Rainy", "Snowy"], state="readonly", font=big_font)
combo_box5.set("Select Weather")
combo_box5.grid(row=1, column=4, padx=5, pady=5)
combo_box5.bind("<<ComboboxSelected>>", select)

# Speed display (row 2, column 0 = next row, left side)
speed_label1 = tk.Label(root, text="Current Speed:", font=("Arial", 40))
speed_label1.grid(row=2, rowspan=1, column=0, columnspan=2, padx=5, pady=5)
speed_label2 = tk.Label(root, text="(mph)", font=("Arial", 40))
speed_label2.grid(row=3, rowspan=1, column=0, columnspan=2, padx=5, pady=5)

speed_var = tk.StringVar()
speed_var.set("0")

speed_label = tk.Label(root, textvariable=speed_var, font=("Arial", 200))
speed_label.grid(row=4, rowspan=3, column=0, columnspan=2, padx=10, pady=20)


# Start / Stop control flag
running = False

def start():
    global running
    running = True
    print("Started")

def stop():
    global running
    running = False
    print("Stopped")

# Start button (green)
start_button = tk.Button(
    root,
    text="START",
    font=("Arial", 40),
    bg="green",
    fg="white",
    width=12,
    height=5,
    command=start
)
start_button.grid(row=3, column=2, rowspan=2, columnspan=2,padx=20, pady=20)

# Stop button (red)
stop_button = tk.Button(
    root,
    text="STOP",
    font=("Arial", 40),
    bg="red",
    fg="white",
    width=12,
    height=5,
    command=stop
)
stop_button.grid(row=3, column=4, rowspan=2, columnspan=2,padx=20, pady=20)

assist_efforts = []
speed_data = []
force_on_axle = []
time_data = []
t = 0

def update_data():
    global t

    # Simulated data (replace later with real inputs)
    assist_num = random.randint(0, 100)
    speed_num = random.randint(0, 100)
    force_num = random.randint(0,100)

    assist_efforts.append(assist_num)
    speed_data.append(speed_num)
    force_on_axle.append(force_num)
    time_data.append(t)

    t += 1

    # Keep last 50 points
    if len(time_data) > 50:
        time_data.pop(0)
        assist_efforts.pop(0)
        speed_data.pop(0)
        force_on_axle.pop(0)

def update_graphs():
    ax1.clear()
    ax1.plot(time_data, assist_efforts)
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Assist Level")

    ax2.clear()
    ax2.plot(time_data, speed_data)
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Speed (mph)")

    ax3.clear()
    ax3.plot(time_data, force_on_axle)
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Force")

    fig1.tight_layout()
    fig2.tight_layout()
    fig3.tight_layout()

    canvas1.draw()
    canvas2.draw()
    canvas3.draw()

def update_speed():
    if running:
        # Replace with real calculation
        new_speed = random.randint(0, 120)
        speed_var.set(f"{new_speed}")

        update_data()
        update_graphs()

    root.after(500, update_speed)

# Start updating
update_speed()

# ----- GRAPH 1 -----
tk.Label(root, text="Assist Efforts:", font=("Arial", 20)).grid(row=7, column=0, columnspan=2)

fig1 = plt.Figure(figsize=(5, 3))
ax1 = fig1.add_subplot(111)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Assist Level")
fig1.tight_layout()

canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1.get_tk_widget().grid(row=8,rowspan=4, column=0, columnspan=2)


# ----- GRAPH 2 -----
tk.Label(root, text="Speed:", font=("Arial", 20)).grid(row=7, column=2, columnspan=2)

fig2 = plt.Figure(figsize=(5, 3))
ax2 = fig2.add_subplot(111)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Speed (mph)")
fig2.tight_layout()

canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas2.get_tk_widget().grid(row=8,rowspan=4, column=2, columnspan=2)


# ----- GRAPH 3 -----
tk.Label(root, text="Force on Axle:", font=("Arial", 20)).grid(row=7, column=4, columnspan=2)

fig3 = plt.Figure(figsize=(5, 3))
ax3 = fig3.add_subplot(111)
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Force")
fig3.tight_layout()

canvas3 = FigureCanvasTkAgg(fig3, master=root)
canvas3.get_tk_widget().grid(row=8, rowspan=4, column=4, columnspan=2)

# Start event loop
root.mainloop()