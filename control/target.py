from config import LOGGER


def get_target_by_command_mcc(command):
    LOGGER.info('Enter get_target_by_command_mcc function')
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
    LOGGER.info('Command is: %s, after parse is: %d', command, target)
    LOGGER.info('Exit get_target_by_command function')
    return target


def get_target_by_command_acm(command):
    LOGGER.info('Enter get_target_by_command_acm function')
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
            elif 'SelfPropelledAcm' in command:
                target = 4
        else:
            LOGGER.error('Command is not a string: %s', str(command))
    except Exception as ex:
        LOGGER.error('Error at get_target_by_command function with message: %s', ex.message)
    LOGGER.info('Command is: %s, after parse is: %d', command, target)
    LOGGER.info('Exit get_target_by_command function')
    return target

