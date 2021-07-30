from config import *
from config.common import UPDATE_VALUE
from config.common_lcd_services import *


# HungLQ
from services.lcd.ats_screen_lcd_services import convert_to_string_default

last_cmd_lcd = './last_cmd_screen.json'


def get_title_rfid(row1):
    from control import process_cmd_lcd
    try:
        show = 'THONG TIN RFID'
        if row1 != show:
            process_cmd_lcd(ROW_1, UPDATE_VALUE, show)
            row1 = show
    except Exception as ex:
        LOGGER.warning('Error at get_title_rfid function with message: %s', ex.message)
    return row1


def get_info_rfid(row2, row3, row4):
    from control import process_cmd_lcd
    try:
        list_row = []
        json_file = open('./last_rfid_card_code.json', )
        rfid_info = json.load(json_file)
        status = 'Ket noi' if convert_to_string_default('mccRfidConnectState', 1) != '0' else 'Mat ket noi'
        if row2 != str(status):
            process_cmd_lcd(ROW_2, UPDATE_VALUE, str(status))
            row2 = str(status)
        if row3 != str(rfid_info['Time']):
            process_cmd_lcd(ROW_3, UPDATE_VALUE, str(rfid_info['Time']))
            row3 = str(rfid_info['Time'])
        if row4 != str(rfid_info['StaffCode']):
            process_cmd_lcd(ROW_4, UPDATE_VALUE, str(rfid_info['StaffCode']))
            row4 = str(rfid_info['StaffCode'])

        list_row.append(row2)
        list_row.append(row3)
        list_row.append(row4)

    except Exception as ex:
        LOGGER.warning('Error at get_info_rfid function with message: %s', ex.message)
    return list_row


def get_screen_rfid():
    from control.utils import read_to_json, write_to_json

    try:
        all_row = read_to_json(last_cmd_lcd)
        row1 = all_row['row1']
        row2 = all_row['row2']
        row3 = all_row['row3']
        row4 = all_row['row4']
        # enter func display
        row1 = get_title_rfid(row1)
        list_row = get_info_rfid(row2, row3, row4)
        # save to file
        all_row['row1'] = row1
        all_row['row2'] = list_row[0]
        all_row['row3'] = list_row[1]
        all_row['row4'] = list_row[2]
        write_to_json(all_row, last_cmd_lcd)
    except Exception as ex:
        LOGGER.warning('Error at get_screen_rfid function with message: %s', ex.message)
