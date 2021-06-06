#!env/bin/python3

import sensors

from tinydb import TinyDB, Query
from datetime import datetime

CPU_SENSOR_NAME = 'k10temp-pci-00c3'
GPU_SENSOR_NAME = 'amdgpu-pci-0a00'

SCRIPT_DURATION = 10*60


def start_logging():
    sensors.init()

    # Get the required chip objects, which in our case is the CPU and GPU chips (get_required_chips)
    # Start a timer which runs for the required SCRIPT_DURATION
    # Log the feature label/value pair (log_sensor_data)
    # Once the SCRIPT_DURATION is complete, the control is given back to start_logging() where sensor.cleanup() happens

    try:
        required_sensor_names = [CPU_SENSOR_NAME, GPU_SENSOR_NAME]
        required_chips = get_required_chips(
            required_sensor_names, sensors.iter_detected_chips())
        log_sensor_data(required_chips)
    finally:
        sensors.cleanup()


def get_required_chips(required_sensor_names, detected_chips):
    required_chips = []
    for chip in detected_chips:
        for sensor_name in required_sensor_names:
            if (chip.__str__() == sensor_name):
                required_chips.append(chip)
                break
    return required_chips


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
