import struct

from config import *
from utility import with_check_sum

def _check_command(device, command):
    return (device == 'fan' and (command == 'off' or command == 'on') and not shared_attributes.get('miscFanControlAuto', default_data.miscFanControlAuto)
            or device == 'airc1' and (command == 'off' or command == 'on') and not shared_attributes.get('aircControlAuto', default_data.aircControlAuto)
            or device == 'airc2' and (command == 'off' or command == 'on') and not shared_attributes.get('aircControlAuto', default_data.aircControlAuto)
            # or device == 'ats' and (command == 'main' or command == 'gen' or command == 'test') and not shared_attributes.get('atsControlAuto', default_data.atsControlAuto)
            or device == 'ats' and (command == 'off' or command == 'on') and not shared_attributes.get('atsControlAuto', default_data.atsControlAuto)
            or device == 'crmu' and (command == 'off' or command == 'on') and not shared_attributes.get('crmuControlAuto', default_data.crmuControlAuto)
            or device == 'bell' and (command == 'off' or command == 'on'))


def _process_set_auto(device, command):
    if not (type(command) == bool
            and (device == 'fan'
                    or device == 'airc'
                    or device == 'ats'
                    or device == 'crmu')
                    or device == 'bell'):
        return False
    if device == 'airc':
        shared_attributes['aircControlAuto'] = command
    elif device == 'fan':
        shared_attributes['miscFanControlAuto'] = command
    elif device == 'ats':
        shared_attributes['atsControlAuto'] = command 
    elif device == 'crmu':
        shared_attributes['crmuControlAuto'] = command
    elif device == 'bell':
        shared_attributes['bellAuto'] = command
    return True

def _process_command(device, command):
    LOGGER.info("Go into _process_command")
    if device == 'bell':
        device = 1
        if command == 'off':
            command = 0
        else:
            command = 1
    elif device == 'fan':
        device = 2
        if command == 'off':
            command = 0
        else:
            command = 1
    elif device == 'airc1':
        device = 3
        if command == 'off':
            command = 0
        else:
            command = 1
    elif device == 'airc2':
        device = 4
        if command == 'off':
            command = 0
        else:
            command = 1
    # elif device == 'ats':
    #     device = 5
    #     if command == 'main':
    #         command = 0
    #     elif command == 'gen':
    #         command = 1
    #     else:
    #         command = 2
    elif device == 'ats':
        device = 5
        if command == 'off':
            command = 0
        else:
            command = 1
    elif device == 'crmu':
        device = 6
        if command == 'off':
            command = 0
        else:
            command = 1
    result = struct.pack('BBBBB', 0xA0, 0x03, 0x21, device, command)
    LOGGER.info("result in _process_command")
    LOGGER.info(result)
    LOGGER.info("Get out _process_command")
    return result
