import struct

from config import *
from config.common import *
from config.common_method import *
from control.switcher import *
from control.target import *


def _check_command(device, command):
    if device == DEVICE_MCC_1 and (command == GET_STATE or command == GET_VALUE):
        return True
    elif device == DEVICE_ACM_1 and (command == GET_STATE or command == GET_VALUE):
        return True
    elif device == DEVICE_ATS and (command == GET_STATE or command == GET_VALUE):
        return True
    else:
        return False


def check_state_device(device_name, method):
    value = ''
    if device_name == DEVICE_MCC_1 and method == GET_SATE_ACM_AIRC_1:
        # TODO: change client attributes of airc1:
        value = client_attributes.get('acmAirc1RunState', default_data.acmAirc1RunState)
    elif device_name == DEVICE_ACM_1 and method == GET_STATE_ACM_AIRC_2:
        # TODO: change client attributes of airc2:
        value = client_attributes.get('acmAirc2RunState', default_data.acmAirc2RunState)
    elif device_name == DEVICE_ACM_1 and method == GET_STATE_ACM_FAN:
        # TODO: change client attributes of fan:
        value = client_attributes.get('acmFanRunState', default_data.acmFanRunState)
    return value


def get_value_device(device_name, method):
    value = ''
    if device_name == DEVICE_ACM_1 and method == GET_VALUE_ACM_AIRC_1:
        # TODO: change telemetry of airc1:
        value = telemetries.get('acmTempIndoor', default_data.acmTempIndoor)
    elif device_name == DEVICE_ACM_1 and method == GET_VALUE_ACM_AIRC_2:
        # TODO: change telemetry of airc2:
        value = telemetries.get('acmTempOutdoor', default_data.acmTempOutdoor)
    elif device_name == DEVICE_MCC_1 and method == GET_STATE_MCC_DOOR:
        # TODO: change telemetry of airc2:
        value = telemetries.get('mccDoorState', default_data.mccDoorState)
    return value


# def _process_set_auto(device, command):
#     if not (type(command) == bool
#             and
#             (device == DEVICE_MISC
#              or device == DEVICE_AIRC_1
#              or device == DEVICE_AIRC_2
#              or device == DEVICE_ATS
#              or device == DEVICE_CRMU
#              or device == DEVICE_MCC_1
#              or device == DEVICE_ATS_1
#              or device == DEVICE_ACM_1)):
#         return False
#
#     value = convert_boolean_to_int(command)
#
#     if device == DEVICE_AIRC_1:
#         shared_attributes['aircControlAuto'] = value
#     elif device == DEVICE_AIRC_2:
#         shared_attributes['aircControlAuto'] = value
#     elif device == DEVICE_MISC:
#         shared_attributes['miscFanControlAuto'] = value
#     elif device == DEVICE_ATS:
#         shared_attributes['atsControlAuto'] = value
#     elif device == DEVICE_CRMU:
#         shared_attributes['crmuControlAuto'] = value
#     elif device == DEVICE_MCC_1:
#         shared_attributes['miscFanControlAuto'] = value
#     elif device == DEVICE_ATS_1:
#         shared_attributes['atsControlAuto'] = value
#     elif device == DEVICE_ACM_1:
#         shared_attributes['aircControlAuto'] = value
#     return True


def _process_command(device, command):
    LOGGER.info('Enter _process_command function')
    result = ''
    value = ''

    if device == DEVICE_MCC_1:
        device = 97
        command_int = parse_mcc_command_to_number(command)
        target = get_target_by_command_mcc(command)
        if isinstance(command_int, int) and isinstance(target, int) and target >= 0:
            result = struct.pack('BBBBBB', 0xA0, 0x04, 0x21, device, target, command_int)
        else:
            LOGGER.error('Error at device %s with command_int or target is not integer: command_int: %s, target: %s', str(device), str(command_int), str(target))
    elif device == DEVICE_ATS_1:
        device = 98
        if value == COMMAND_ATS_MAIN:
            command = 0
        elif value == COMMAND_ATS_GEN:
            command = 1
        elif value == COMMAND_ATS_AUTO:
            command = 2
        result = struct.pack('BBBBB', 0xA0, 0x03, 0x21, device, command)
    elif device == DEVICE_ACM_1:
        device = 99
        command_int = parse_acm_command_to_number(command)
        target = get_target_by_command_acm(command)
        if isinstance(command_int, int) and isinstance(target, int) and target >= 0:
            result = struct.pack('BBBBBB', 0xA0, 0x04, 0x21, device, target, command_int)
        else:
            LOGGER.error('Error at device %s with command_int or target is not integer: command_int: %s, target: %s', str(device),str(command_int), str(target))
    elif device == SHARED_ATTRIBUTES_RFID_CARD:
        device = 5
        result = struct.pack('BBBBB', 0xA0, 0x03, 0x24, device, command)
    elif device == ALL_SHARED_ATTRIBUTES:
        device = 1
        length_command = len(command) + 4
        prefix = '<' + str(length_command) + 'Q'
        result = struct.pack(prefix, 0xA0, 0x03, 0x25, device, *command)
    # else:
    #     response_classify = classify_shared_attributes(device, command)
    #     id_shared_attributes = response_classify['idSharedAttributes']
    #     if 'ats' in device and type(id_shared_attributes) is int:
    #         result = struct.pack('BBBBB', 0xA0, 0x03, 0x22, id_shared_attributes, command)
    #     elif 'acm' in device and type(id_shared_attributes) is int:
    #         result = struct.pack('BBBBB', 0xA0, 0x03, 0x23, id_shared_attributes, command)
    #     elif 'mcc' in device and type(id_shared_attributes) is int:
    #         result = struct.pack('BBBBB', 0xA0, 0x03, 0x24, id_shared_attributes, command)

    LOGGER.debug('Process command: device: %s, command: %s', device, command)
    return result


def convert_boolean_to_int(command):
    if command:
        _command = 1
    else:
        _command = 0

    return _command


def _check_command_send_rpc(device, command):
    LOGGER.info('Enter _check_command_send_rpc function')
    result = False
    try:
        if device == DEVICE_ACM_1 and check_exist_command(command):
            result = True
        elif device == DEVICE_ATS_1 and check_exist_command(command):
            result = True
        elif device == DEVICE_MCC_1 and check_exist_command(command):
            result = True
    except Exception as ex:
        LOGGER.error('Error at _check_command_send_rpc function with message: %s', ex.message)
    LOGGER.info('Result of check command is: %s', result)
    LOGGER.info('Exit _check_command_send_rpc function')
    return result


def check_exist_command(command):
    LOGGER.info('Enter check_exist_command function')
    result = False
    try:
        if command in list_command:
            result = True
    except Exception as ex:
        LOGGER.error('Error at check_exist_command function with message: %s', ex.message)
    LOGGER.info('Result of check existence is: %s', result)
    LOGGER.info('Exit check_exist_command function')
    return result

