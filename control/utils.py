import struct

from config import *
from config.common import *


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
    result = ''
    value = ''

    if type(command) is bool:
        value = convert_boolean_to_string(command)
    else:
        value = command

    if device == DEVICE_MCC_1:
        device = 97
        command_int = parse_mcc_command_to_number(command)
        target = get_target_by_command_mcc(command)
        if isinstance(command_int, int) and isinstance(target, int) and target >= 0:
            result = struct.pack('BBBBBB', 0xA0, 0x04, 0x21, device, target, command_int)
        else:
            LOGGER.error('Error at device %s with command_int or target is not integer: command_int: %s, target: %s', str(device),str(command_int), str(target))
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


def parse_mcc_command_to_number(command):
    switcher_mcc_command = {
        COMMAND_MCC_CLOSE_DOOR: 0,
        COMMAND_MCC_OPEN_DOOR: 1,
        COMMAND_MCC_OFF_BELL: 0,
        COMMAND_MCC_ON_BELL: 1,
        COMMAND_MCC_OFF_LAMP: 0,
        COMMAND_MCC_ON_LAMP: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_1: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_1: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_2: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_2: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_3: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_3: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_4: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_4: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_5: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_5: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_6: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_6: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_7: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_7: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_8: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_8: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_9: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_9: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_10: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_10: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_11: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_11: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_12: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_12: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_13: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_13: 1
    }
    return switcher_mcc_command.get(command, "Out of range!")


def parse_acm_command_to_number(command):
    switcher_acm_command = {
        COMMAND_ACM_AUTO_OFF: 0,
        COMMAND_ACM_AUTO_ON: 1,
        COMMAND_ACM_AIRC_1_OFF: 0,
        COMMAND_ACM_AIRC_1_ON: 1,
        COMMAND_ACM_AIRC_2_OFF: 0,
        COMMAND_ACM_AIRC_2_ON: 1,
        COMMAND_ACM_FAN_OFF: 0,
        COMMAND_ACM_FAN_ON: 1
    }
    return switcher_acm_command.get(command, "Out of range!")


def get_target_by_command_mcc(command):
    target = -1
    try:
        is_string = isinstance(command, str)
        if is_string:
            if 'Door' in command:
                target = 0
            elif 'Lamp' in command:
                target = 1
            elif 'DoutReversed1' in command:
                target = 2
            elif 'DoutReversed2' in command:
                target = 3
            elif 'DoutReversed3' in command:
                target = 4
            elif 'DoutReversed4' in command:
                target = 5
            elif 'DoutReversed5' in command:
                target = 6
            elif 'DoutReversed6' in command:
                target = 7
            elif 'DoutReversed7' in command:
                target = 8
            elif 'DoutReversed8' in command:
                target = 9
            elif 'DoutReversed9' in command:
                target = 10
            elif 'DoutReversed10' in command:
                target = 11
            elif 'Bell' in command:
                target = 12
            elif 'DoutReversed11' in command:
                target = 13
            elif 'DoutReversed12' in command:
                target = 14
            elif 'DoutReversed13' in command:
                target = 15
        else:
            LOGGER.error('Command is not a string: %s', str(command))
    except Exception as ex:
        LOGGER.error('Error at get_target_by_command function with message: %s', ex.message)
    return target


def get_target_by_command_acm(command):
    target = -1
    try:
        is_string = isinstance(command, str)
        if is_string:
            if 'AutoAcm' in command:
                target = 0
            elif 'AcmAirc1' in command:
                target = 1
            elif 'AcmAirc2' in command:
                target = 2
            elif 'AcmFan' in command:
                target = 3
        else:
            LOGGER.error('Command is not a string: %s', str(command))
    except Exception as ex:
        LOGGER.error('Error at get_target_by_command function with message: %s', ex.message)
    return target


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
    if device == DEVICE_ACM_1 \
            and (command == COMMAND_ACM_AIRC_1_ON or
                 command == COMMAND_ACM_AIRC_1_OFF or
                 command == COMMAND_ACM_AIRC_2_ON or
                 command == COMMAND_ACM_AIRC_2_OFF or
                 command == COMMAND_ACM_FAN_OFF or
                 command == COMMAND_ACM_FAN_ON or
                 command == COMMAND_ACM_AUTO_ON or
                 command == COMMAND_ACM_AUTO_OFF):
        return True
    elif device == DEVICE_ATS_1 and (command == COMMAND_ATS_MAIN or command == COMMAND_ATS_GEN or command == COMMAND_ATS_AUTO):
        return True
    elif device == DEVICE_MCC_1 and check_exist_command_mcc(command):
        return True
    else:
        return False


def check_exist_command_mcc(command):
    list_command_mcc = [COMMAND_MCC_OPEN_DOOR, COMMAND_MCC_CLOSE_DOOR, COMMAND_MCC_ON_BELL, COMMAND_MCC_OFF_BELL,
                        COMMAND_MCC_ON_LAMP, COMMAND_MCC_OFF_LAMP, COMMAND_MCC_OFF_DOUT_REVERSED_1, COMMAND_MCC_ON_DOUT_REVERSED_1,
                        COMMAND_MCC_OFF_DOUT_REVERSED_2, COMMAND_MCC_ON_DOUT_REVERSED_2, COMMAND_MCC_OFF_DOUT_REVERSED_3, COMMAND_MCC_ON_DOUT_REVERSED_3,
                        COMMAND_MCC_OFF_DOUT_REVERSED_4, COMMAND_MCC_ON_DOUT_REVERSED_4, COMMAND_MCC_OFF_DOUT_REVERSED_5, COMMAND_MCC_ON_DOUT_REVERSED_5,
                        COMMAND_MCC_OFF_DOUT_REVERSED_6, COMMAND_MCC_ON_DOUT_REVERSED_6, COMMAND_MCC_OFF_DOUT_REVERSED_7, COMMAND_MCC_ON_DOUT_REVERSED_7,
                        COMMAND_MCC_OFF_DOUT_REVERSED_8, COMMAND_MCC_ON_DOUT_REVERSED_8, COMMAND_MCC_OFF_DOUT_REVERSED_9, COMMAND_MCC_ON_DOUT_REVERSED_9,
                        COMMAND_MCC_OFF_DOUT_REVERSED_10, COMMAND_MCC_ON_DOUT_REVERSED_10, COMMAND_MCC_OFF_DOUT_REVERSED_11, COMMAND_MCC_ON_DOUT_REVERSED_11,
                        COMMAND_MCC_OFF_DOUT_REVERSED_12, COMMAND_MCC_ON_DOUT_REVERSED_12, COMMAND_MCC_OFF_DOUT_REVERSED_13, COMMAND_MCC_ON_DOUT_REVERSED_13]
    if command in list_command_mcc:
        return True
    else:
        return False

