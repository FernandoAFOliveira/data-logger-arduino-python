# Captures serial data from COM port and logs it in csv file.
import csv
import os
from datetime import datetime, timedelta
import serial
from user_input import get_port, get_directory, get_filename

def setup_file(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    file = open(filename, 'w', newline='')
    writer = csv.writer(file)
    return file, writer

def start_logging():
    # Step 1: Get Port
    default_port = 'COM3'
    port = get_port(default_port)
    arduino = serial.Serial(port, 9600, timeout=.1)
    
    # Step 2: Get Directory and Filename
    default_directory = 'data_logs'
    directory = get_directory(default_directory)
    default_filename = 'data_log.csv'
    filename_base = get_filename(default_filename)
    
    # Step 3: Test Logging using provided directory and "test_" prefix for filename
    print("Starting initial test logging for one minute...")
    test_filename = os.path.join(directory, f"test_{filename_base}")
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
    file_path = os.path.join(directory, filename_base)
    file, writer = setup_file(file_path)
    print(f'Success! Logging data to {file_path}.')
    # Rest of the logging process...

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
    start_logging()
