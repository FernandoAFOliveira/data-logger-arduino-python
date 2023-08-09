#serial_reader.py
import serial
import signal
import time
from datetime import datetime
from multiprocessing import Queue, Event
from arduino_data import decode_and_timestamp
from input_utils.serial_port_manager import setup_serial_connection

class SerialManager:
    def __init__(self, port):
        self.port = port
        self.logger_queue = Queue()
        self.generic_data_queue = None
        self.arduino = setup_serial_connection(self.port)

    def start_reading(self):
        while True:
            data = self.arduino.readline()[:-2]
            if data:
                timestamped_data = decode_and_timestamp(data)
                self.logger_queue.put(timestamped_data)
                
                if self.generic_data_queue:
                    self.generic_data_queue.put(timestamped_data)

    def get_logger_queue(self):
        return self.logger_queue

    def request_data_queue(self):
        """
        Initializes and returns a new data queue for external classes or scripts.
        """
        self.generic_data_queue = Queue()
        return self.generic_data_queue

    def stop_providing_data(self):
        """
        Stops the provisioning of data to the generic data queue.
        """
        self.generic_data_queue = None
        
HEARTBEAT_TIMEOUT = 10  # let's say 10 seconds for the sake of this example
last_heartbeat_received = datetime.now()

def heartbeat_received():
    """
    This function updates the last received heartbeat timestamp.
    """
    global last_heartbeat_received
    last_heartbeat_received = datetime.now()

def check_heartbeat():
    """
    Checks if the last heartbeat was received within the timeout period.
    """
    global last_heartbeat_received
    return (datetime.now() - last_heartbeat_received).seconds <= HEARTBEAT_TIMEOUT

def graceful_shutdown(signal, frame):
    """
    Handle graceful shutdown when a signal is received.
    """
    print("Serial reader received shutdown signal. Cleaning up...")
    # TODO: Add any cleanup code here if needed
    exit(0)

# Signal handling
signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

while True:
    # Check if heartbeat has been received recently
    if not check_heartbeat():
        print("No heartbeat received for a while. Pausing operations.")
        # Pause operations or stop, based on your requirement
        time.sleep(HEARTBEAT_TIMEOUT)  # Sleeping for the timeout period before checking again
    else:
        # Your usual read and process loop
        pass
