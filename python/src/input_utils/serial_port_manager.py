#serial_port_manager.py
import serial
import platform
import time
from config.constants import WINDOWS_PORT_PATTERN, LINUX_PORT_PATTERN, MAC_PORT_PATTERN
from input_utils.input_prompts import prompt_for_serial_port

def get_os_type():
    """
    Determines the type of operating system.
    
    Returns:
    - str: Type of OS ('windows', 'linux', 'mac', or 'unknown').
    """
    os_string = platform.system().lower()
    if 'windows' in os_string:
        return 'windows'
    elif 'linux' in os_string:
        return 'linux'
    elif 'darwin' in os_string:
        return 'mac'
    else:
        return 'unknown'

def is_valid_port(port_name):
    """
    Validates the port name based on the current OS type.
    """
    os_type = get_os_type()
    if os_type == 'windows':
        return bool(WINDOWS_PORT_PATTERN.match(port_name))
    elif os_type == 'linux':
        return bool(LINUX_PORT_PATTERN.match(port_name))
    elif os_type == 'mac':
        return bool(MAC_PORT_PATTERN.match(port_name))
    return False

def establish_port_connection(default_port='COM3'):
    """
    Attempt to establish a connection to the given port.
    If the connection fails, prompt the user to input a valid port.
    
    Returns:
    - str: Name of the successfully connected port.
    """
    port = default_port

    while True:
        if not is_valid_port(port):
            print(f"'{port}' is not a valid port name for your operating system. Please try another one.")
            port = prompt_for_serial_port(default_port)
        elif not try_connect_to_port(port):
            print(f"System cannot connect to Arduino on port '{port}'. Please try another one.")
            port = prompt_for_serial_port(default_port)
        else:
            break
        
    return port

def try_connect_to_port(port_name):
    """
    Try to establish a connection to a given serial port.
    
    Returns:
    - bool: True if connection is successful, False otherwise.
    """
    try:
        with serial.Serial(port_name):
            return True
    except (serial.SerialException, OSError):
        return False
    
def setup_serial_connection(port):
    try:
        arduino = serial.Serial(port, 9600)
        time.sleep(2)  # give connection a second to establish
        return arduino
    except serial.SerialException:
        print(f"Unable to open serial port: {port}")
        exit(1)
