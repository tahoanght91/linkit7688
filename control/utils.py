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
        if value == COMMAND_MCC_OFF_BELL:
            command = 0
        elif value == COMMAND_MCC_ON_BELL:
            command = 1
        elif value == COMMAND_MCC_OFF_LAMP:
            command = 2
        elif value == COMMAND_MCC_ON_LAMP:
            command = 3
        elif value == COMMAND_MCC_OPEN_DOOR:
            command = 4
        elif value == COMMAND_MCC_CLOSE_DOOR:
            command = 5
        else:
            command = value
        result = struct.pack('BBBBB', 0xA0, 0x03, 0x21, device, command)
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
        if value == COMMAND_ACM_AUTO_OFF:
            command = 0
        elif value == COMMAND_ACM_AUTO_ON:
            command = 1
        elif value == COMMAND_ACM_AIRC_1_OFF:
            command = 2
        elif value == COMMAND_ACM_AIRC_1_ON:
            command = 3
        elif value == COMMAND_ACM_AIRC_2_OFF:
            command = 4
        elif value == COMMAND_ACM_AIRC_2_ON:
            command = 5
        elif value == COMMAND_ACM_FAN_OFF:
            command = 6
        elif value == COMMAND_ACM_FAN_ON:
            command = 7
        else:
            command = value
        result = struct.pack('BBBBB', 0xA0, 0x03, 0x21, device, command)
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


def classify_shared_attributes(key, value):
    formatted = {}
    number = 0
    if 'ats' in key:
        number = parse_ats_shared_attributes_to_number(key)
    elif 'mcc' in key:
        number = parse_mcc_shared_attributes_to_number(key)
    elif 'acm' in key:
        number = parse_acm_shared_attributes_to_number(key)
    formatted = {'idSharedAttributes': number, 'value': value}
    return formatted


def parse_ats_shared_attributes_to_number(key):
    switcher_ats = {
        'atsVacMaxThreshold': 1,
        'atsVdcThreshold': 2,
        'atsVacMinThreshold': 3,
        'atsVgenMaxThreshold': 4,
        'atsVgenMinThreshold': 5,
        'atsVacStabilizeTimeout': 6,
        'atsVgenIdleCoolingTimeout': 7,
        'atsVgenIdleWarmUpTimeout': 8,
        'atsGenInactiveStartTime': 9,
        'atsGenInactiveEndTime': 10,
        'atsGenActiveDuration': 11
    }
    return switcher_ats.get(key, "Out of range!")


def parse_mcc_shared_attributes_to_number(key):
    switcher_mcc = {
        'mccPeriodReadDataIO': 1,
        'mccPeriodSendTelemetry': 2,
        'mccPeriodUpdate': 3,
        'mccPeriodSendShared': 4,
        'mccListRfid': 6,
        'mccDcMinThreshold': 7
    }
    return switcher_mcc.get(key, "Out of range!")


def parse_acm_shared_attributes_to_number(key):
    switcher_acm = {
        'acmAlternativeState': 1,
        'acmAlternativeTime': 2,
        'acmRunTime': 3,
        'acmRestTime': 4,
        'acmGenAllow': 5,
        'acmVacThreshold': 6,
        'acmMinTemp': 7,
        'acmMaxTemp': 8,
        'acmMinHumid': 9,
        'acmMaxHumid': 10,
        'acmExpectedTemp': 11,
        'acmExpectedHumid': 12
    }
    return switcher_acm.get(key, "Out of range!")


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
    elif device == DEVICE_ATS_1 and (
            command == COMMAND_ATS_MAIN or command == COMMAND_ATS_GEN or command == COMMAND_ATS_AUTO):
        return True
    elif device == DEVICE_MCC_1 \
            and (command == COMMAND_MCC_OPEN_DOOR or
                 command == COMMAND_MCC_CLOSE_DOOR or
                 command == COMMAND_MCC_ON_BELL or
                 command == COMMAND_MCC_OFF_BELL or
                 command == COMMAND_MCC_ON_LAMP or
                 command == COMMAND_MCC_OFF_LAMP or
                 command == COMMAND_MCC_ON_ERROR or
                 command == COMMAND_MCC_OFF_ERROR):
        return True
    else:
        return False
