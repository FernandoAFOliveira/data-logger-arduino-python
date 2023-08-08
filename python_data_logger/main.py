# main.py
import os
from user_input import get_port, get_directory, get_filename
from data_logger import DataLogger
from multiprocessing import Queue

from config import CURRENT_SETTINGS_PATH
print(os.path.abspath(CURRENT_SETTINGS_PATH))


if __name__ == "__main__":
    # Gather necessary inputs in the main process
    default_port = 'COM3'
    port = get_port(default_port)
    default_directory = 'data_logs'
    directory = get_directory(default_directory)
    default_filename = 'data_log.csv'
    filename_base = get_filename(default_filename)

    # Create a queue for communication (if necessary)
    queue = Queue(maxsize=1000)

    # Instantiate and start the DataLogger process
    logger = DataLogger(queue, port, directory, filename_base)
    logger.start()

    # If you have other processes or threads, you can start them here as well

    logger.join()

    # If you have other processes or threads, join them here as well
