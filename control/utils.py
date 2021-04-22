import struct

from config import *
from config.common import *


def _check_command(device, command):
    if device == DEVICE_AIRC_1 and (command == GET_STATE or command == GET_VALUE):
        return True
    elif device == DEVICE_AIRC_2 and (command == GET_STATE or command == GET_VALUE):
        return True
    elif device == DEVICE_MISC and (command == GET_STATE or command == GET_VALUE):
        return True
    elif device == DEVICE_ATS and (command == GET_STATE or command == GET_VALUE):
        return True
    elif device == DEVICE_CRMU and (command == GET_STATE or command == GET_VALUE):
        return True
    else:
        return False


def check_state_device(device_name, method):
    value = ''
    if device_name == DEVICE_AIRC_1 and method == GET_SATE_AIRC_1:
        # TODO: change client attributes of airc1:
        value = client_attributes.get('aircIrStatus', default_data.aircIrStatus)
    elif device_name == DEVICE_AIRC_2 and method == GET_STATE_AIRC_2:
        # TODO: change client attributes of airc2:
        value = client_attributes.get('aircIrStatus', default_data.aircIrStatus)
    elif device_name == DEVICE_MISC and method == GET_STATE_FAN:
        # TODO: change client attributes of fan (misc):
        value = client_attributes.get('miscDin0', default_data.miscDin0)
    elif device_name == DEVICE_ATS and method == GET_STATE_ATS:
        value = client_attributes.get('atsMode', default_data.atsMode)
    elif device_name == DEVICE_CRMU and method == GET_STATE_CRMU:
        # TODO: change client attributes of crmu:
        value = client_attributes.get('crmuOnlineStatus', default_data.crmuOnlineStatus)
    return value


def get_value_device(device_name, method):
    value = ''
    if device_name == DEVICE_AIRC_1 and method == GET_VALUE_AIRC_1:
        # TODO: change telemetry of airc1:
        value = telemetries.get('temp_indoor', default_data.temp_indoor)
    elif device_name == DEVICE_AIRC_2 and method == GET_VALUE_AIRC_2:
        # TODO: change telemetry of airc2:
        value = telemetries.get('temp_indoor', default_data.temp_indoor)
    # elif device_name == DEVICE_MISC and method == GET_VALUE_FAN:
    #     # TODO: change telemetry of fan (misc):
    #     value = telemetries.get('miscDin0', default_data.miscDin0)
    # elif device_name == DEVICE_ATS and method == GET_STATE_ATS:
    #     value = client_attributes.get('atsMode', default_data.atsMode)
    # elif device_name == DEVICE_CRMU and method == GET_STATE_CRMU:
    #     # TODO: change client attributes of crmu:
    #     value = client_attributes.get('crmuOnlineStatus', default_data.crmuOnlineStatus)
    return value


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
    elif device == DEVICE_AIRC_2 and (command == False or command == True or command == GET_STATE) and not shared_attributes.get('aircControlAuto', default_data.miscFanControlAuto):
        return True
    elif device == DEVICE_MISC and (command == False or command == True or command == GET_STATE) and not shared_attributes.get('miscFanControlAuto', default_data.miscFanControlAuto):
        return True
    elif device == DEVICE_ATS and (command == 'main' or command == 'gen' or command == GET_STATE) and not shared_attributes.get('atsControlAuto', default_data.atsControlAuto):
        return True
    elif device == DEVICE_CRMU and (command == False or command == True or command == GET_STATE) and not shared_attributes.get('crmuControlAuto', default_data.crmuControlAuto):
        return True
    else:
        return False
