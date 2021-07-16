import os
from config import *
from config.common import *
from config.common_lcd_services import *

# Define
GO_CONFIRM = True
NOT_GO_CONFIRM = False

# Common variables
date = ['_', '_', '/', '_', '_', '/', '_', '_', '_', '_']
time = ['_', '_', ':', '_', '_']
level_at_index_date = [0] * 12
level_at_index_time = [0] * 6
number = [str(u) for u in range(10)]
ok_time = 0
cursor_idx = 0
cursor_idx_time = 0
confirm_idx = 0
confirm_status = False
last_time_setting_screen_index = -1
time_setting_screen_index = 0
go_setting_flag = False
screen_confirm_flag = False
first_access_flag = True
time_setting_print = {
    0: {
        'row1': 'THOI GIAN',
        'row2': '> Ngay',
        'row3': 'Gio',
        'row4': ''
    },
    1: {
        'row1': 'THOI GIAN',
        'row2': 'Ngay',
        'row3': '> Gio',
        'row4': ''
    }
}


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
        LOGGER.info('Enter call_screen_confirm function', )
        process_cmd_lcd(ROW_1, UPDATE_VALUE, 'XAC NHAN')
        process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[p_idx]['row_2'])
        process_cmd_lcd(ROW_3, UPDATE_VALUE, switcher[p_idx]['row_3'])
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)

# Date setting
def date_setting_screen(cursor_index):
    from control import process_cmd_lcd
    global level_at_index_date, number, date

    date[cursor_index] = number[level_at_index_date[cursor_index]]
    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(date))


def date_setting_process(button):
    from time import sleep
    from control import process_cmd_lcd
    global cursor_idx, level_at_index_date, date, confirm_idx, screen_confirm_flag, first_access_flag, go_setting_flag

    try:
        if first_access_flag is True:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(date))
            process_cmd_lcd(ROW_3, UPDATE_VALUE, '')
            first_access_flag = False
            return NOT_GO_CONFIRM
        if screen_confirm_flag is False:
            if button == UP:
                level_at_index_date[cursor_idx] += 1

                if level_at_index_date[cursor_idx] > 9:
                    level_at_index_date[cursor_idx] = 0

            elif button == DOWN:
                level_at_index_date[cursor_idx] -= 1
                if level_at_index_date[cursor_idx] < 0:
                    level_at_index_date[cursor_idx] = 9
            elif button == RIGHT and cursor_idx < 10:
                if cursor_idx == 1 or cursor_idx == 4:
                    cursor_idx += 2
                else:
                    cursor_idx += 1
                if cursor_idx > 9:
                    cursor_idx = 9
            elif button == LEFT and cursor_idx < 10:
                if cursor_idx == 3 or cursor_idx == 6:
                    cursor_idx -= 2
                else:
                    cursor_idx -= 1
                if cursor_idx < 0:
                    cursor_idx = 0
            elif button == OK and cursor_idx == 9:
                screen_confirm_flag = True
                call_screen_confirm(confirm_idx)
        else:
            if button == UP:
                confirm_idx = 0
            elif button == DOWN:
                confirm_idx = 1
            elif button == OK:
                if confirm_idx == 0:
                    # try:
                    #     os.system("""date +%Y%m%d "{year}{month}{day}" """.format(year=''.join(date[6:9]),
                    #                                                               month=''.join(date[3:4]),
                    #                                                               day=''.join(date[0:1])))
                    # except Exception as ex:
                    #     LOGGER.error('Error at set datetime to os in os.system with message: %s', ex.message)
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, 'DA LUU THOI GIAN')
                    sleep(3)
                get_default_value()
                return GO_CONFIRM
            call_screen_confirm(confirm_idx)
            return NOT_GO_CONFIRM
        if button is UP or button is DOWN:
            date_setting_screen(cursor_idx)
    except Exception as ex:
        LOGGER.error('Error at call function in date_setting_process with message: %s', ex.message)


# Time setting
def time_setting_screen(cursor_index):
    from control import process_cmd_lcd
    global level_at_index_time, number, time

    time[cursor_index] = number[level_at_index_time[cursor_index]]
    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(time))


