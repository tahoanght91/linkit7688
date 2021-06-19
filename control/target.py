from config import LOGGER


def get_target_by_command_mcc(command):
    target = -1
    try:
        if 'DoorMcc' in command:
            target = 15
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
        elif 'BellMcc' in command:
            target = 12
        elif 'DoutReversed11Mcc' in command:
            target = 13
        elif 'DoutReversed12Mcc' in command:
            target = 14
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
        if 'MainAts' in command or 'AutoAts' in command or 'GenAts' in command or 'Ats' in command:
            target = 0
        else:
            LOGGER.error('Command is not a string: %s', str(command))
    except Exception as ex:
        LOGGER.error('Error at get_target_by_command_ats function with message: %s', ex.message)
    LOGGER.info('Command is: %s, after parse is: %d', command, target)
    return target

