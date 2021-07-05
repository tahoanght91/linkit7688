from config.common import UPDATE_VALUE, END_CMD, CLEAR
from config import *
from config.common_lcd_services import *


def print_lcd(row1, row2, row3, row4):
    try:
        LOGGER.info('Send message print on lcd')
        # cmd_lcd[UPDATE_VALUE] = str(row1) + SALT_DOLLAR_SIGN + str(ROW_1) + END_CMD \
        #                         + str(row2) + SALT_DOLLAR_SIGN + str(ROW_2) + END_CMD
        cmd_lcd[UPDATE_VALUE] = str(row1) + SALT_DOLLAR_SIGN + str(ROW_1) + END_CMD \
                                + str(row2) + SALT_DOLLAR_SIGN + str(ROW_2) + END_CMD \
                                + str(row3) + SALT_DOLLAR_SIGN + str(ROW_3) + END_CMD \
                                + str(row4) + SALT_DOLLAR_SIGN + str(ROW_4) + END_CMD
        LOGGER.info('Send message print on lcd: %s', str(cmd_lcd[UPDATE_VALUE]))
    except Exception as ex:
        LOGGER.info('print_lcd function error: %s', ex.message)


def clear_display():
    cmd_lcd[CLEAR] = ''
