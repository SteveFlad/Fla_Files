import sys
import datetime
import PySimpleGUI as sg
import serial
import serial.tools.list_ports  
import tkinter as tk

# Set the default font for all Tkinter widgets
root = tk.Tk()
default_font = ("Helvetica", 28)  # Change the font size as needed
root.option_add("*Font", default_font)
root.withdraw()  # Hide the root window

ports = list(serial.tools.list_ports.comports())
ports.sort()
port_descriptions = [port.description for port in ports]
port_dict = {port.description: port.device for port in ports}

layout = [  
    [sg.Text("Serial Port:"),
     sg.Combo(values=port_descriptions, key="-COM_PORT-"),
     sg.Button("Open Port")],            
    
    [sg.Text("                       |  ______ ACCELEROMETER ________  |  __________ GYROSCOPE __________  |  ____________ QUATERNIONS _________________  |")],
    [sg.Text("  Time(ms)     |      A-X                    A-Y                   A-Z        |       G-X                   G-Y                    G-Z         |       Q-R                  Q-I                  Q-J                   Q-K          |")],
    [sg.Text(size=(10,1),background_color='white', text_color='black',key='-ETIME-'), 
     sg.Text(size=(10,1),background_color='white', text_color='black',key='-A-X-'), 
     sg.Text(size=(10,1),background_color='white', text_color='black',key='-A-Y-'), 
     sg.Text(size=(10,1),background_color='white', text_color='black',key='-A-Z-'),       
     sg.Text(size=(10,1),background_color='white', text_color='black',key='-G-X-'), 
     sg.Text(size=(10,1),background_color='white', text_color='black',key='-G-Y-'),   
     sg.Text(size=(10,1),background_color='white', text_color='black',key='-G-Z-'), 
     sg.Text(size=(10,1),background_color='white', text_color='black',key='-Q-R-'), 
     sg.Text(size=(10,1),background_color='white', text_color='black',key='-Q-I-'),
     sg.Text(size=(10,1),background_color='white', text_color='black',key='-Q-J-'),  
     sg.Text(size=(10,1),background_color='white', text_color='black',key='-Q-K-')], 
     
    [sg.Canvas(size=(500, 500), background_color='red', key='canvas')],
    [sg.Text('Change circle color to:'), sg.Button('Red'), sg.Button('Blue', )],
]

window = sg.Window('Club Data Display', layout, finalize=True)

cir = window['canvas'].TKCanvas.create_oval(50, 50, 100, 100)

ser = None

while True:
    event, values = window.read(timeout=100)  # Add a timeout to the read
    
    if event == "Open Port":
        selected_desc = values["-COM_PORT-"]
        if selected_desc:
            selected_port = port_dict.get(selected_desc)
            if selected_port:
                try:
                    ser = serial.Serial(selected_port, 115200, timeout=1)  
                    print(f"Opened port: {selected_port}")
                except serial.SerialException as e:
                    print(f"Error opening port: {e}")
    
    if event in ('Blue', 'Red'): 
        window['canvas'].TKCanvas.itemconfig(cir, fill=event) 
        
    if event == sg.WIN_CLOSED or event == 'Cancel':
        if ser:
            ser.close()
        window.close()
        sys.exit()
    
    if ser and ser.is_open:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                # Serial data is comma-separated
                data = line.split(',')
                if len(data) == 11:  # The number of expected values
                    window['-ETIME-'].update(data[0])
                    window['-A-X-'].update(data[1])
                    window['-A-Y-'].update(data[2])
                    window['-A-Z-'].update(data[3])
                    window['-G-X-'].update(data[4])
                    window['-G-Y-'].update(data[5])
                    window['-G-Z-'].update(data[6])
                    window['-Q-R-'].update(data[7])
                    window['-Q-I-'].update(data[8])
                    window['-Q-J-'].update(data[9])
                    window['-Q-K-'].update(data[10])
        except Exception as e:
            print(f"Error reading serial data: {e}")