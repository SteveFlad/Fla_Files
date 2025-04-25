import sys
import serial
import tkinter as tk
from tkinter import ttk

# Initialize the serial connection
ser = serial.Serial(
    port='COM3',
    baudrate=9600,
    timeout=1  # Set a timeout for non-blocking read
)
print("Connected to: " + ser.portstr)

# Create the main Tkinter window
root = tk.Tk()
root.title("Club Data Display")

# Create a frame to hold the Treeview and scrollbar
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Create a vertical scrollbar
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)

# Create a treeview to display the data
columns = ("Time (ms)", "A-X", "A-Y", "A-Z", "G-X", "G-Y", "G-Z", "Q-R", "Q-I", "Q-J", "Q-K")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=15, yscrollcommand=scrollbar.set)

# Configure the scrollbar to work with the Treeview
scrollbar.config(command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Define column headings
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Function to update the treeview with new data
def update_data():
    try:
        line = ser.readline().decode('utf-8').strip()
        if line:
            data = line.split(',')
            if len(data) == 11:  # Check that the data is valid
                # Insert the new data into the treeview
                tree.insert("", tk.END, values=data)
                # Automatically scroll to the bottom
                tree.yview_moveto(1.0)
    except Exception as e:
        print(f"Error reading serial data: {e}")
    finally:
        # Schedule the function to run again after 100ms
        # root.after(100, update_data)
        root.after(1,update_data)
# Start updating the data
update_data()

# Handle window close event
def on_closing():
    print("\nExiting...")
    ser.close()
    root.destroy()
    sys.exit()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the Tkinter main loop
root.mainloop()