#Captures serial data from COM port and logs it in csv file.
import csv
import os
from datetime import datetime
import serial

#Function returns filename for csv file based on current time.
def get_filename():
    now = datetime.now()
    return f"data-logs/data-log-{now.strftime('%Y-%m-%d-H%H')}.csv"

#Function creates new folder if does not exists, creates csv file and returns file object and writer object.
def setup_file(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    file = open(filename, 'w', newline='')
    writer = csv.writer(file)
    return file, writer

def main():
    arduino = serial.Serial('COM3', 9600, timeout=.1)
    while True:
        filename = get_filename()
        file, writer = setup_file(filename)
        print(f'Success! Logging data to {filename}.')

        try:
            current_hour = datetime.now().hour
            minute_headers = [f"{current_hour}:{str(minute).zfill(2)}" for minute in range(60)]
            writer.writerow([datetime.now().strftime("%Y-%b-%d from %H:00 to %H:59")])
            writer.writerow(minute_headers)
            
            while datetime.now().hour == current_hour:
                data = arduino.readline()[:-2] 
                if data:
                    decoded_data = data.decode()
                    print(f"Received data: {decoded_data}") 
                    writer.writerow([decoded_data])
            
        except KeyboardInterrupt:
            print('Data logging stopped.')
            file.close()
            break

        file.close()

if __name__ == "__main__":
    main()
