#!env/bin/python3

import sensors

from tinydb import TinyDB, Query
from datetime import datetime

CPU_SENSOR_NAME = 'k10temp-pci-00c3'
GPU_SENSOR_NAME = 'amdgpu-pci-0a00'

SCRIPT_DURATION = 10*60


def start_logging():
    sensors.init()

    # Get the required chip objects, which in our case is the CPU and GPU chips
    # Call function log_chip_information() which starts a timer for the required SCRIPT_DURATION and
    # handles the subsequent cases.
    # Once the SCRIPT_DURATION is complete, the program gives control back to start_logging() where
    # sensors.cleanup() happens.

    try:
        required_sensor_names = [CPU_SENSOR_NAME, GPU_SENSOR_NAME]
        required_chips = get_required_chips(
            required_sensor_names, sensors.iter_detected_chips())
        log_sensor_data(sensors.iter_detected_chips())
    finally:
        sensors.cleanup()


def get_required_chips(required_sensor_names, detected_chips):
    return "required chips"


def get_db_file_name():
    now = datetime.now()
    return 'db-{datetime}.json'.format(datetime=now.strftime("%d-%m-%Y-%H-%M"))


def log_sensor_data(detected_chips):
    for chip in detected_chips:
        print('%s at %s' % (chip.__str__(), chip.adapter_name))
        for feature in chip:
            print(' %s: %.2f' % (feature.label, feature.get_value()))


if __name__ == '__main__':
    start_logging()
