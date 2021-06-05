#!env/bin/python3

import sensors

from tinydb import TinyDB, Query
from datetime import datetime

CPU_SENSOR = 'k10temp-pci-00c3'
GPU_SENSOR = 'amdgpu-pci-0a00'


def start_logging():
    sensors.init()
    try:
        for chip in sensors.iter_detected_chips():
            print('%s at %s' % (chip.__str__(), chip.adapter_name))
            for feature in chip:
                print(' %s: %.2f' % (feature.label, feature.get_value()))
    finally:
        sensors.cleanup()


def get_db_file_name():
    datetime.now()


if __name__ == '__main__':
    start_logging()
