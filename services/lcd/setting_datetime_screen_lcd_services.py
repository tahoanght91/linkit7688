import os
from config import *
from config.common import *
from config.common_lcd_services import *

# Define
GO_CONFIRM = True
NOT_GO_CONFIRM = False
HOUR = [str(u) for u in range(24)]
MIN = [str(u) for u in range(60)]
YEAR = [str(u) for u in range(2021, 2101)]
MONTH = [str(u) for u in range(1, 13)]
DAY = [str(u) for u in range(1, 32)]

# Common variables
date = ['____', '/', '__', '/', '__']
time = ['__', ':', '__']
level_at_index_date = [0] * 3
level_at_index_time = [0] * 2

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
    global level_at_index_date, date

    if cursor_index == 0:
        date[cursor_index] = YEAR[level_at_index_date[cursor_index]-2021]
    elif cursor_index == 1:
        date[cursor_index+1] = MONTH[level_at_index_date[cursor_index]-1]
    elif cursor_index == 2:
        date[cursor_index+2] = DAY[level_at_index_date[cursor_index]-1]
    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(date))


def date_setting_process(button):
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
                if cursor_idx == 0:
                    if level_at_index_date[cursor_idx] > 2100:
                        level_at_index_date[cursor_idx] = 2021
                elif cursor_idx == 1:
                    if level_at_index_date[cursor_idx] > 12:
                        level_at_index_date[cursor_idx] = 0
                elif cursor_idx == 2:
                    if level_at_index_date[cursor_idx] > 31:
                        level_at_index_date[cursor_idx] = 0
            elif button == DOWN:
                level_at_index_date[cursor_idx] -= 1
                if cursor_idx == 0:
                    if level_at_index_date[cursor_idx] < 2021:
                        level_at_index_date[cursor_idx] = 2100
                elif cursor_idx == 1:
                    if level_at_index_date[cursor_idx] < 1:
                        level_at_index_date[cursor_idx] = 12
                elif cursor_idx == 2:
                    if level_at_index_date[cursor_idx] < 1:
                        level_at_index_date[cursor_idx] = 31
            elif button == RIGHT:
                cursor_idx += 1
                if cursor_idx > 2:
                    cursor_idx = 2
            elif button == LEFT:
                cursor_idx -= 1
                if cursor_idx < 0:
                    cursor_idx = 0
            elif button == OK and cursor_idx == 2:
                screen_confirm_flag = True
                call_screen_confirm(confirm_idx)
        else:
            if button == UP:
                confirm_idx = 0
            elif button == DOWN:
                confirm_idx = 1
            elif button == OK:
                if confirm_idx == 0:
                    try:
                        LOGGER.info("date -s %s.%s.%s-%s:%s", str(date[0]), str(date[2]), str(date[4]), str(0), str(0))
                        os.system('date -s {year}.{month}.{day}-{hour}:{min}'.format(year=date[0], month=date[2], day=date[4], hour=0, min=0))
                    except Exception as ex:
                        LOGGER.error('Error at set datetime to os in os.system with message: %s', ex.message)
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
    global level_at_index_time, time

    if cursor_index == 0:
        time[cursor_index] = HOUR[level_at_index_time[cursor_index]]
    elif cursor_index == 1:
        time[cursor_index+1] = MIN[level_at_index_time[cursor_index]]
    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(time))


def time_setting_process(button):
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
                if cursor_idx == 0:
                    if level_at_index_time[cursor_idx] > 23:
                        level_at_index_time[cursor_idx] = 0
                elif cursor_idx == 1:
                    if level_at_index_time[cursor_idx] > 59:
                        level_at_index_time[cursor_idx] = 0
            elif button == DOWN:
                level_at_index_time[cursor_idx] -= 1
                if cursor_idx == 0:
                    if level_at_index_time[cursor_idx] < 0:
                        level_at_index_time[cursor_idx] = 23
                elif cursor_idx == 1:
                    if level_at_index_time[cursor_idx] < 0:
                        level_at_index_time[cursor_idx] = 59
            elif button == RIGHT:
                cursor_idx = 1
            elif button == LEFT:
                cursor_idx = 0
            elif button == OK and cursor_idx == 1:
                screen_confirm_flag = True
                call_screen_confirm(confirm_idx)
        else:
            if button == UP:
                confirm_idx = 0
            elif button == DOWN:
                confirm_idx = 1
            elif button == OK:
                if confirm_idx == 0:
                    try:
                        LOGGER.info("date -s %s:%s", str(time[0]), str(time[2]))
                        os.system('date -s {hour}:{minute}'.format(hour=time[0], minute=time[2]))
                    except Exception as ex:
                        LOGGER.error('Error at call function in os.system in 113 with message: %s', ex.message)
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
    global date, time, level_at_index_date, level_at_index_time, level_at_index_time, ok_time, cursor_idx, \
        cursor_idx_time, confirm_idx, confirm_status, last_time_setting_screen_index, time_setting_screen_index, \
        go_setting_flag, screen_confirm_flag, first_access_flag

    date = ['____', '/', '__', '/', '__']
    time = ['__', ':', '__']
    level_at_index_date = [0] * 3
    level_at_index_time = [0] * 2
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
