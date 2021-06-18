import string
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
    elif device == DEVICE_ATS_1 and (command == GET_STATE or command == GET_VALUE):
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
    try:
        if not (type(command) == str and device in [DEVICE_ATS_1, DEVICE_ACM_1]):
            return False
        value = convert_str_command_to_int(command)
        if 0 <= value <= 1:
            if device == DEVICE_ACM_1:
                shared_attributes['acmControlAuto'] = value
            elif device == DEVICE_ATS_1:
                shared_attributes['atsControlAuto'] = value
        else:
            LOGGER.info('Value: %d, value is not expected', value)
    except Exception as ex:
        LOGGER.error('Error at _process_set_auto function with message: %s', ex.message)
    return True


def _process_command(device, command):
    result = ''
    try:
        if device == DEVICE_MCC_1 or device == DEVICE_ATS_1 or device == DEVICE_ACM_1:
            result = compose_command_rpc(device, command)
        else:
            result = compose_command_lcd(device, command)
        result_encode = ':'.join(x.encode('hex') for x in result)
        LOGGER.debug('Process command: device: %s, command: %s, after decode is: %s', device, command, result_encode)
    except Exception as ex:
        LOGGER.error('Error at _process_command function with message: %s', ex.message)
    return result


def convert_str_command_to_int(command):
    _command = -1
    if command is COMMAND_ACM_AUTO_ON:
        _command = 1
    elif command is COMMAND_ACM_AUTO_OFF:
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


def compose_command_shared_attributes(module_id, value):
    result = -1
    bytes_length = -1
    prefix = ''
    length = -1
    op_code_sa = 0x41
    try:
        length_value = len(value)
        length_prefix = length_value + 5
        prefix = ''.join([char * length_prefix for char in CHAR_B])
        if module_id == ID_MCC:
            bytes_length = BYTES_SA_MCC
            length = length_value + bytes_length + 2
        elif module_id == ID_ACM:
            bytes_length = BYTES_SA_ACM
            length = length_prefix + bytes_length + 2
        elif module_id == ID_ATS:
            bytes_length = BYTES_SA_ATS
            length = length_prefix + bytes_length + 2
        if bytes_length > 0 and prefix is not '' and length > 0:
            result = struct.pack(prefix, 0xA0, length, op_code_sa, module_id, bytes_length, *value)
    except Exception as ex:
        LOGGER.error('Error at compose_command_shared_attributes function with message: %s', ex.message)
    return result


def compose_command_lcd(key_lcd, content):
    arr_char = [char for char in content]
    prefix = ''.join([char * len(arr_char) for char in CHAR_S])
    length = len(arr_char) + 3
    op_code_lcd = 0X31
    row = 0X02
    result = struct.pack(FORMAT_LCD + prefix, 0xA0, length, op_code_lcd, key_lcd, row, *arr_char)
    return result


def _process_cmd_led(length_led, arr_value):
    op_code_led = 0x33
    length_value = len(arr_value)
    length_prefix = length_value + 4
    prefix = ''.join([char * length_prefix for char in CHAR_B])
    try:
        result = struct.pack(prefix, 0xA0, length_led, op_code_led, length_led, *arr_value)
        result_encode = ':'.join(x.encode('hex') for x in result)
        LOGGER.debug('Process led command: led_id: %s, led_color: %s, after decode is: %s', length_led, arr_value, result_encode)
        return result
    except Exception as ex:
        LOGGER.error('Error at _process_cmd_led function with message: %s', ex.message)


def _process_cmd_lcd(key_lcd, content):
    try:
        result = compose_command_lcd(key_lcd, content)
        result_encode = ':'.join(x.encode('hex') for x in result)
        LOGGER.debug('Process led command: key_lcd: %s, content: %s, after decode is: %s', key_lcd, content, result_encode)
        return result
    except Exception as ex:
        LOGGER.error('Error at _process_cmd_lcd function with message: %s', ex.message)


def _process_cmd_sa(module_id, value):
    result = ''
    try:
        if module_id == ID_MCC or module_id == ID_ACM or module_id == ID_ATS:
            result = compose_command_shared_attributes(module_id, value)
            result_encode = ':'.join(x.encode('hex') for x in result)
            LOGGER.debug('Process sa command: key_name: %s, value: %s, after decode is: %s', module_id, value, result_encode)
        return result
    except Exception as ex:
        LOGGER.error('Error at _process_cmd_lcd function with message: %s', ex.message)
