import struct

from config import *
from config.common import *
from config.common_led import LIST_LED
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
    LOGGER.info('Enter check_state_device function')
    value = -1
    try:
        if device_name == DEVICE_MCC_1:
            value = get_state_mcc(method)
        elif device_name == DEVICE_ACM_1:
            value = get_state_acm(method)
        elif device_name == DEVICE_ATS_1:
            value = get_state_ats(method)

        if 0 <= value <= 1:
            LOGGER.info('The state of device %s with method %s is: %d', device_name, method, value)
        else:
            LOGGER.info('Status is %d, not as expected', value)
    except Exception as ex:
        LOGGER.error('Error at check_state_device function with message: %s', ex.message)
    LOGGER.info('Exit check_state_device function')
    return value


def get_state_ats(method):
    LOGGER.info('Enter get_state_ats function')
    value = -1
    try:
        if method == GET_STATE_ATS:
            value = client_attributes.get('atsMode', default_data.atsMode)
    except Exception as ex:
        LOGGER.error('Error at get_state_ats function with message: %s', ex.message)
    LOGGER.info('Exit get_state_ats function')
    return value


def get_state_acm(method):
    LOGGER.info('Enter get_state_acm function')
    value = -1
    try:
        if method == GET_STATE_ACM_AUTO:
            value = shared_attributes.get('acmControlAuto', default_data.acmControlAuto)
        elif method == GET_SATE_ACM_AIRC_1:
            value = client_attributes.get('acmAirc1RunState', default_data.acmAirc1RunState)
        elif method == GET_STATE_ACM_AIRC_2:
            value = client_attributes.get('acmAirc2RunState', default_data.acmAirc2RunState)
        elif method == GET_STATE_ACM_FAN:
            value = client_attributes.get('acmFanRunState', default_data.acmFanRunState)
        elif method == GET_SATE_ACM_SELF_PROPELLED:
            value = 0 # TODO: change client attributes of lamp
    except Exception as ex:
        LOGGER.error('Error at get_state_acm function with message: %s', ex.message)
    LOGGER.info('Exit get_state_acm function')
    return value


def get_state_mcc(method):
    LOGGER.info('Enter get_state_mcc function')
    value = -1
    try:
        if method == GET_STATE_MCC_DOOR:
            value = client_attributes.get('mccDoorState', default_data.mccDoorState)
        elif method == GET_STATE_MCC_LAMP:
            value = 0  # TODO: change client attributes of lamp
        elif method == GET_STATE_MCC_BELL:
            value = client_attributes.get('mccBellState', default_data.mccBellState)
    except Exception as ex:
        LOGGER.error('Error at get_state_mcc function with message: %s', ex.message)
    LOGGER.info('Exit get_sate_mcc function')
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


def _process_set_auto(device, command):
    LOGGER.info('Enter _process_set_auto function')
    try:
        if not (type(command) == str and device in [DEVICE_ATS_1, DEVICE_ACM_1]):
            return False
        value = convert_str_command_to_int(command)
        if value >= 0:
            if device == DEVICE_ATS_1:
                shared_attributes['atsControlAuto'] = value
            elif device == DEVICE_ACM_1:
                shared_attributes['acmControlAuto'] = value
        else:
            LOGGER.info('Value: %d, value is not expected', value)
    except Exception as ex:
        LOGGER.error('Error at _process_set_auto function with message: %s', ex.message)
    LOGGER.info('Exit _process_set_auto function')
    return True


def _process_command(device, command):
    LOGGER.info('Enter _process_command function')
    result = ''
    if device == DEVICE_MCC_1 or device == DEVICE_ATS_1 or device == DEVICE_ACM_1:
        result = compose_command_rpc(device, command)
    elif device == KEY_MCC or device == KEY_ACM or device == KEY_ATS:
        result = compose_command_shared_attributes(device, command)
    elif device == LCD_SERVICE:
        row = 2
        length = 19
        lcd_command = 0
        result = struct.pack(FORMAT_LCD, 0xA0, length, 0x31, lcd_command, row, command)
    elif device in LIST_LED:
        result = struct.pack(FORMAT_LED, 0xA0, 0x03, 0x33, device, command)
    LOGGER.debug('Process command: device: %s, command: %s', device, command)
    LOGGER.info('Exit _process_command function')
    return result


def convert_str_command_to_int(command):
    _command = -1
    if command is COMMAND_ACM_AUTO_ON:
        _command = 1
    elif command is COMMAND_ACM_AUTO_OFF:
        _command = 0
    elif command is COMMAND_ATS_SELF_PROPELLED_OFF:
        _command = 0
    elif command is COMMAND_ATS_SELF_PROPELLED_ON:
        _command = 1
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
        length_command = get_length_command(command)
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
        LOGGER.info('Device: %s, command send to STM32: %s', device, byte_stream_decode)
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

