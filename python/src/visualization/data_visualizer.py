# data_visualizer.py

import time
from src.serial_logger.serial_reader import heartbeat_received

def mock_visualization():
    """
    Mock function to simulate visualization process.
    """
    while True:
        print("Visualizing data...")
        time.sleep(1)  # Simulating some processing
        heartbeat_received()  # Sending heartbeat

def simulate_crash():
    """
    Simulate a crash or abrupt termination.
    """
    time.sleep(5)  # Run for 5 seconds
    exit(0)  # Exit the process

if __name__ == "__main__":
    try:
        mock_visualization()
    except Exception as e:
        print(f"Exception occurred: {e}")
        simulate_crash()
