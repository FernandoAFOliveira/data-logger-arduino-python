# user_input.py
import os
import serial
from datetime import datetime

INVALID_FILENAME_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

def get_port(default_port):
    print(f"Default port: {default_port}")
    while True:
        port = input("Enter the serial port or press Enter to accept the default: ")
        if not port:
            port = default_port
        try:
            arduino = serial.Serial(port, 9600, timeout=.1)
            arduino.close()
            return port
        except serial.serialutil.SerialException:
            print(f"System cannot connect to Arduino on port '{port}'. Please try another one.")

def get_directory(default_directory):
    print(f"Default directory: {default_directory}")
    while True:
        directory = input("Enter the directory to save data logs or press Enter to accept the default: ").strip()
        if not directory:
            directory = default_directory
        
        # Check for invalid characters
        if any(char in directory for char in INVALID_FILENAME_CHARS):
            print("The directory name contains invalid characters. Please enter a valid directory name.")
            continue
        
        # Check if directory exists or can be created
        try:
            os.makedirs(directory, exist_ok=True)
            return directory
        except Exception as e:
            print(f"An error occurred while creating the directory: {e}. Please try another one.")

def get_filename(default_filename):
    now = datetime.utcnow()
    time_stamp = now.strftime('%Y_%m_%d_%H')
    print(f"Default filename: {default_filename}")
    while True:
        filename_base = input("Enter the base name for the data log or press Enter to accept the default: ").strip()
        if not filename_base:
            filename_base = default_filename

        # Check for invalid characters in filename
        if any(char in filename_base for char in INVALID_FILENAME_CHARS):
            print("The filename contains invalid characters. Please enter a valid filename.")
            continue
        
        filename = f"{filename_base}_{time_stamp}.csv"
        return filename

