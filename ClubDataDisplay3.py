# ClubDataDisplay3.py
import sys
import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation as R  # For quaternion to Euler conversion
from collections import deque  # Import deque for buffering

# Initialize the serial communication
ser = None
reading_serial = False  # Flag to control serial data reading

# Create the main Tkinter window
root = tk.Tk()
root.title("Club Data Display")
root.geometry("1200x1000")

# Create a frame for the serial port selection
frame_top = tk.Frame(root)
frame_top.pack(fill=tk.X, padx=1, pady=5)

# Serial port selection
ports = list(serial.tools.list_ports.comports())
ports.sort()
port_dict = {port.description: port.device for port in ports}
port_descriptions = list(port_dict.keys())

tk.Label(frame_top, text="Serial Port:").pack(side=tk.LEFT, padx=5)
port_combo = ttk.Combobox(frame_top, values=port_descriptions, state="readonly")
port_combo.pack(side=tk.LEFT, padx=5)
open_port_button = tk.Button(frame_top, text="Open Port")
open_port_button.pack(side=tk.LEFT, padx=5)

# Create a frame for the data display
frame_data = tk.Frame(root)
frame_data.pack(fill=tk.X, padx=10, pady=5)

# Create labels for data display
labels = [" Time (ms)", "     A-X", "      A-Y", "      A-Z", "      G-X", "      G-Y", "      G-Z", "      Q-R", "      Q-I", "      Q-J", "      Q-K"]
data_labels = {}

# Use grid layout for better alignment
for i, label in enumerate(labels):
    tk.Label(frame_data, text=label, width=10, anchor="w").grid(row=0, column=i, padx=2, pady=2)
    data_labels[label] = tk.Label(frame_data, text="N/A", width=10, anchor="w", bg="white")
    data_labels[label].grid(row=1, column=i, padx=2, pady=2)

# Create a frame for the 3D plots
frame_plot = tk.Frame(root)
frame_plot.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Create 3D matplotlib figures for accelerometer, gyroscope, and quaternion data
fig_acc = plt.figure(figsize=(4, 4))
ax_acc = fig_acc.add_subplot(111, projection='3d')
canvas_acc = FigureCanvasTkAgg(fig_acc, frame_plot)
canvas_acc.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

fig_gyro = plt.figure(figsize=(4, 4))
ax_gyro = fig_gyro.add_subplot(111, projection='3d')
canvas_gyro = FigureCanvasTkAgg(fig_gyro, frame_plot)
canvas_gyro.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

fig_quat = plt.figure(figsize=(4, 4))
ax_quat = fig_quat.add_subplot(111, projection='3d')
canvas_quat = FigureCanvasTkAgg(fig_quat, frame_plot)
canvas_quat.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Data buffers
acc_data = []
gyro_data = []
quat_data = []
data_buffer = deque(maxlen=1000)

# Function to convert quaternion to Euler angles
def quaternion_to_euler(qr, qi, qj, qk):
    r = R.from_quat([qi, qj, qk, qr])  # Note: scipy uses [x, y, z, w] format
    return r.as_euler('xyz', degrees=True)  # Return roll, pitch, yaw in degrees

# Function to update the 3D graphs
def update_graphs(acc, gyro, quat):
    # Update accelerometer graph
    acc_data.append(acc)
    ax_acc.cla()
    acc_np = np.array(acc_data)
    ax_acc.scatter(acc_np[:, 0], acc_np[:, 1], acc_np[:, 2], c='b', label="Accelerometer")
    ax_acc.set_xlabel("X")
    ax_acc.set_ylabel("Y")
    ax_acc.set_zlabel("Z")
    ax_acc.set_title("Accelerometer Data")
    ax_acc.legend()
    canvas_acc.draw()

    # Update gyroscope graph
    gyro_data.append(gyro)
    ax_gyro.cla()
    gyro_np = np.array(gyro_data)
    ax_gyro.scatter(gyro_np[:, 0], gyro_np[:, 1], gyro_np[:, 2], c='g', label="Gyroscope")
    ax_gyro.set_xlabel("X")
    ax_gyro.set_ylabel("Y")
    ax_gyro.set_zlabel("Z")
    ax_gyro.set_title("Gyroscope Data")
    ax_gyro.legend()
    canvas_gyro.draw()

    # Update quaternion graph
    quat_data.append(quat)
    ax_quat.cla()
    quat_np = np.array(quat_data)
    ax_quat.scatter(quat_np[:, 0], quat_np[:, 1], quat_np[:, 2], c='r', label="Quaternion")
    ax_quat.set_xlabel("Q-R")
    ax_quat.set_ylabel("Q-I")
    ax_quat.set_zlabel("Q-J")
    ax_quat.set_title("Quaternion Data")
    ax_quat.legend()
    canvas_quat.draw()

# Function to read serial data
def read_serial_data():
    global reading_serial
    if ser and ser.is_open and reading_serial:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                data_buffer.append(line)
        except Exception as e:
            print(f"Error reading line from serial: {e}")

        if len(data_buffer) > 0:
            try:
                data = data_buffer.popleft().split(',')
                if len(data) == 11:
                    # Update the data labels
                    for i, label in enumerate(labels):
                        data_labels[label].config(text=data[i])

                    # Process accelerometer, gyroscope, and quaternion data
                    acc = [float(data[1]), float(data[2]), float(data[3])]
                    gyro = [float(data[4]), float(data[5]), float(data[6])]
                    quat = [float(data[7]), float(data[8]), float(data[9]),float(data[10])]
                    # Quant comes in as Real,I,J,K so we need to convert it to I,J,K,Real
                    # quat = [quat[1], quat[2], quat[3], quat[0]]
                   
                    print(f"Accelerometer: {acc}")
                    print(f"Gyroscope: {gyro}") 
                    print(f"Quaternion: {quat}")
                    
                    # Update the graphs
                    update_graphs(acc, gyro, quat)
            except Exception as e:
                print(f"Error processing serial data: {e}")

    root.after(100, read_serial_data)

# Function to open the serial port
def open_port():
    global ser
    selected_desc = port_combo.get()
    if selected_desc:
        selected_port = port_dict.get(selected_desc)
        if selected_port:
            try:
                ser = serial.Serial(selected_port, 9600, timeout=1)
                print(f"Opened port: {selected_port}")
            except serial.SerialException as e:
                print(f"Error opening port: {e}")

# Function to toggle serial reading
def toggle_reading():
    global reading_serial
    reading_serial = not reading_serial
    if reading_serial:
        acc_data.clear()
        gyro_data.clear()
        quat_data.clear()
        ax_acc.cla()
        ax_gyro.cla()
        ax_quat.cla()
        canvas_acc.draw()
        canvas_gyro.draw()
        canvas_quat.draw()

# Add button functionality
open_port_button.config(command=open_port)
start_stop_button = tk.Button(frame_top, text="Start/Stop", command=toggle_reading)
start_stop_button.pack(side=tk.LEFT, padx=5)

# Start reading serial data
read_serial_data()

# Handle window close event
def on_closing():
    global ser
    if ser:
        ser.close()
    root.destroy()
    sys.exit()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the Tkinter main loop
root.mainloop()