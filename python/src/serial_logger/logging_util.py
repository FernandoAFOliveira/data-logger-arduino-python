#logging_util.py
import csv
from datetime import datetime
from pathlib import Path

def setup_file(filename: Path):  # Add typing for clarity
    file = open(filename, "w", newline='')
    writer = csv.writer(file)
    writer.writerow(["Time", "Data"])
    return file, writer

def log_data(writer, data_time, data):
    writer.writerow([data_time, data])
