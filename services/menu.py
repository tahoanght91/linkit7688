"""---------------------------------------------------------------------------------------------------------------------
                                                    Include
   ------------------------------------------------------------------------------------------------------------------"""
from config.common import *
from services.lcd import main_screen_lcd_services, ats_screen_lcd_services, ats_setting_lcd_service, \
    rfid_screen_lcd_sevices, rfid_setting_lcd_service
from services.lcd.acm_sreen_lcd_services import show_temp_condition
from services.lcd.alarm_lcd_services import check_alarm
from services.lcd.sensor_screen_lcd_services import *
# SonTH
from services.lcd.setting_datetime_screen_lcd_services import date_setting_process, time_setting_process
from services.lcd.setting_info_screen_lcd_services import info_setting_process
from services.lcd.setting_screen_lcd_services import *


"""---------------------------------------------------------------------------------------------------------------------
                                                    Define 
   ------------------------------------------------------------------------------------------------------------------"""
ROW = [ROW_1, ROW_2, ROW_3, ROW_4]
TIME_OUT = 600

setting_display_print = {
    0: {
        'row1': 'CAI DAT HE THONG',
        'row2': '> Thong tin',
        'row3': 'Ngay gio',
        'row4': 'Thong so mang'
        },
    1: {
        'row1': 'CAI DAT HE THONG',
        'row2': 'Thong tin',
        'row3': '> Ngay gio',
        'row4': 'Thong so mang'
        },
    2: {
        'row1': 'CAI DAT HE THONG',
        'row2': 'Thong tin',
        'row3': 'Ngay gio',
        'row4': '> Thong so mang'
        },
    3: {
        'row1': 'CAI DAT HE THONG',
        'row2': '> Canh bao',
        'row3': 'Thiet bi ATS',
        'row4': 'Thiet bi RFID'
        },
    4: {
        'row1': 'CAI DAT HE THONG',
        'row2': 'Canh bao',
        'row3': '> Thiet bi ATS',
        'row4': 'Thiet bi RFID'
        },
    5: {
        'row1': 'CAI DAT HE THONG',
        'row2': 'Canh bao',
        'row3': 'Thiet bi ATS',
        'row4': '> Thiet bi RFID'
        }
}

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


'''---------------------------------------------------------------------------------------------------------------------
                                                Global variable
   ------------------------------------------------------------------------------------------------------------------'''
event = 0
ats_screen_index = 0
setting_screen_index = 0
last_setting_screen_index = -1
screen_lv1_index = 0
last_screen_lv1_index = -1
time_count = 0
cycle_flag = False
time_setting_screen_index = 0,
last_time_setting_screen_index = -1

"""---------------------------------------------------------------------------------------------------------------------
                                                Internal function
   ------------------------------------------------------------------------------------------------------------------"""
''' print lcd function '''
def clear_display():
    cmd_lcd[CLEAR] = ''


def print_lcd(str1, str2, str3, str4):
    from control import process_cmd_lcd
    try:
        str = [str1, str2, str3, str4]
        LOGGER.info('Send message print_lcd on lcd')
        i = 0
        while i < 4:
            if str[i] == '':
                str[i] = ' '
            status = process_cmd_lcd(ROW[i], UPDATE_VALUE, str[i])
            if status:
                i += 1
    except Exception as ex:
        LOGGER.info('print_lcd function error: %s', ex.message)


''' screen level 1 implement '''
def main_display():
    main_screen_lcd_services.screen_main()


def warning_display():
    check_alarm()


def security_sensor_info_display():
    global event

    LOGGER.info('Enter security_sensor_info_display function')
    if event == LEFT:
        security_sensor_screen_1(telemetries)
    elif event == RIGHT:
        security_sensor_screen_2(telemetries)


def air_info_display():
    show_temp_condition(telemetries)


def ats_display():
    global ats_screen_index
    ats_display_func = {
        0: ats_screen_lcd_services.get_screen_ats,
        1: ats_screen_lcd_services.get_detail_screen1_ats,
        2: ats_screen_lcd_services.get_detail_screen2_ats,
        3: ats_screen_lcd_services.get_detail_screen3_ats,
        4: ats_screen_lcd_services.get_detail_screen4_ats,
        5: ats_screen_lcd_services.get_detail_screen5_ats
    }
    try:
        if event == RIGHT:
            ats_screen_index += 1
        elif event == LEFT:
            ats_screen_index -= 1
        if ats_screen_index > 5:
            ats_screen_index = 5
        elif ats_screen_index < 0:
            ats_screen_index = 0

        func = ats_display_func[ats_screen_index]
        LOGGER.info('ATS DISPLAY DETAIL %s', str(ats_screen_index))
        return func()
    except Exception as ex:
        LOGGER.error('ats_display function error: %s', ex.message)


