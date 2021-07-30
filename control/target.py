from config import LOGGER
from config.common_command import *


def get_target_by_command_mcc(command):
    target = -1
    try:
        if 'DoorMcc' in command:
            target = 13
        elif 'BellMcc' in command:
            target = 12
        elif 'VmbMcc' in command:
            target = 15
        elif 'CamMcc' in command:
            target = 14
        elif 'VsensMcc' in command:
            target = 16
        elif 'LampMcc' in command:
            target = 1
        elif 'DoutReversed1Mcc' in command:
            target = 2
        elif 'DoutReversed2Mcc' in command:
            target = 3
        elif 'DoutReversed3Mcc' in command:
            target = 4
        elif 'DoutReversed4Mcc' in command:
            target = 5
        elif 'DoutReversed5Mcc' in command:
            target = 6
        elif 'DoutReversed6Mcc' in command:
            target = 7
        elif 'DoutReversed7Mcc' in command:
            target = 8
        elif 'DoutReversed8Mcc' in command:
            target = 9
        elif 'DoutReversed9Mcc' in command:
            target = 10
        elif 'DoutReversed10Mcc' in command:
            target = 11
        elif 'DoutReversed13Mcc' in command:
            target = 0
        else:
            LOGGER.error('Command is not a string: %s', str(command))
    except Exception as ex:
        LOGGER.error('Error at get_target_by_command function with message: %s', ex.message)
    LOGGER.info('Command is: %s, after parse is: %d', command, target)
    return target


def get_target_by_command_acm(command):
    target = -1
    try:
        if 'AutoAcm' in command:
            target = 0
        elif 'Airc1Acm' in command:
            target = 1
        elif 'Airc2Acm' in command:
            target = 2
        elif 'FanAcm' in command:
            target = 3
        elif 'SelfPropelledAcm' in command:
            target = 4
        else:
            LOGGER.error('Command is not a string: %s', str(command))
    except Exception as ex:
        LOGGER.error('Error at get_target_by_command function with message: %s', ex.message)
    LOGGER.info('Command is: %s, after parse is: %d', command, target)
    return target


def get_target_by_command_ats(command):
    target = -1
    try:
        if COMMAND_ATS_MAIN_ON in command or COMMAND_ATS_AUTO_ON in command or COMMAND_ATS_GEN_ON in command or COMMAND_ATS_OFF in command:
            target = 0
        elif COMMAND_ATS_STOP_GEN in command or COMMAND_ATS_START_GEN in command:
            target = 1
        else:
            LOGGER.error('Command is not a string: %s', str(command))
    except Exception as ex:
        LOGGER.error('Error at get_target_by_command_ats function with message: %s', ex.message)
    LOGGER.info('Command is: %s, after parse is: %d', command, target)
    return target

