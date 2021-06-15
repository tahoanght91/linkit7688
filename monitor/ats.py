import time

from config import *
from config.common import *

MAIN = 0
GEN = 1
TEST = 2

last_run = 0
last_rest = 0
last_test = 0


def _send_command(command):
    if command == 'main' and client_attributes.get('atsMode', default_data.atsMode) != MAIN:
        commands_lock.acquire()
        commands[DEVICE_ATS] = 'main'
        commands_lock.release()
        return 'main'
    elif command == 'gen' and client_attributes.get('atsMode', default_data.atsMode) != GEN:
        commands_lock.acquire()
        commands[DEVICE_ATS] = 'gen'
        commands_lock.release()
        return 'gen'
    elif command == 'test' and client_attributes.get('atsMode', default_data.atsMode) != TEST:
        commands_lock.acquire()
        commands[DEVICE_ATS] = 'auto'
        commands_lock.release()
        return 'auto'
    return ''


# This method is called every loop if the device is in Auto mode
def check_status():
    global last_run, last_rest, last_test
    mode = client_attributes.get('atsMode', default_data.atsMode)
    now = time.time()
    if mode == MAIN:
        last_rest = now
    else:
        last_run = now

    if (telemetries.get('atsVacP1', default_data.atsVacP1) <= shared_attributes.get('atsVacThreshold', default_data.atsVacThreshold)
            and (mode == MAIN and now - last_run > shared_attributes.get('atsMinRestTime', default_data.atsMinRestTime)
                 or mode == GEN and now - last_rest < shared_attributes.get('atsMaxRunTime', default_data.atsMaxRunTime))
            and (client_attributes.get('atsIsAllBatFull', default_data.atsIsAllBatFull) == 0
                 or shared_attributes.get('atsBatFull', default_data.atsBatFull) == 0)
            and telemetries.get('dcVdc', default_data.dcVdc) < shared_attributes.get('atsVdcThreshold', default_data.atsVdcThreshold)):
        LOGGER.debug('ATS mode GEN')
        return _send_command('gen')
    elif (shared_attributes.get('atsTestEn', default_data.atsTestEn) == 1
          and (mode != TEST and now - last_test > shared_attributes.get('atsTestCycle', default_data.atsTestCycle)
               or mode == TEST and now - last_test < shared_attributes.get('atsTestTime', default_data.atsTestTime))):
        if mode != TEST:
            last_test = now
        LOGGER.debug('ATS mode AUTO')
        return _send_command('auto')
    else:
        LOGGER.debug('ATS mode MAIN')
        return _send_command('main')
