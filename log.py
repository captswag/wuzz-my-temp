#!env/bin/python3

import sensors

from tinydb import TinyDB, Query

CPU_SENSOR = 'k10temp-pci-00c3'
GPU_SENSOR = 'amdgpu-pci-0a00'


def startLogging():
    print("Start logging")


if __name__ == '__main__':
    startLogging()
