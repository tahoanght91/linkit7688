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
    if device == DEVICE_MCC_1 or device == DEVICE_ATS_1 or device == DEVICE_ACM_1:
        result = compose_command_rpc(device, command)
    elif device == KEY_MCC or device == KEY_ACM or device == KEY_ATS:
        result = compose_command_shared_attributes(device, command)
    elif device == SHARED_ATTRIBUTES_RFID_CARD:
        device = 5
        result = struct.pack(FORMAT_RFID, 0xA0, 0x03, 0x24, device, command)
    LOGGER.debug('Process command: device: %s, command: %s', device, command)
    LOGGER.info('Exit _process_command function')
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


def compose_command_rpc(device, command):
    LOGGER.info('Enter compose_command_rpc function')
    result = -1
    try:
        if device == DEVICE_MCC_1:
            device = ID_MCC
            command_int = parse_mcc_command_to_number(command)
            target = get_target_by_command_mcc(command)
            if isinstance(command_int, int) and isinstance(target, int) and target >= 0:
                result = struct.pack(FORMAT_RPC, 0xA0, 0x04, 0x21, device, target, command_int)
            else:
                LOGGER.error('Error at device %s with command_int or target is not integer: command_int: %s, target: %s', str(device), str(command_int), str(target))
        elif device == DEVICE_ATS_1:
            device = ID_ATS
            command_int = parse_ats_command_to_number(command)
            target = get_target_by_command_ats(command)
            if isinstance(command_int, int) and isinstance(target, int) and target >= 0:
                result = struct.pack(FORMAT_RPC, 0xA0, 0x04, 0x21, device, target, command_int)
            else:
                LOGGER.error('Error at device %s with command_int or target is not integer: command_int: %s, target: %s', str(device), str(command_int), str(target))
        elif device == DEVICE_ACM_1:
            device = ID_ACM
            command_int = parse_acm_command_to_number(command)
            target = get_target_by_command_acm(command)
            if isinstance(command_int, int) and isinstance(target, int) and target >= 0:
                result = struct.pack(FORMAT_RPC, 0xA0, 0x04, 0x21, device, target, command_int)
            else:
                LOGGER.error('Error at device %s with command_int or target is not integer: command_int: %s, target: %s', str(device), str(command_int), str(target))
    except Exception as ex:
        LOGGER.error('Error at compose_command_rpc with message: %s', ex.message)
    if isinstance(result, str):
        byte_stream_decode = ':'.join(x.encode('hex') for x in result)
        LOGGER.info('Command send to STM32: %s', byte_stream_decode)
    else:
        LOGGER.info('Command error!')
    LOGGER.info('Exit compose_command_rpc function')
    return result


def compose_command_shared_attributes(device, command):
    LOGGER.info('Enter compose_command_shared_attributes function')
    result = -1
    try:
        length_command = get_length_command
        if device == KEY_MCC:
            device = ID_MCC
            bytes_length = BYTES_SA_MCC
            prefix = format_sa(length_command)
            length = get_length(bytes_length)
            result = struct.pack(prefix, 0xA0, length, 0x41, device, bytes_length, *command)
        elif device == KEY_ACM:
            device = ID_ACM
            bytes_length = BYTES_SA_ACM
            prefix = format_sa(length_command)
            length = get_length(bytes_length)
            result = struct.pack(prefix, 0xA0, length, 0x41, device, bytes_length, *command)
        elif device == KEY_ATS:
            device = ID_ATS
            bytes_length = BYTES_SA_ATS
            prefix = format_sa(length_command)
            length = get_length(bytes_length)
            result = struct.pack(prefix, 0xA0, length, 0x41, device, bytes_length, *command)
    except Exception as ex:
        LOGGER.error('Error at compose_command_shared_attributes function with message: %s', ex.message)
    if isinstance(result, str):
        byte_stream_decode = ':'.join(x.encode('hex') for x in result)
        LOGGER.info('Command send to STM32: %s', byte_stream_decode)
    else:
        LOGGER.info('Command error!')
    LOGGER.info('Exit compose_command_shared_attributes function')
    return result


def format_sa(length_command):
    return ''.join([char * length_command for char in CHAR_B])


def get_length_command(command):
    return len(command) + 5


def get_length(bytes_length):
    return bytes_length + 3

