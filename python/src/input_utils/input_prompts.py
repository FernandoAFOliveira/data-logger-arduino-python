#input_prompts.py
from config.constants import INVALID_FILENAME_CHARS, MAX_FILENAME_LENGTH
from serial_port_manager import is_valid_port
from file_util import validate_directory

def prompt_for_serial_port(default_port):
    while True:
        port = input("Enter the serial port or press Enter to accept the default: ").strip()
        port = port or default_port
        
        if not is_valid_port(port):
            print("Invalid port name. Please try again.")
            continue
        
        return port

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
            return directory
        else:
            print(f"Invalid directory. Please try another directory.")

def prompt_for_filename(default_filename, last_used=None):
    print(f"Default filename: {default_filename}")
    
    if last_used:
        print(f"Last used filename: {last_used}")
        
    while True:
        filename_base = input("Enter the filename or press Enter to accept the default (or 'L' for last used): ").strip()
        filename_base = filename_base or default_filename
        
        if len(filename_base) > MAX_FILENAME_LENGTH:
            print(f"Please limit the filename to {MAX_FILENAME_LENGTH} characters (excluding timestamp).")
            continue
        if any(char in filename_base for char in INVALID_FILENAME_CHARS):
            print(f"The filename contains invalid characters. Please avoid using: {', '.join(INVALID_FILENAME_CHARS)}")
            continue
            
        return filename_base
