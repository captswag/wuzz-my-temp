#!env/bin/python3

import sensors

from tinydb import TinyDB, Query
from datetime import datetime
import time
import os

# Enhancement suggestion 1: take this as system args
CPU_SENSOR_NAME = 'k10temp-pci-00c3'
GPU_SENSOR_NAME = 'amdgpu-pci-0a00'

# Enhacement suggestion 2: take this as system args
SCRIPT_DURATION = 10*60


def setup():
    sensors.init()
    try:
        required_sensor_names = [CPU_SENSOR_NAME, GPU_SENSOR_NAME]
        required_chips = get_required_chips(
            required_sensor_names, sensors.iter_detected_chips())
        db = setup_db()
        start_logging(db, required_chips, SCRIPT_DURATION)
    finally:
        sensors.cleanup()


def get_required_chips(required_sensor_names, detected_chips):
    required_chips = []
    for chip in detected_chips:
        for sensor_name in required_sensor_names:
            if chip.__str__() == sensor_name:
                required_chips.append(chip)
                break
    return required_chips


def setup_db():
    folder_name = "logs"
    create_logs_directory(folder_name)
    db_name = get_db_file_name()
    return TinyDB('{folder_name}/{db_name}'.format(folder_name=folder_name, db_name=db_name))


def create_logs_directory(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


def get_db_file_name():
    now = datetime.now()
    return 'db-{datetime}.json'.format(datetime=now.strftime("%d-%m-%Y-%H-%M"))


def start_logging(db, required_chips, script_duration):
    time_elapsed = 0
    while (time_elapsed < script_duration):
        log_sensor_data(db, time_elapsed, required_chips)
        time.sleep(1)  # Interval is set to 1 second
        time_elapsed += 1


def log_sensor_data(db, time_elapsed, detected_chips):
    for chip in detected_chips:
        table = db.table(chip.__str__())
        features = {'time_elapsed': time_elapsed}
        for feature in chip:
            features[feature.label] = '{:.2f}'.format(
                round(feature.get_value(), 2))
        table.insert(features)


if __name__ == '__main__':
    setup()
