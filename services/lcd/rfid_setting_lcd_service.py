# coding=utf-8
from config import *
from config.common import UPDATE_VALUE
from config.common_lcd_services import *

data_setting_path = './lcd_setting_data_file.json'
setting_rfid_allow = 0
# Mặc định vào màn hình đầu tiên id = 0, con trỏ dòng đầu của selection
screen_idx = 0
pointer_idx = -1

# Thông tin tên id của từng màn hình
screens_info = {"rfid_setting": 0, "confirmRfidMode": 1}


# Màn hình chính được call ở menu
def call_screen_rfid_setting(p_idx, isFirst):
    from control import process_cmd_lcd
    global screen_idx, pointer_idx
    try:
        switcher = [
            {
                "row_2": '> Cho phep doc',
                "row_3": 'Khong doc'
            },
            {
                "row_2": 'Cho phep doc',
                "row_3": '> Khong doc'
            }
        ]
        # Update text
        if isFirst == 1:
            refresh_screen()
            process_cmd_lcd(ROW_1, UPDATE_VALUE, 'THIET BI RFID')
            process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[p_idx]['row_2'])
            process_cmd_lcd(ROW_3, UPDATE_VALUE, switcher[p_idx]['row_3'])
        elif isFirst == 0:
            process_cmd_lcd(pointer_idx + 2, UPDATE_VALUE, switcher[p_idx]['row_{0}'.format(pointer_idx + 2)])
            process_cmd_lcd(p_idx + 2, UPDATE_VALUE, switcher[p_idx]['row_{0}'.format(p_idx + 2)])

        screen_idx = screens_info["rfid_setting"]
        pointer_idx = p_idx
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)


# Màn hình xác nhận
def call_screen_confirm(p_idx, isFirst):
    from control import process_cmd_lcd
    global screen_idx, pointer_idx
    try:
        switcher = [
            {
                "row_2": '> Co',
                "row_3": 'Khong'
            },
            {
                "row_2": 'Co',
                "row_3": '> Khong'
            }
        ]
        # Update text
        if isFirst == 1:
            refresh_screen()
            process_cmd_lcd(ROW_1, UPDATE_VALUE, 'XAC NHAN LUU')
            process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[p_idx]['row_2'])
            process_cmd_lcd(ROW_3, UPDATE_VALUE, switcher[p_idx]['row_3'])
        elif isFirst == 0:
            process_cmd_lcd(pointer_idx + 2, UPDATE_VALUE, switcher[p_idx]['row_{0}'.format(pointer_idx + 2)])
            process_cmd_lcd(p_idx + 2, UPDATE_VALUE, switcher[p_idx]['row_{0}'.format(p_idx + 2)])

        screen_idx = screens_info["confirmRfidMode"]
        pointer_idx = p_idx

    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)


def refresh_screen():
    from control import process_cmd_lcd
    try:
        # Update text
        process_cmd_lcd(ROW_1, UPDATE_VALUE, '')
        process_cmd_lcd(ROW_2, UPDATE_VALUE, '')
        process_cmd_lcd(ROW_3, UPDATE_VALUE, '')
        process_cmd_lcd(ROW_4, UPDATE_VALUE, '')
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)


# Register func nay
def listen_key_code(keycode):
    try:
        if screen_idx == screens_info["rfid_setting"]:
            rfid_setting_listen_key(keycode)
        elif screen_idx == screens_info["confirmRfidMode"]:
            confirm_listen_key(keycode)
        else:
            return
    except Exception as ex:
        LOGGER.error('Error at call function listen_key_code with message: %s', ex.message)


def rfid_setting_listen_key(keycode):
    global screen_idx, pointer_idx, setting_rfid_allow
    try:
        if keycode == BUTTON_34_EVENT_UP:
            # down
            if pointer_idx == 1:
                pointer_idx = 1
            else:
                pointer_idx = pointer_idx + 1
            call_screen_rfid_setting(pointer_idx, isFirst=0)

        elif keycode == BUTTON_14_EVENT_UP:
            # up
            if pointer_idx == 0:
                pointer_idx = 0
            else:
                pointer_idx = pointer_idx - 1
            call_screen_rfid_setting(pointer_idx, isFirst=0)

        elif keycode == BUTTON_24_EVENT_UP:
            # ok
            if pointer_idx == 0:
                setting_rfid_allow = 1
            else:
                setting_rfid_allow = 0

            if pointer_idx == -1:
                call_screen_rfid_setting(0, isFirst=1)
            else:
                call_screen_confirm(pointer_idx, isFirst=1)
        else:
            pass
    except Exception as ex:
        LOGGER.error('Error at call function ats_setting_listen_key with message: %s', ex.message)


def confirm_listen_key(keycode):
    global pointer_idx
    try:
        if keycode == BUTTON_34_EVENT_UP:
            # down
            if pointer_idx == 1:
                pointer_idx = 1
            else:
                pointer_idx = pointer_idx + 1
            call_screen_confirm(pointer_idx, isFirst=0)

        elif keycode == BUTTON_14_EVENT_UP:
            # up
            if pointer_idx == 0:
                pointer_idx = 0
            else:
                pointer_idx = pointer_idx - 1
            call_screen_confirm(pointer_idx, isFirst=0)

        elif keycode == BUTTON_24_EVENT_UP:
            if pointer_idx == 0:
                update_to_file_json_setting(setting_rfid_allow)
            if pointer_idx == 1:
                call_screen_rfid_setting(p_idx=0, isFirst=1)
        else:
            pass
    except Exception as ex:
        LOGGER.error('Error at call function in confirm_listen_key with message: %s', ex.message)


def reset_params():
    try:
        global setting_rfid_allow, screen_idx, pointer_idx
        setting_rfid_allow = 0
        screen_idx = 0
        pointer_idx = -1
    except Exception as ex:
        LOGGER.error('Error at call function in confirm_listen_key with message: %s', ex.message)


def update_to_file_json_setting(allow):
    from control.utils import read_to_json, write_to_json
    try:
        data = read_to_json(data_setting_path)
        data['setting_rfid_allow'] = allow
        write_to_json(data, data_setting_path)
        call_screen_rfid_setting(p_idx=0, isFirst=1)
        LOGGER.info('Enter update_to_file_json_setting function, data: %s', str(data))
    except Exception as ex:
        LOGGER.error('Error at call function in confirm_listen_key with message: %s', ex.message)