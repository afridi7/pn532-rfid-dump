#!/usr/bin/env python3

import serial
import time
import subprocess
from adafruit_pn532.uart import PN532_UART

SERIAL_PORT = "/dev/ttyUSB0" #change based on your hardware config
BAUDRATE = 115200
LOG_FILE = "detections.txt"
READ_TIMEOUT = 0.5
POLL_DELAY = 0.1


def log_detection():
    try:
        result = subprocess.run(
            ["nfc-list", "-v"],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout.strip()
        if not output:
            output = "(no output from nfc-list)"

        #write to log file
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n=== card detected at {timestamp} ===\n")
            f.write(output + "\n")

    except Exception as e:
        print(f"failed to capture nfc-list output: {e}")


def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    except Exception as e:
        print(f"Failed to open serial port {SERIAL_PORT}: {e}")
        return

    try:
        pn532 = PN532_UART(ser, debug=False)
    except Exception as e:
        print("Failed to initialize PN532 over UART:", e)
        ser.close()
        return

    try:
        try:
            fw = pn532.firmware_version
            if fw:
                print("PN532 firmware version:", fw)
        except Exception:
            pass

        # try to configure SAM
        try:
            pn532.SAM_configuration()
        except Exception:
            pass

        print("scanning... (press ctrl+c to stop)")
        previous_present = False

        while True:
            try:
                uid = pn532.read_passive_target(timeout=READ_TIMEOUT)
            except Exception:
                time.sleep(POLL_DELAY)
                continue

            if uid is not None:
                if not previous_present:
                    print("card found")
                    try:
                        log_detection()
                    except Exception as e:
                        print("failed to write to log file:", e)
                    previous_present = True
                time.sleep(0.2)
            else:
                previous_present = False
                time.sleep(POLL_DELAY)

    except KeyboardInterrupt:
        print("\nexiting.")
    finally:
        ser.close()


if __name__ == "__main__":
    main()
