from config import *
from config.common import *
from config.common_lcd_services import *

info = ['_'] * 16
level_at_index = [-1] * 16
# char = [chr(i) for i in range(ord('A'), ord('A') + 26)]
# char.append(" ")
CHAR = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y', 'Z', ' ', '_']
confirm_flag = False
confirm_idx = 0
cursor_idx = 0
ok_time = 0
first_access_flag = True
show_confirm_screen_flag = True
first_access_confirm_flag = True
CONFIRM_VALUE = [-1, True, False]


def call_screen_confirm(p_idx):
    from control import process_cmd_lcd
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
        process_cmd_lcd(ROW_1, UPDATE_VALUE, 'XAC NHAN')
        process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[p_idx]['row_2'])
        process_cmd_lcd(ROW_3, UPDATE_VALUE, switcher[p_idx]['row_3'])
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)


def process_confirm(button):
    global confirm_idx, show_confirm_screen_flag, first_access_confirm_flag

    save = CONFIRM_VALUE[0]
    if not first_access_confirm_flag:
        if button == UP:
            confirm_idx = 0
        elif button == DOWN:
            confirm_idx = 1
        elif button == OK:
            save = CONFIRM_VALUE[confirm_idx + 1]
            show_confirm_screen_flag = False
        if show_confirm_screen_flag:
            call_screen_confirm(confirm_idx)
    else:
        first_access_confirm_flag = False
        call_screen_confirm(confirm_idx)

    return save


def first_screen():
    from control import process_cmd_lcd

    process_cmd_lcd(ROW_1, UPDATE_VALUE, 'THONG TIN')
    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(info))
    process_cmd_lcd(ROW_3, UPDATE_VALUE, ' ')
    process_cmd_lcd(ROW_4, UPDATE_VALUE, ' ')


def info_setting_process(button):
    from control import process_cmd_lcd
    global ok_time, cursor_idx, show_confirm_screen_flag, confirm_idx, first_access_flag, confirm_flag, \
        first_access_confirm_flag

    try:
        save = -1
        ret = False
        if not first_access_flag:
            if not confirm_flag:
                if button == UP:
                    level_at_index[cursor_idx] += 1
                    if level_at_index[cursor_idx] > len(CHAR) - 1:
                        level_at_index[cursor_idx] = 0
                    info[cursor_idx] = CHAR[level_at_index[cursor_idx]]
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(info))
                elif button == DOWN:
                    level_at_index[cursor_idx] -= 1
                    if level_at_index[cursor_idx] < 0:
                        level_at_index[cursor_idx] = len(CHAR) - 1
                    info[cursor_idx] = CHAR[level_at_index[cursor_idx]]
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(info))
                elif button == RIGHT:
                    cursor_idx += 1
                    if cursor_idx > 15:
                        cursor_idx = 15
                elif button == LEFT:
                    cursor_idx -= 1
                    if cursor_idx < 0:
                        cursor_idx = 0
                elif button == OK:
                    confirm_flag = True
                    save = process_confirm(button)
            else:
                save = process_confirm(button)

            if save is True:
                a_file = open("./lcd_setting_data_file.json", "r")
                json_object = json.load(a_file)
                a_file.close()
                json_object["setting_info_title"] = ''.join(info).replace('_', '')
                a_file = open("./lcd_setting_data_file.json", "w")
                json.dump(json_object, a_file)
                a_file.close()
                ret = True
            elif save is False:
                ret = True
            else:
                show_confirm_screen_flag = True
        else:
            first_access_flag = False
            first_screen()

        return ret
    except Exception as ex:
        LOGGER.error('Error at call function in info_setting_process with message: %s', ex.message)


def get_default_value():
    global confirm_idx, cursor_idx, ok_time, first_access_flag, info, level_at_index, \
        show_confirm_screen_flag, first_access_confirm_flag, confirm_flag

    info = ['_'] * 16
    level_at_index = [-1] * 16
    confirm_idx = 0
    cursor_idx = 0
    ok_time = 0
    confirm_flag = False
    first_access_flag = True
    show_confirm_screen_flag = True
    first_access_confirm_flag = True
