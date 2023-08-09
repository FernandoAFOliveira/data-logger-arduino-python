from input_utils.file_util import get_directory, get_filename
from python.settings.settings_manager import default_directory
from serial_logger.main_serial_logging import DataLogger
from multiprocessing import Queue
from input_utils.serial_port_manager import establish_port_connection

if __name__ == "__main__":
    # Attempt to establish a connection to a serial port
    port = establish_port_connection()

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