def rfid_display():
    rfid_screen_lcd_sevices.get_screen_rfid()
    LOGGER.info('RFID DISPLAY')


def setting_display():
    global setting_screen_index, event, last_setting_screen_index
    try:
        if event == UP:
            setting_screen_index -= 1
        elif event == DOWN:
            setting_screen_index += 1
        if setting_screen_index > 5:
            setting_screen_index = 5
        elif setting_screen_index < 0:
            setting_screen_index = 0
        if event == LEFT:
            setting_screen_index = 0
        elif event == RIGHT:
            setting_screen_index = 3
        if last_setting_screen_index != setting_screen_index:
            print_lcd(setting_display_print[setting_screen_index]['row1'],
                      setting_display_print[setting_screen_index]['row2'],
                      setting_display_print[setting_screen_index]['row3'],
                      setting_display_print[setting_screen_index]['row4'])
            last_setting_screen_index = setting_screen_index
        if event == OK:
            select_setting()
        LOGGER.info('setting menu, setting_screen_index: %s', str(setting_screen_index))
    except Exception as ex:
        LOGGER.error('setting_display function error: %s', ex.message)


''' Setting implement '''
def select_setting():
    global event, setting_screen_index
    setting_function_list = {
        0: information_setting,
        1: time_setting,
        2: internet_setting,
        3: warning_setting,
        4: ats_setting,
        5: rfid_setting
    }

    func = setting_function_list.get(setting_screen_index)
    return func()


def information_setting():
    global event

    LOGGER.info('Finish cai_dat_thong_tin function')
    info_setting_process(event)


def time_setting():
    global event, time_setting_screen_index, last_time_setting_screen_index

    try:
        if event == DOWN:
            time_setting_screen_index = 1
        elif event == UP:
            time_setting_screen_index = 0
        elif event == OK:
            if time_setting_screen_index == 0:
                date_setting_process(event)
            else:
                time_setting_process(event)
        if last_time_setting_screen_index != time_setting_screen_index:
            print_lcd(time_setting_print[time_setting_screen_index]['row1'],
                      time_setting_print[time_setting_screen_index]['row2'],
                      time_setting_print[time_setting_screen_index]['row3'],
                      time_setting_print[time_setting_screen_index]['row4'])
            last_time_setting_screen_index = time_setting_screen_index
        LOGGER.info('finish time_setting function, time_setting_screen_index: %s', str(time_setting_screen_index))
    except Exception as ex:
        LOGGER.error('time_setting function error: %s', ex.message)


def internet_setting():
    global event, screen_lv1_index

    LOGGER.info('Enter thong_so_mang function')
    # Call function xu ly keycode
    choose_config(screen_lv1_index + 1)
    listen_key_code(event)

def warning_setting():
    global event, screen_lv1_index

    LOGGER.info('Enter canh_bao function')
    # Call function xu ly keycode
    choose_config(screen_lv1_index + 1)
    listen_key_code(event)


def ats_setting():
    global event

    ats_setting_lcd_service.listen_key_code(event)


def rfid_setting():
    global event

    rfid_setting_lcd_service.listen_key_code(event)


def back_main_screen(button):
    global cycle_flag, time_count, screen_lv1_index
    start_time = 0
    try:
        if button != -1:
            start_time = time.time()
            cycle_flag = True
        if cycle_flag is True:
            time_count = time.time() - start_time
            LOGGER.info('Time out come back to main display: %ds', time_count)
        if time_count > TIME_OUT:
            time_count = 0
            cycle_flag = False
            screen_lv1_index = 0
    except Exception as ex:
        LOGGER.error('back_main_screen function error: %s', ex.message)


'''---------------------------------------------------------------------------------------------------------------------
                                                 External function
   ------------------------------------------------------------------------------------------------------------------'''
def main_menu(button):
    global screen_lv1_index, event, last_screen_lv1_index

    try:
        menu_function_list = {
            ESC: main_display,
            CANH_BAO: warning_display,
            CAM_BIEN: security_sensor_info_display,
            DIEU_HOA: air_info_display,
            ATS: ats_display,
            SETTING: setting_display,
            RFID: rfid_display
        }

        if button in MENU_LV_1 and last_screen_lv1_index != screen_lv1_index:
            screen_lv1_index = button
            last_screen_lv1_index = screen_lv1_index
        elif button != -1:
            event = button
        back_main_screen(button)
        func = menu_function_list.get(screen_lv1_index)

        return func()
    except Exception as ex:
        LOGGER.error('print_screen function error: %s', ex.message)
