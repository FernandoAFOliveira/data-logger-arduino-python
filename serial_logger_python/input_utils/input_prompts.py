# input_prompts.py

import serial
from datetime import datetime
from config import INVALID_FILENAME_CHARS, MAX_DIRECTORY_LENGTH, MAX_FILENAME_LENGTH

def prompt_for_port(default_port):
    print(f"Default port: {default_port}")
    while True:
        port = input("Enter the serial port or press Enter to accept the default: ")
        port = port or default_port
        if validate_port(port):
            return port
        print(f"System cannot connect to Arduino on port '{port}'. Please try another one.")

def validate_port(port):
    try:
        arduino = serial.Serial(port, 9600, timeout=.1)
        arduino.close()
        return True
    except serial.serialutil.SerialException:
        return False

def prompt_for_directory(default_directory, last_used=None):
    print(f"Default directory: {default_directory}")
    if last_used:
        print(f"Last used directory: {last_used}")

    while True:
        input_directory = input("Enter the directory or press Enter to accept the default (or 'L' for last used, 'exit' to quit): ").strip()

        if not input_directory:  # If user pressed Enter
            directory = default_directory
        elif input_directory.lower() == 'l' and last_used:  
            directory = last_used
        elif input_directory.lower() == 'exit':
            return None
        else:
            directory = input_directory

        if validate_directory(directory):
            success, result = set_directory(directory)  # Assuming set_directory is imported from file_util.py
            if success:
                print(f"Successfully set directory to: {result}")
                return result
            else:
                print(f"An error occurred: {result}. Please try another directory.")

def prompt_for_filename(default_filename, last_used=None):
    now = datetime.utcnow()
    time_stamp = now.strftime('%Y_%m_%d_%H')
    print(f"Default filename: {default_filename}")
    
    if last_used:
        print(f"Last used filename: {last_used}")
        
    while True:
        input_filename = input("Enter the filename or press Enter to accept the default (or 'L' for last used): ").strip()
        filename_base = input_filename or default_filename
        
        if len(filename_base) > MAX_FILENAME_LENGTH:
            print(f"Please limit the filename to {MAX_FILENAME_LENGTH} characters (excluding timestamp).")
            continue
        if any(char in filename_base for char in INVALID_FILENAME_CHARS):
            print(f"The filename contains invalid characters. Please avoid using: {', '.join(INVALID_FILENAME_CHARS)}")
            continue
            
        filename = f"{filename_base}_{time_stamp}.csv"
        return filename


