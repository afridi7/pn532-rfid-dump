# PN532 RFID Dumper/Logger

Small Python 3 script that watches a PN532 NFC reader over UART and, whenever a new card is detected, runs `nfc-list -v` and appends the full output to a log file.



## Hardware / Environment

- PN532-based NFC reader (UART mode)
- usb-serial adapter connected to PN532 uart (tx/rx/gnd, and 5v/3.3v as required)
- linux host (tested on `/dev/ttyUSB0`, adapt if needed)




## Dependencies

### system packages

- `python3`
- `python3-pip` (or equivalent)
- `libnfc` and tools (for `nfc-list`), e.g.:

```bash
sudo apt-get install libnfc-bin
pip install pyserial adafruit-circuitpython-pn532
```


## Configuration
Adjust these values in the script if needed:

```
SERIAL_PORT = "/dev/ttyUSB0"
BAUDRATE = 115200
LOG_FILE = "detections.txt"
READ_TIMEOUT = 0.5
POLL_DELAY = 0.1
```

Ensure your user has access to the serial port:
```
sudo usermod -aG dialout $USER
```


## Usage
```
python3 pn532-rfid-dump.py
```
