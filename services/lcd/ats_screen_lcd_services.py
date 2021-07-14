from config import *
from config.common import UPDATE_VALUE
from config.common_lcd_services import *


def get_title_ats():
    from control import process_cmd_lcd
    try:
        show = 'THONG TIN ATS'
        process_cmd_lcd(ROW_1, UPDATE_VALUE, show)
    except Exception as ex:
        LOGGER.error('Error at get_title_ats function with message: %s', ex.message)


def get_info_ats():
    from control import process_cmd_lcd
    try:
        row2 = 'Ket noi' if client_attributes.get('atsConnect') > 0 else 'Mat ket noi'
        row3 = 'Nguon: May phat' if client_attributes.get('atsContactorGenState') > 0 else 'Nguon: Dien luoi'
        row4 = 'Che do: ' + str(telemetries.get('atsState', default=''))
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
        LOGGER.info('ATS SCREEN : %s', 1)
    except Exception as ex:
        LOGGER.error('Error at get_info_ats function with message: %s', ex.message)


def get_detail_screen1_ats():
    from control import process_cmd_lcd
    try:
        row2 = 'Dien luoi: ' + str(telemetries.get('atsAcState', default=''))
        row3 = 'May phat: ' + str(telemetries.get('atsGenState', default=''))
        row4 = 'Che do M.Phat: ' + str(telemetries.get('atsState', default=''))
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
        LOGGER.info('ATS SCREEN : %s', 2)
    except Exception as ex:
        LOGGER.error('Error at get_detail_ats function with message: %s', ex.message)


def get_detail_screen2_ats():
    from control import process_cmd_lcd
    try:
        row2 = telemetries.get('atsVacP1', default=0) + 'V ' + telemetries.get('atsVacP2',
                                                                               default=0) + 'V ' + telemetries.get(
            'atsVacP3', default=0) + 'V'
        row3 = telemetries.get('atsVgenP1', default=0) + 'V ' + telemetries.get('atsVgenP2',
                                                                                default=0) + 'V ' + telemetries.get(
            'atsVgenP3', default=0) + 'V'
        row4 = telemetries.get('atsVloadP1', default=0) + 'V ' + telemetries.get('atsVloadP2',
                                                                                 default=0) + 'V ' + telemetries.get(
            'atsVloadP3', default=0) + 'V'
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
        LOGGER.info('ATS SCREEN : %s', 3)
    except Exception as ex:
        LOGGER.error('Error at get_detail_screen2_ats function with message: %s', ex.message)


def get_detail_screen3_ats():
    from control import process_cmd_lcd
    try:
        row2 = telemetries.get('atsIloadP1', default=0) + 'A ' + telemetries.get('atsIloadP2',
                                                                                 default=0) + 'A ' + telemetries.get(
            'atsIloadP3', default=0) + 'A'
        row3 = telemetries.get('atsPac1', default=0) + 'W ' + telemetries.get('atsPac2',
                                                                              default=0) + 'W ' + telemetries.get(
            'atsPac3', default=0) + 'W'

        row4 = telemetries.get('atsVacFreq', default=0) + 'Hz ' + telemetries.get('atsVgenFreq',
                                                                                  default=0) + 'Hz ' + telemetries.get(
            'atsVloadFreq', default=0) + 'Hz'
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
        LOGGER.info('ATS SCREEN : %s', 4)
    except Exception as ex:
        LOGGER.error('Error at get_detail_screen3_ats function with message: %s', ex.message)


def get_detail_screen4_ats():
    from control import process_cmd_lcd
    try:
        row2 = telemetries.get('mccDcBat1Temp', default=0) + 'C ' + telemetries.get('mccDcBat2Temp',
                                                                                    default=0) + 'C ' + telemetries.get(
            'mccDcBat3Temp', default=0) + 'C'
        row3 = telemetries.get('mccDcV1', default=0) + 'V ' + telemetries.get('mccDcI1',
                                                                              default=0) + 'A ' + telemetries.get(
            'mccDcP1', default=0) + 'W'
        row4 = telemetries.get('mccDcV2', default=0) + 'V ' + telemetries.get('mccDcI2',
                                                                              default=0) + 'A ' + telemetries.get(
            'mccDcP2', default=0) + 'W'
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
        LOGGER.info('ATS SCREEN : %s', 5)
    except Exception as ex:
        LOGGER.error('Error at get_detail_screen4_ats function with message: %s', ex.message)


def get_detail_screen5_ats():
    from control import process_cmd_lcd
    try:
        row2 = telemetries.get('mccDcV3', default=0) + 'V ' + telemetries.get('mccDcI3',
                                                                              default=0) + 'A ' + telemetries.get(
            'mccDcP3', default=0) + 'W'
        row3 = telemetries.get('mccDcV4', default=0) + 'V ' + telemetries.get('mccDcI4',
                                                                              default=0) + 'A ' + telemetries.get(
            'mccDcP4', default=0) + 'W'
        row4 = telemetries.get('mccDcV5', default=0) + 'V ' + telemetries.get('mccDcI5',
                                                                              default=0) + 'A ' + telemetries.get(
            'mccDcP5', default=0) + 'W'
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
        LOGGER.info('ATS SCREEN : %s', 6)
    except Exception as ex:
        LOGGER.error('Error at get_detail_screen5_ats function with message: %s', ex.message)


def get_screen_ats():
    try:
        get_title_ats()
        get_info_ats()
    except Exception as ex:
        LOGGER.error('Error at get_screen_ats function with message: %s', ex.message)
