from config import LOGGER
from config.common_command import *


# Command MCC
def parse_mcc_command_to_number(command):
    LOGGER.info('Enter parse_mcc_command_to_number function')
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
    LOGGER.info('Command is: %s, after parse is: %d', command, switcher_mcc_command.get(command))
    LOGGER.info('Exit parse_mcc_command_to_number function')
    return switcher_mcc_command.get(command, "Out of range!")


# ACM
def parse_acm_command_to_number(command):
    LOGGER.info('Enter parse_acm_command_to_number function')
    switcher_acm_command = {
        COMMAND_ACM_AUTO_OFF: 0,
        COMMAND_ACM_AUTO_ON: 1,
        COMMAND_ACM_AIRC_1_OFF: 0,
        COMMAND_ACM_AIRC_1_ON: 1,
        COMMAND_ACM_AIRC_2_OFF: 0,
        COMMAND_ACM_AIRC_2_ON: 1,
        COMMAND_ACM_FAN_OFF: 0,
        COMMAND_ACM_FAN_ON: 1,
        COMMAND_ACM_SELF_PROPELLED_OFF: 0,
        COMMAND_ACM_SELF_PROPELLED_ON: 1
    }
    LOGGER.info('Command is: %s, after parse is: %d', command, switcher_acm_command.get(command))
    LOGGER.info('Exit parse_acm_command_to_number function')
    return switcher_acm_command.get(command, "Out of range!")

