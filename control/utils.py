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
        value = client_attributes.get('aircAirc1Command', default_data.aircAirc1Command)
    elif device_name == DEVICE_AIRC_2 and method == GET_STATE_AIRC_2:
        # TODO: change client attributes of airc2:
        value = client_attributes.get('aircAirc2Command', default_data.aircAirc2Command)
    elif device_name == DEVICE_MISC and method == GET_STATE_FAN:
        # TODO: change client attributes of fan (misc):
        value = client_attributes.get('aircFanCommand', default_data.aircFanCommand)
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
        value = telemetries.get('aircTempIndoor', default_data.aircTempIndoor)
    elif device_name == DEVICE_AIRC_2 and method == GET_VALUE_AIRC_2:
        # TODO: change telemetry of airc2:
        value = telemetries.get('aircTempIndoor', default_data.aircTempIndoor)
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
             or device == DEVICE_AIRC_1
             or device == DEVICE_AIRC_2
             or device == DEVICE_ATS
             or device == DEVICE_CRMU
             or device == DEVICE_MCC_1
             or device == DEVICE_ATS_1
             or device == DEVICE_ACM_1)):
        return False

    value = convert_boolean_to_int(command)

    if device == DEVICE_AIRC_1:
        shared_attributes['aircControlAuto'] = value
    elif device == DEVICE_AIRC_2:
        shared_attributes['aircControlAuto'] = value
    elif device == DEVICE_MISC:
        shared_attributes['miscFanControlAuto'] = value
    elif device == DEVICE_ATS:
        shared_attributes['atsControlAuto'] = value
    elif device == DEVICE_CRMU:
        shared_attributes['crmuControlAuto'] = value
    elif device == DEVICE_MCC_1:
        shared_attributes['miscFanControlAuto'] = value
    elif device == DEVICE_ATS_1:
        shared_attributes['atsControlAuto'] = value
    elif device == DEVICE_ACM_1:
        shared_attributes['aircControlAuto'] = value
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
    elif device == DEVICE_MCC_1:
        device = 7
        if value == COMMAND_MCC_CLOSE_DOOR:
            command = 0
        elif value == COMMAND_MCC_OPEN_DOOR:
            command = 1
        elif value == COMMAND_MCC_OFF_BELL:
            command = 2
        elif value == COMMAND_MCC_ON_BELL:
            command = 3
        elif value == COMMAND_MCC_OFF_LAMP:
            command = 4
        elif value == COMMAND_MCC_ON_LAMP:
            command = 5
        elif value == COMMAND_MCC_OFF_ERROR:
            command = 6
        elif value == COMMAND_MCC_ON_ERROR:
            command = 7
        else:
            command = value
    elif device == DEVICE_ATS_1:
        device = 8
        if value == COMMAND_ATS_MAIN:
            command = 0
        elif value == COMMAND_ATS_GEN:
            command = 1
        elif value == 'auto':
            command = 2
    elif device == DEVICE_ACM_1:
        device = 9
        if value == COMMAND_AIRC_1_OFF:
            command = 0
        elif value == COMMAND_AIRC_1_ON:
            command = 1
        elif value == COMMAND_AIRC_2_OFF:
            command = 2
        elif value == COMMAND_AIRC_2_ON:
            command = 3
        elif value == COMMAND_FAN_OFF:
            command = 4
        elif value == COMMAND_FAN_ON:
            command = 5
        else:
            command = value
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
    if device == DEVICE_AIRC_1 \
            and (command == 'off' or command == 'on') \
            and not shared_attributes.get('aircControlAuto', default_data.aircControlAuto):
        return True
    elif device == 'bell' and (command == 'off' or command == 'on'):
        return True
    elif device == DEVICE_AIRC_2 \
            and (command == 'off' or command == 'on') \
            and not shared_attributes.get('aircControlAuto', default_data.aircControlAuto):
        return True
    elif device == DEVICE_MISC \
            and (command == 'off' or command == 'on') \
            and not shared_attributes.get('miscFanControlAuto', default_data.miscFanControlAuto):
        return True
    elif device == DEVICE_ATS \
            and (command == 'main' or command == 'gen') \
            and not shared_attributes.get('atsControlAuto', default_data.atsControlAuto):
        return True
    elif device == DEVICE_CRMU \
            and (command == 'off' or command == 'on') \
            and not shared_attributes.get('crmuControlAuto', default_data.crmuControlAuto):
        return True
    elif device == DEVICE_ACM_1 \
            and (command == COMMAND_AIRC_1_ON or
                 command == COMMAND_AIRC_1_OFF or
                 command == COMMAND_AIRC_2_ON or
                 command == COMMAND_AIRC_2_OFF or
                 command == COMMAND_FAN_OFF or
                 command == COMMAND_FAN_ON) \
            and not shared_attributes.get('aircControlAuto', default_data.aircControlAuto):
        return True
    elif device == DEVICE_ATS_1 \
            and (command == COMMAND_ATS_MAIN or
                 command == COMMAND_ATS_GEN) \
            and not shared_attributes.get('atsControlAuto', default_data.atsControlAuto):
        return True
    # TODO: edit shared attributes
    elif device == DEVICE_MCC_1 \
            and (command == COMMAND_MCC_OPEN_DOOR or
                                     command == COMMAND_MCC_CLOSE_DOOR or
                                     command == COMMAND_MCC_ON_BELL or
                                     command == COMMAND_MCC_OFF_BELL or
                                     command == COMMAND_MCC_ON_LAMP or
                                     command == COMMAND_MCC_OFF_LAMP or
                                     command == COMMAND_MCC_ON_ERROR or
                                     command == COMMAND_MCC_OFF_ERROR)\
            and not shared_attributes.get('miscFanControlAuto', default_data.miscFanControlAuto):
        return True
    else:
        return False
