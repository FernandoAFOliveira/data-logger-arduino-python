#main_serial_logging.py
from datetime import datetime
from multiprocessing import Process
from pathlib import Path
from logging_util import setup_file, log_data
from serial_reader import SerialManager
from input_utils import input_prompt

class DataLogger(Process):
    def __init__(self, serial_manager):
        super(DataLogger, self).__init__()
        self.queue = serial_manager.get_logger_queue()
        self.serial_manager = serial_manager
        self.directory = Path(input_prompt.prompt_for_directory())  # Query input_prompt for directory
        self.filename_base = input_prompt.prompt_for_filename()  # Query input_prompt for filename_base

    def run(self):
        # Test Logging
        print("Starting initial test logging for one minute...")
        test_filename = self.directory / f"test_{self.filename_base}.csv"
        test_file, test_writer = setup_file(test_filename)

        end_time = datetime.now() + timedelta(minutes=1)
        while datetime.now() < end_time:
            timestamp, decoded_data = self.queue.get()
            print(f"Test data: {decoded_data}")
            log_data(test_writer, timestamp.strftime("%Y-%m-%d %H:%M:%S"), decoded_data)
        test_file.close()

        # Main Logging
        file_path = self.directory / f"{self.filename_base}.csv"
        file, writer = setup_file(file_path)
        print(f'Success! Logging data to {file_path}.')

        self.main_logging_loop(writer)

        file.close()

    def main_logging_loop(self, writer):
        try:
            while True:
                current_hour = datetime.now().hour
                writer.writerow([datetime.now().strftime("%Y-%b-%d from %H:00 to %H:59")])
                data_row = []
                current_minute = datetime.now().minute

                while datetime.now().hour == current_hour:
                    timestamp, decoded_data = self.queue.get()
                    print(f"Received data: {decoded_data}")
                    if datetime.now().minute == current_minute:
                        data_row.append(decoded_data)
                    else:
                        writer.writerow([f"{current_hour}:{str(current_minute).zfill(2)}"] + data_row)
                        data_row = [decoded_data]
                        current_minute = datetime.now().minute

                writer.writerow([f"{current_hour}:{str(current_minute).zfill(2)}"] + data_row)

        except KeyboardInterrupt:
            print('Data logging stopped.')

if __name__ == "__main__":
    serial_manager = SerialManager()  # Initialize without port. SerialManager gets port from input_prompt or elsewhere.
    serial_manager.start_reading()

    logger = DataLogger(serial_manager)
    # visualizer = DataVisualizer(serial_manager.get_visualizer_queue())  # Uncomment when ready

    logger.start()
    # visualizer.start()  # Uncomment when ready

    logger.join()
    # visualizer.join()  # Uncomment when ready
