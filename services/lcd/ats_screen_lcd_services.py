from config import *
from config.common import UPDATE_VALUE
from config.common_lcd_services import *

last_cmd_lcd = './last_cmd_screen.json'


def get_title_ats(row1):
    from control import process_cmd_lcd
    try:
        show = 'THONG TIN ATS'
        if row1 != show:
            process_cmd_lcd(ROW_1, UPDATE_VALUE, show)
            row1 = show
    except Exception as ex:
        LOGGER.error('Error at get_title_ats function with message: %s', ex.message)
    return row1


def get_info_ats(row2_old, row3_old, row4_old):
    from control import process_cmd_lcd
    try:
        list_row = []
        row2 = 'Ket noi' if client_attributes.get('atsConnect') > 0 else 'Mat ket noi'
        row3 = 'Nguon: May phat' if client_attributes.get('atsContactorGenState') > 0 else 'Nguon: Dien luoi'
        row4 = 'Che do: ' + str(telemetries.get('atsState', default=''))
        if row2_old != row2:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
            row2_old = row2
        if row3_old != row3:
            process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
            row3_old = row3
        if row4_old != row4:
            process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
            row4_old = row4
        LOGGER.info('ATS SCREEN : %s', 1)

        list_row.append(row2_old)
        list_row.append(row3_old)
        list_row.append(row4_old)
        return list_row
    except Exception as ex:
        LOGGER.error('Error at get_info_ats function with message: %s', ex.message)


def get_detail_screen1_ats():
    from control import process_cmd_lcd
    from control.utils import read_to_json, write_to_json

    try:
        all_row = read_to_json(last_cmd_lcd)

        row2 = 'Dien luoi: ' + str(telemetries.get('atsAcState', default=''))
        row3 = 'May phat: ' + str(telemetries.get('atsGenState', default=''))
        row4 = 'Che do M.Phat: ' + str(telemetries.get('atsState', default=''))
        if all_row['row2'] != row2:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
            all_row['row2'] = row2
        if all_row['row3'] != row3:
            process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
            all_row['row3'] = row3
        if all_row['row4'] != row4:
            process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
            all_row['row4'] = row4

        write_to_json(all_row, last_cmd_lcd)
        LOGGER.info('ATS SCREEN : %s', 2)
    except Exception as ex:
        LOGGER.error('Error at get_detail_ats function with message: %s', ex.message)


def get_detail_screen2_ats():
    from control import process_cmd_lcd
    from control.utils import read_to_json, write_to_json
    try:
        all_row = read_to_json(last_cmd_lcd)

        row2 = telemetries.get('atsVacP1', default=0) + 'V ' + telemetries.get('atsVacP2',
                                                                               default=0) + 'V ' + telemetries.get(
            'atsVacP3', default=0) + 'V'
        row3 = telemetries.get('atsVgenP1', default=0) + 'V ' + telemetries.get('atsVgenP2',
                                                                                default=0) + 'V ' + telemetries.get(
            'atsVgenP3', default=0) + 'V'
        row4 = telemetries.get('atsVloadP1', default=0) + 'V ' + telemetries.get('atsVloadP2',
                                                                                 default=0) + 'V ' + telemetries.get(
            'atsVloadP3', default=0) + 'V'
        if all_row['row2'] != row2:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
            all_row['row2'] = row2
        if all_row['row3'] != row3:
            process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
            all_row['row3'] = row3
        if all_row['row4'] != row4:
            process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
            all_row['row4'] = row4
        LOGGER.info('ATS SCREEN : %s', 3)
        write_to_json(all_row, last_cmd_lcd)
    except Exception as ex:
        LOGGER.error('Error at get_detail_screen2_ats function with message: %s', ex.message)


