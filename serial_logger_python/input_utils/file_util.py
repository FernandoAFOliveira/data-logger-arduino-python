# file_util.py
import os
from datetime import datetime
from config import load_current_settings, save_current_settings, save_last_successful

current_settings = load_current_settings()

def set_directory(directory):
    """
    Create a directory and update the configuration.
    
    Parameters:
    - directory (str): The path of the directory to create.
    
    Returns:
    - tuple: (bool, str)
    - bool: True if directory creation was successful, False otherwise.
    - str: The directory path on success, or an error message on failure.
    """
    try:
        os.makedirs(directory, exist_ok=True)
        current_settings['Directory']['default_directory'] = directory
        save_last_successful(current_settings)
        save_current_settings(current_settings)
        return True, directory
    except OSError as e:
        return False, str(e)
    
def set_filename(filename_base):
    """
    Generate a timestamped filename based on the provided base.
    
    Parameters:
    - filename_base (str): The base of the filename.
    
    Returns:
    - tuple: (bool, str)
    - bool: True if filename generation was successful, False otherwise.
    - str: The generated filename on success, or an error message on failure.
    """
    try:
        now = datetime.utcnow()
        time_stamp = now.strftime('%Y_%m_%d_%H')
        filename = f"{filename_base}_UTC_{time_stamp}.csv"
        current_settings['Filename']['default_filename'] = filename_base
        save_last_successful(current_settings)
        save_current_settings(current_settings)
        return True, filename
    except Exception as e:
        return False, str(e)

