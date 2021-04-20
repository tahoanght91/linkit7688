import struct

from config import *
from config.common import *


def _check_command(device, command):
    if device == DEVICE_AIRC and (command == False or command == True or command == GET_STATE) and not shared_attributes.get('aircControlAuto', default_data.aircControlAuto):
        return True
    elif device == DEVICE_MISC and (command == False or command == True or command == GET_STATE) and not shared_attributes.get('miscFanControlAuto', default_data.miscFanControlAuto):
        return True
    elif device == DEVICE_ATS and (command == False or command == True or command == GET_STATE) and not shared_attributes.get('atsControlAuto', default_data.atsControlAuto):
        return True
    elif device == DEVICE_CRMU and (command == False or command == True or command == GET_STATE) and not shared_attributes.get('crmuControlAuto', default_data.crmuControlAuto):
        return True
    else:
        return False


def _process_set_auto(device, command):
    if not (type(command) == bool
            and
            (device == DEVICE_MISC
             or device == DEVICE_AIRC
             or device == DEVICE_ATS
             or device == DEVICE_CRMU)):
        return False

    value = convert_boolean_to_int(command)

    if device == DEVICE_AIRC:
        shared_attributes['aircControlAuto'] = value
    elif device == DEVICE_MISC:
        shared_attributes['miscFanControlAuto'] = value
    elif device == DEVICE_ATS:
        shared_attributes['atsControlAuto'] = value
    elif device == DEVICE_CRMU:
        shared_attributes['crmuControlAuto'] = value
    return True


def _process_command(device, command):
    value = ''

    if type(command) is bool:
        value = convert_boolean_to_string(command)
    else:
        value = command

    if device == 'bell':
        device = 1
        if command == 'off':
            command = 0
        else:
            command = 1
    elif device == DEVICE_MISC:
        device = 2
        if value == 'off':
            command = 0
        else:
            command = 1
    elif device == DEVICE_AIRC_1:
        device = 3
        if value == 'off':
            command = 0
        elif value == 'on':
            command = 1
    elif device == DEVICE_AIRC_2:
        device = 4
        if value == 'off':
            command = 0
        elif value == 'on':
            command = 1
    elif device == DEVICE_ATS:
        device = 5
        if value == 'main':
            command = 0
        elif value == 'gen':
            command = 1
        elif value == 'auto':
            command = 2
    elif device == DEVICE_CRMU:
        device = 6
        if value == 'off':
            command = 0
        else:
            command = 1
    LOGGER.debug('Process command: device: %s, command: %s', device, command)
    result = struct.pack('BBBBB', 0xA0, 0x03, 0x21, device, command)
    return result


def convert_boolean_to_string(command):
    if command:
        _command = 'on'
    else:
        _command = 'off'

    return _command


def convert_boolean_to_int(command):
    if command:
        _command = 1
    else:
        _command = 0

    return _command


def _check_command_send_rpc(device, command):
    if device == DEVICE_AIRC_1 and (command == False or command == True or command == GET_STATE) and not shared_attributes.get('aircControlAuto', default_data.aircControlAuto):
        return True
    elif device == DEVICE_AIRC_2 and (command == False or command == True or command == GET_STATE) and not shared_attributes.get('miscFanControlAuto', default_data.miscFanControlAuto):
        return True
    elif device == DEVICE_MISC and (command == False or command == True or command == GET_STATE) and not shared_attributes.get('miscFanControlAuto', default_data.miscFanControlAuto):
        return True
    elif device == DEVICE_ATS and (command == 'main' or command == 'gen' or command == GET_STATE) and not shared_attributes.get('atsControlAuto', default_data.atsControlAuto):
        return True
    elif device == DEVICE_CRMU and (command == False or command == True or command == GET_STATE) and not shared_attributes.get('crmuControlAuto', default_data.crmuControlAuto):
        return True
    else:
        return False
