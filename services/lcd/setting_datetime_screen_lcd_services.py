import os
from config import *
from config.common import *
from config.common_lcd_services import *

# Common variables
date = ['_', '_', '/', '_', '_', '/', '_', '_', '_', '_']
time = ['_', '_', ':', '_', '_']
level_at_index = [0] * 12
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

time_setting_print = {
    0: {
        'row1': 'THOI GIAN',
        'row2': '> Ngay',
        'row3': 'Ngay gio',
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
def date_setting_process(button):
    try:
        from control import process_cmd_lcd
        global confirm_status, confirm_idx, confirm_status, cursor_idx, date, time, number
        if confirm_status:
            if button == OK:
                if confirm_idx == 0:
                    try:
                        os.system("""date +%Y%m%d "{year}{month}{day}" """.format(year=''.join(date[6:9]),
                                                                                  month=''.join(date[3:4]),
                                                                                  day=''.join(date[0:1])))
                    except Exception as ex:
                        LOGGER.error('Error at set datetime to os in os.system with message: %s', ex.message)
                    confirm_status = False
                    # ham thoat
                    process_cmd_lcd(ROW_1, UPDATE_VALUE, 'NGAY')
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(date))
                else:
                    process_cmd_lcd(ROW_1, UPDATE_VALUE, 'NGAY')
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(date))
                    confirm_status = False
            elif button == UP or button == DOWN:
                if confirm_idx == 0:
                    confirm_idx = 1
                else:
                    confirm_idx = 0
        else:
            if button == OK:
                if ['_', '_', '/', ' ', '_', '_', '/', ' ', '_', '_', '_', '_'] == date:
                    process_cmd_lcd(ROW_1, UPDATE_VALUE, 'NGAY')
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(date))
                    process_cmd_lcd(ROW_3, UPDATE_VALUE, '')
                elif "_" not in date:
                    confirm_status = True
                    call_screen_confirm(0)

            else:
                if button == UP:
                    level_at_index[cursor_idx] += 1

                    if level_at_index[cursor_idx] > 9:
                        level_at_index[cursor_idx] = 0

                    date[cursor_idx] = number[level_at_index[cursor_idx]]
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(date))
                elif button == DOWN:
                    level_at_index[cursor_idx] -= 1
                    if level_at_index[cursor_idx] < 0:
                        level_at_index[cursor_idx] = 9
                    date[cursor_idx] = number[level_at_index[cursor_idx]]
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(date))
                elif button == RIGHT:
                    if cursor_idx == 1 or cursor_idx == 4:
                        cursor_idx += 2
                    else:
                        cursor_idx += 1
    except Exception as ex:
        LOGGER.error('Error at call function in date_setting_process with message: %s', ex.message)


# Time setting
def time_setting_process(button):
    try:
        from control import process_cmd_lcd
        global confirm_status, confirm_idx, cursor_idx_time, time
        if confirm_status:
            if button == OK:
                if confirm_idx == 0:
                    try:
                        os.system("""date +%T -s "{hour}:{minute}" """.format(hour=''.join(time[0:1]),
                                                                              minute=''.join(time[3:4])))
                    except Exception as ex:
                        LOGGER.error('Error at call function in os.system in 113 with message: %s', ex.message)
                    confirm_status = False
                    # ham thoat
                    process_cmd_lcd(ROW_1, UPDATE_VALUE, 'GIO')
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(time))
                else:
                    process_cmd_lcd(ROW_1, UPDATE_VALUE, 'GIO')
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(time))
            elif button == UP or button == DOWN:
                if confirm_idx == 0:
                    confirm_idx = 1
                else:
                    confirm_idx = 0
        else:
            if button == OK:
                if ['_', '_', ':', ' ', '_', '_'] == time:
                    process_cmd_lcd(ROW_1, UPDATE_VALUE, 'GIO')
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(time))
                elif "_" not in time:
                    confirm_status = True
                    call_screen_confirm(0)
            else:
                if button == UP:
                    level_at_index_time[cursor_idx_time] += 1

                    if level_at_index_time[cursor_idx_time] > 9:
                        level_at_index_time[cursor_idx_time] = 0

                    time[cursor_idx_time] = number[level_at_index_time[cursor_idx_time]]
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(time))
                elif button == DOWN:
                    level_at_index_time[cursor_idx_time] -= 1
                    if level_at_index_time[cursor_idx_time] < 0:
                        level_at_index_time[cursor_idx_time] = 9
                    time[cursor_idx_time] = number[level_at_index_time[cursor_idx_time]]
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, ''.join(time))
                elif button == RIGHT:
                    if cursor_idx_time == 1:
                        cursor_idx_time += 2
                    else:
                        cursor_idx_time += 1
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