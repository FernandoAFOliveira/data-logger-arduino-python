# user_input.py
import os
import csv
import serial
from datetime import datetime
from config import load_current_settings, save_current_settings, save_last_successful, INVALID_FILENAME_CHARS, MAX_DIRECTORY_LENGTH, MAX_FILENAME_LENGTH

# Fetch the current settings
current_settings = load_current_settings()

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
    last_used = current_settings.get('Directory', {}).get('default_directory', None)
    print(f"Default directory: {default_directory}")
    if last_used:
        print(f"Last used directory: {last_used}")

    while True:
        input_directory = input("Enter the directory or press Enter to accept the default (or 'L' for last used, 'exit' to quit): ").strip()

        if not input_directory:  # If user pressed Enter
            directory = default_directory
        elif input_directory.lower() == 'l' and last_used:  # Convert input to lowercase and check
            directory = last_used
        elif input_directory.lower() == 'exit':
            # Handle the exit case as appropriate for your program. 
            # For example, you can return None, or raise an exception, etc.
            return None
        else:
            directory = input_directory

        # Check for length
        if len(directory) > MAX_DIRECTORY_LENGTH:
            print(f"Please limit the directory name to {MAX_DIRECTORY_LENGTH} characters.")
            continue
        # Check for invalid characters
        if any(char in directory for char in INVALID_FILENAME_CHARS):
            print(f"The directory name contains invalid characters. Please avoid using: {', '.join(INVALID_FILENAME_CHARS)}")
            continue

        # Check if directory exists or can be created
        try:
            os.makedirs(directory, exist_ok=True)
            # Update last successful directory
            current_settings['Directory']['default_directory'] = directory
            save_last_successful(current_settings)
            save_current_settings(current_settings)
            print(f"Successfully set directory to: {directory}")
            break
        except Exception as e:
            print(f"An error occurred while creating the directory: {e}. Please try another one.")

    return directory     

#modifying get_filename to get filename_base
def get_filename(default_filename):
    last_used = current_settings.get('Filename', {}).get('default_filename', None)
    now = datetime.utcnow()
    time_stamp = now.strftime('%Y_%m_%d_%H')
    print(f"Default filename: {default_filename}")
    
    if last_used:
        print(f"Last used filename: {last_used}")
        
    while True:
        input_filename = input("Enter the filename or press Enter to accept the default (or 'L' for last used): ").strip()
        
        if not input_filename:  # If user pressed Enter
            filename_base = default_filename
        elif input_filename.lower() == 'l' and last_used:  # Convert input to lowercase and check
            filename_base = last_used
        else:
            filename_base = input_filename
            
        # Check for length
        if len(filename_base) > MAX_FILENAME_LENGTH:
            print(f"Please limit the filename to {MAX_FILENAME_LENGTH} characters (excluding timestamp).")
            continue

        # Check for invalid characters in filename
        if any(char in filename_base for char in INVALID_FILENAME_CHARS):
            print(f"The filename contains invalid characters. Please avoid using: {', '.join(INVALID_FILENAME_CHARS)}")
            continue

        
        filename = f"{filename_base}_{time_stamp}.csv"
        return filename    

def setup_file(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    file = open(filename, 'w', newline='')
    writer = csv.writer(file)
    return file, writer