def time_setting_process(button):
    from time import sleep
    from control import process_cmd_lcd
    global cursor_idx, level_at_index_time, time, confirm_idx, screen_confirm_flag, first_access_flag, go_setting_flag

    try:
        if first_access_flag is True:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(time))
            process_cmd_lcd(ROW_3, UPDATE_VALUE, '')
            first_access_flag = False
            return NOT_GO_CONFIRM
        if screen_confirm_flag is False:
            if button == UP:
                level_at_index_time[cursor_idx] += 1

                if level_at_index_time[cursor_idx] > 9:
                    level_at_index_time[cursor_idx] = 0

            elif button == DOWN:
                level_at_index_time[cursor_idx] -= 1
                if level_at_index_time[cursor_idx] < 0:
                    level_at_index_time[cursor_idx] = 9
            elif button == RIGHT and cursor_idx < 5:
                if cursor_idx == 1:
                    cursor_idx += 2
                else:
                    cursor_idx += 1
                if cursor_idx > 4:
                    cursor_idx = 4
            elif button == LEFT and cursor_idx < 5:
                if cursor_idx == 1:
                    cursor_idx -= 2
                else:
                    cursor_idx -= 1
                if cursor_idx < 0:
                    cursor_idx = 0
            elif button == OK and cursor_idx == 4:
                screen_confirm_flag = True
                call_screen_confirm(confirm_idx)
        else:
            if button == UP:
                confirm_idx = 0
            elif button == DOWN:
                confirm_idx = 1
            elif button == OK:
                if confirm_idx == 0:
                    # try:
                    #     os.system("""date +%T -s "{hour}:{minute}" """.format(hour=''.join(time[0:1]),
                    #                                                           minute=''.join(time[3:4])))
                    # except Exception as ex:
                    #     LOGGER.error('Error at call function in os.system in 113 with message: %s', ex.message)
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, 'DA LUU THOI GIAN')
                    sleep(3)
                get_default_value()
                return GO_CONFIRM
            call_screen_confirm(confirm_idx)
            return NOT_GO_CONFIRM
        if button is UP or button is DOWN:
            time_setting_screen(cursor_idx)
    except Exception as ex:
        LOGGER.error('Error at call function in time_setting_process with message: %s', ex.message)


def datetime_setting(button):
    from control import process_cmd_lcd
    global last_time_setting_screen_index, time_setting_screen_index, ok_time, go_setting_flag

    try:
        function = {
            0: date_setting_process,
            1: time_setting_process
        }
        if go_setting_flag is True:
            return function[time_setting_screen_index](button)
        if button == DOWN:
            time_setting_screen_index = 1
        elif button == UP:
            time_setting_screen_index = 0
        elif button == OK:
            if ok_time > 0:
                go_setting_flag = True
                return function[time_setting_screen_index](button)
            else:
                ok_time = 1
        if last_time_setting_screen_index != time_setting_screen_index:
            process_cmd_lcd(ROW_1, UPDATE_VALUE, time_setting_print[time_setting_screen_index]['row1'])
            process_cmd_lcd(ROW_2, UPDATE_VALUE, time_setting_print[time_setting_screen_index]['row2'])
            process_cmd_lcd(ROW_3, UPDATE_VALUE, time_setting_print[time_setting_screen_index]['row3'])
            process_cmd_lcd(ROW_4, UPDATE_VALUE, time_setting_print[time_setting_screen_index]['row4'])
            last_time_setting_screen_index = time_setting_screen_index
        LOGGER.info('finish time_setting function, time_setting_screen_index: %s', str(time_setting_screen_index))
    except Exception as ex:
        LOGGER.error('time_setting function error: %s', ex.message)


def get_default_value():
    global date, time, level_at_index_date, level_at_index_time, level_at_index_time, number, ok_time, cursor_idx, \
        cursor_idx_time, confirm_idx, confirm_status, last_time_setting_screen_index, time_setting_screen_index, \
        go_setting_flag, screen_confirm_flag, first_access_flag

    date = ['_', '_', '/', '_', '_', '/', '_', '_', '_', '_']
    time = ['_', '_', ':', '_', '_']
    level_at_index_date = [0] * 12
    level_at_index_time = [0] * 6
    number = 0
    ok_time = 0
    cursor_idx = 0
    cursor_idx_time = 0
    confirm_idx = 0
    confirm_status = False
    last_time_setting_screen_index = -1
    time_setting_screen_index = 0
    go_setting_flag = False
    screen_confirm_flag = False
    first_access_flag = True
