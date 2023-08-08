#data_logger.py
import csv
import os
from datetime import datetime, timedelta
import serial
from user_input import get_port, get_directory, get_filename, setup_file
from multiprocessing import Process, Queue

class DataLogger(Process):
    def __init__(self, queue, port, directory, filename_base):
        super(DataLogger, self).__init__()
        self.queue = queue
        self.port = port
        self.directory = directory
        self.filename_base = filename_base
    
    def run(self):
        
       # Use self.port directly, no need to ask for user input here
        arduino = serial.Serial(self.port, 9600, timeout=.1)
        
        # Use self.directory and self.filename_base directly
        print("Starting initial test logging for one minute...")
        test_filename = os.path.join(self.directory, f"test_{self.filename_base}")
        
        # Step 3: Test Logging
        print("Starting initial test logging for one minute...")
        test_filename = os.path.join(self.directory, f"test_{self.filename_base}")
        test_file, test_writer = setup_file(test_filename)
        end_time = datetime.now() + timedelta(minutes=1)
        while datetime.now() < end_time:
            data = arduino.readline()[:-2]
            if data:
                decoded_data = data.decode()
                print(f"Test data: {decoded_data}")
                test_writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), decoded_data])
        test_file.close()
        print(f"Test logging complete. Data saved to {test_filename}")

        # Step 4: Main Logging
        file_path = os.path.join(self.directory, self.filename_base)
        file, writer = setup_file(file_path)
        print(f'Success! Logging data to {file_path}.')
        
        try:
            while True:       
                current_hour = datetime.now().hour
                writer.writerow([datetime.now().strftime("%Y-%b-%d from %H:00 to %H:59")])
                data_row = []
                current_minute = datetime.now().minute

                while datetime.now().hour == current_hour:
                    data = arduino.readline()[:-2]
                    if data:
                        decoded_data = data.decode()
                        print(f"Received data: {decoded_data}")
                        self.queue.put(decoded_data) 
                        if datetime.now().minute == current_minute:
                            data_row.append(decoded_data)
                        else:
                            writer.writerow([f"{current_hour}:{str(current_minute).zfill(2)}"] + data_row)
                            data_row = [decoded_data]
                            current_minute = datetime.now().minute

                writer.writerow([f"{current_hour}:{str(current_minute).zfill(2)}"] + data_row)
                
        except KeyboardInterrupt:
            print('Data logging stopped.')
            file.close()

if __name__ == "__main__":
    queue = Queue(maxsize=1000)
    logger = DataLogger(queue)
    # visualizer = DataVisualizer(queue)  # Uncomment when ready

    logger.start()
    # visualizer.start()  # Uncomment when ready

    logger.join()
    # visualizer.join()  # Uncomment when ready