def get_detail_screen3_ats():
    from control import process_cmd_lcd
    from control.utils import read_to_json, write_to_json
    try:
        all_row = read_to_json(last_cmd_lcd)
        row2 = telemetries.get('atsIloadP1', default=0) + 'A ' + telemetries.get('atsIloadP2',
                                                                                 default=0) + 'A ' + telemetries.get(
            'atsIloadP3', default=0) + 'A'
        row3 = telemetries.get('atsPac1', default=0) + 'W ' + telemetries.get('atsPac2',
                                                                              default=0) + 'W ' + telemetries.get(
            'atsPac3', default=0) + 'W'

        row4 = telemetries.get('atsVacFreq', default=0) + 'Hz ' + telemetries.get('atsVgenFreq',
                                                                                  default=0) + 'Hz ' + telemetries.get(
            'atsVloadFreq', default=0) + 'Hz'
        if all_row['row2'] != row2:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
            all_row['row2'] = row2
        if all_row['row3'] != row3:
            process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
            all_row['row3'] = row3
        if all_row['row4'] != row4:
            process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
            all_row['row4'] = row4
        LOGGER.info('ATS SCREEN : %s', 4)
        write_to_json(all_row, last_cmd_lcd)
    except Exception as ex:
        LOGGER.error('Error at get_detail_screen3_ats function with message: %s', ex.message)


def get_detail_screen4_ats():
    from control import process_cmd_lcd
    from control.utils import read_to_json, write_to_json
    try:
        all_row = read_to_json(last_cmd_lcd)
        row2 = telemetries.get('mccDcBat1Temp', default=0) + 'C ' + telemetries.get('mccDcBat2Temp',
                                                                                    default=0) + 'C ' + telemetries.get(
            'mccDcBat3Temp', default=0) + 'C'
        row3 = telemetries.get('mccDcV1', default=0) + 'V ' + telemetries.get('mccDcI1',
                                                                              default=0) + 'A ' + telemetries.get(
            'mccDcP1', default=0) + 'W'
        row4 = telemetries.get('mccDcV2', default=0) + 'V ' + telemetries.get('mccDcI2',
                                                                              default=0) + 'A ' + telemetries.get(
            'mccDcP2', default=0) + 'W'
        if all_row['row2'] != row2:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
            all_row['row2'] = row2
        if all_row['row3'] != row3:
            process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
            all_row['row3'] = row3
        if all_row['row4'] != row4:
            process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
            all_row['row4'] = row4
        LOGGER.info('ATS SCREEN : %s', 5)
        write_to_json(all_row, last_cmd_lcd)
    except Exception as ex:
        LOGGER.error('Error at get_detail_screen4_ats function with message: %s', ex.message)


def get_detail_screen5_ats():
    from control import process_cmd_lcd
    from control.utils import read_to_json, write_to_json
    try:
        all_row = read_to_json(last_cmd_lcd)
        row2 = telemetries.get('mccDcV3', default=0) + 'V ' + telemetries.get('mccDcI3',
                                                                              default=0) + 'A ' + telemetries.get(
            'mccDcP3', default=0) + 'W'
        row3 = telemetries.get('mccDcV4', default=0) + 'V ' + telemetries.get('mccDcI4',
                                                                              default=0) + 'A ' + telemetries.get(
            'mccDcP4', default=0) + 'W'
        row4 = telemetries.get('mccDcV5', default=0) + 'V ' + telemetries.get('mccDcI5',
                                                                              default=0) + 'A ' + telemetries.get(
            'mccDcP5', default=0) + 'W'
        if all_row['row2'] != row2:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
            all_row['row2'] = row2
        if all_row['row3'] != row3:
            process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
            all_row['row3'] = row3
        if all_row['row4'] != row4:
            process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
            all_row['row4'] = row4
        LOGGER.info('ATS SCREEN : %s', 6)
        write_to_json(all_row, last_cmd_lcd)
    except Exception as ex:
        LOGGER.error('Error at get_detail_screen5_ats function with message: %s', ex.message)


def get_screen_ats():
    from control.utils import read_to_json, write_to_json
    try:
        all_row = read_to_json(last_cmd_lcd)
        row1 = all_row['row1']
        row2 = all_row['row2']
        row3 = all_row['row3']
        row4 = all_row['row4']
        # enter func display
        row1 = get_title_ats(row1)
        list_row = get_info_ats(row2, row3, row4)
        # save to file
        all_row['row1'] = row1
        all_row['row2'] = list_row[0]
        all_row['row3'] = list_row[1]
        all_row['row4'] = list_row[2]
        write_to_json(all_row, last_cmd_lcd)
    except Exception as ex:
        LOGGER.error('Error at get_screen_ats function with message: %s', ex.message)
