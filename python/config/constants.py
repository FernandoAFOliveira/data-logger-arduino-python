#constants.py

import re

INVALID_FILENAME_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
MAX_DIRECTORY_LENGTH = 20  # max length of directory name
MAX_FILENAME_LENGTH = 20    # This does not include the appended timestamp

# Port name patterns for different operating systems
WINDOWS_PORT_PATTERN = re.compile(r'COM\d+')
LINUX_PORT_PATTERN = re.compile(r'/dev/tty[A-Za-z]+\d+')
MAC_PORT_PATTERN = re.compile(r'/dev/tty\..+')