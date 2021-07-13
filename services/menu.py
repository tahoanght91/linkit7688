from config import *
from config.common import *
from config.common_lcd_services import *
from services.lcd import main_screen_lcd_services
from services.lcd.acm_sreen_lcd_services import show_temp_condition
from services.lcd.alarm_lcd_services import check_alarm
from services.lcd import ats_screen_lcd_services, ats_setting_lcd_service
from services.lcd import rfid_screen_lcd_sevices, rfid_setting_lcd_service
from services.lcd.sensor_screen_lcd_services import *
from time import time

# SonTH
from services.lcd.setting_screen_lcd_services import *

TIME_OUT = 600
ROW = [ROW_1, ROW_2, ROW_3, ROW_4]
section_lv_1 = 0
section_lv_2 = 0
section_lv_3 = -1
section_lv_4 = -1
section_lv_5 = -1
time_count = 0
button = 0
set_string_ok = 0
cycle_flag = False
time_cycle = 0
def print_lcd(str1, str2, str3, str4):
    from control import process_cmd_lcd
    status = False
    try:
        str = [str1, str2, str3, str4]
        LOGGER.info('Send message print_lcd on lcd')
        i = 0
        while i < 4:
            # if str[i] != '':
            #     status = process_cmd_lcd(ROW[i], UPDATE_VALUE, str[i])
            status = process_cmd_lcd(ROW[i], UPDATE_VALUE, str[i])
            if status:
                i += 1
    except Exception as ex:
        LOGGER.info('print_lcd_lcd function error: %s', ex.message)


def clear_display():
    cmd_lcd[CLEAR] = ''


def select_section_lv1():
    global section_lv_1
    global section_lv_2
    global button

    try:
        if button in MENU_LV_1:
            section_lv_1 = MENU_LV_1.index(button)
        switcher = {
            0: main_display,
            1: warning_display,
            2: security_sensor_info_display,
            3: air_info_display,
            4: ats_display,
            5: setting_display,
            6: rfid_display,
        }
        LOGGER.info('Send message select_section_lv1 on lcd, section_lv_1: %s', str(section_lv_1))
        func = switcher.get(section_lv_1)
        return func()
    except Exception as ex:
        LOGGER.error('Error at call function in select_section_lv1 with message: %s', ex.message)


def main_display():
    main_screen_lcd_services.screen_main()


def warning_display():
    check_alarm()
    # global button
    # try:
    #     ats_setting_lcd_service.listen_key_code(button)
    # except Exception as ex:
    #     LOGGER.error('Error at call function in warning_display with message: %s', ex.message)


def security_sensor_info_display():
    global section_lv_2

    if button == LEFT:
        section_lv_2 = 0
    elif button == RIGHT:
        section_lv_2 = 1

    if section_lv_2 == 0:
        security_sensor_screen_1(telemetries)
    if section_lv_2 == 1:
        security_sensor_screen_2(telemetries)
    LOGGER.info('Enter security_sensor_info_display function')
    LOGGER.info('section_lv_2: %s', str(section_lv_2))


def air_info_display():
    # print_lcd('BAN TIN DIEU HOA',
    #           'DH1: bat, HD2:Tat',
    #           'Quat:Bat',
    #           'Che do: Auto')
    # # goi ham hien thi
    show_temp_condition(telemetries)
    # LOGGER.info('Enter air_info_display function')
    # LOGGER.info('section_lv_2: %s', str(section_lv_2))


def ats_display():
    global section_lv_2

    if button == RIGHT:
        section_lv_2 += 1
    elif button == LEFT:
        section_lv_2 -= 1
    if section_lv_2 > 5:
        section_lv_2 = 5
    elif section_lv_2 < 0:
        section_lv_2 = 0

    if section_lv_2 == 0:
        ats_screen_lcd_services.get_screen_ats()
        LOGGER.info('ATS DISPLAY')
    elif section_lv_2 == 1:
        ats_screen_lcd_services.get_detail_screen1_ats()
        LOGGER.info('ATS DISPLAY DETAIL1')
    elif section_lv_2 == 2:
        ats_screen_lcd_services.get_detail_screen2_ats()
        LOGGER.info('ATS DISPLAY DETAIL2')
    elif section_lv_2 == 3:
        ats_screen_lcd_services.get_detail_screen3_ats()
        LOGGER.info('ATS DISPLAY DETAIL3')
    elif section_lv_2 == 4:
        ats_screen_lcd_services.get_detail_screen4_ats()
        LOGGER.info('ATS DISPLAY DETAIL4')
    elif section_lv_2 == 5:
        ats_screen_lcd_services.get_detail_screen5_ats()
        LOGGER.info('ATS DISPLAY DETAIL5')


def rfid_display():
    rfid_screen_lcd_sevices.get_screen_rfid()
    LOGGER.info('RFID DISPLAY')


def setting_display():
    global section_lv_2
    global section_lv_3
    global button

    try:
        if button == OK and section_lv_3 == -1:
            section_lv_3 = 0

        if section_lv_3 > -1:
            switcher = {
                0: cai_dat_thong_tin,
                1: thoi_gian,
                2: thong_so_mang,
                3: canh_bao,
                4: thiet_bi_ats,
                5: thiet_bi_rfid,
            }
            func = switcher.get(section_lv_2)
            return func()

        elif section_lv_3 == -1:
            if button == UP:
                section_lv_2 -= 1
            elif button == DOWN:
                section_lv_2 += 1
            if section_lv_2 > 5:
                section_lv_2 = 5
            elif section_lv_2 < 0:
                section_lv_2 = 0
            if button == LEFT:
                section_lv_2 = 0
            elif button == RIGHT:
                section_lv_2 = 3

            if section_lv_2 == 0:
                print_lcd('CAI DAT HE THONG',
                          '> Thong tin',
                          'Ngay gio',
                          'Thong so mang')


            elif section_lv_2 == 1:
                print_lcd('CAI DAT HE THONG',
                          'Thong tin',
                          '> Ngay gio',
                          'Thong so mang')
            elif section_lv_2 == 2:
                print_lcd('CAI DAT HE THONG',
                          'Thong tin',
                          'Ngay gio',
                          '> Thong so mang')
            elif section_lv_2 == 3:
                print_lcd('CAI DAT HE THONG',
                          '> Canh bao',
                          'Thiet bi ATS',
                          'Thiet bi RFID')
            elif section_lv_2 == 4:
                print_lcd('CAI DAT HE THONG',
                          'Canh bao',
                          '> Thiet bi ATS',
                          'Thiet bi RFID')
            elif section_lv_2 == 5:
                print_lcd('CAI DAT HE THONG',
                          'Canh bao',
                          'Thiet bi ATS',
                          '> Thiet bi RFID')
        LOGGER.info('Finish rfid_display function')
        LOGGER.info('section_lv_2: %s', str(section_lv_2))
    except Exception as ex:
        LOGGER.error('setting_display function error: %s', ex.message)


def cai_dat_thong_tin():
    global set_string_ok
    global section_lv_4

    LOGGER.info('Finish cai_dat_thong_tin function')


def thoi_gian():
    global section_lv_3
    global section_lv_4
    global button

    if button == OK:
        section_lv_4 += 1

    if section_lv_4 == 1:
        if section_lv_3 == 0:
            print_lcd('Vao cai dat ngay')
            # goi ham xu ly
        elif section_lv_3 == 1:
            print_lcd('Vao cai dat gio')
            # goi ham xu ly

    if button == DOWN:
        section_lv_3 = 1
    elif button == UP:
        section_lv_3 = 0
    if section_lv_4 < 1:
        if section_lv_3 == 0:
            print_lcd('THOI GIAN',
                      '> Ngay',
                      'Gio',
                      '')

        elif section_lv_3 == 1:
            print_lcd('THOI GIAN',
                      'Ngay',
                      '> Gio',
                      '')
    LOGGER.info('Finish thoi_gian function')
    LOGGER.info('section_lv_3: %s', str(section_lv_3))


def thong_so_mang():
    # global section_lv_3
    # global section_lv_4
    global button
    global section_lv_2

    LOGGER.info('Enter thong_so_mang function')

    # Call function xu ly keycode
    choose_config(section_lv_2 + 1)
    listen_key_code(button)

    # SonTH: Comment lai, man hinh con se tu render
    # if button == OK:
    #     section_lv_4 += 1
    # if section_lv_4 == 1:
    #     if section_lv_3 == 0:
    #         print_lcd('cai IP address')
    #         # goi ham xu ly
    #     elif section_lv_3 == 1:
    #         print_lcd('cai subnet mask')
    #         # goi ham xu ly
    #     elif section_lv_3 == 2:
    #         print_lcd('cai Default gateway')
    #         # goi ham xy ly
    #     elif section_lv_3 == 3:
    #         print_lcd('cai Prefered DNS')
    #         # goi ham xu ly
    #     elif section_lv_3 == 4:
    #         print_lcd('cai AlternateDNS')
    #         # goi ham xu ly
    #     return
    #
    # if button == DOWN:
    #     section_lv_3 += 1
    # elif button == UP:
    #     section_lv_3 -= 1
    # if button == RIGHT:
    #     section_lv_3 = 3
    # elif button == LEFT:
    #     section_lv_3 = 0
    # if section_lv_3 > 4:
    #     section_lv_3 = 4
    # elif section_lv_3 < 0:
    #     section_lv_3 = 0
    # if section_lv_4 < 1:
    #     if section_lv_3 == 0:
    #         print_lcd('THONG SO MANG',
    #                   '> IP address',
    #                   'Subnet mask',
    #                   'Default gateway')
    #     elif section_lv_3 == 1:
    #         print_lcd('THONG SO MANG',
    #                   'IP address',
    #                   '> Subnet mask',
    #                   'Default gateway')
    #     elif section_lv_3 == 2:
    #         print_lcd('THONG SO MANG',
    #                   'IP address',
    #                   'Subnet mask',
    #                   '> Default gateway')
    #     elif section_lv_3 == 3:
    #         print_lcd('THONG SO MANG',
    #                   '> Prefered DNS',
    #                   'AlternateDNS',
    #                   '')
    #     elif section_lv_3 == 4:
    #         print_lcd('THONG SO MANG',
    #                   'Prefered DNS',
    #                   '> AlternateDNS',
    #                   '')
    # LOGGER.info('section_lv_3: %s', str(section_lv_3))


def canh_bao():
    # global section_lv_3
    # global section_lv_4
    global button
    global section_lv_2

    LOGGER.info('Enter canh_bao function')
    # Call function xu ly keycode
    choose_config(section_lv_2 + 1)
    listen_key_code(button)

    # SonTH: Comment lai, man hinh con se tu render
    # if button == OK:
    #     section_lv_4 += 1
    #
    # if button == DOWN:
    #     section_lv_3 += 1
    # elif button == UP:
    #     section_lv_3 -= 1
    #
    # if button == LEFT:
    #     section_lv_3 = 0
    # elif button == RIGHT:
    #     section_lv_3 = 2
    # if section_lv_3 > 3:
    #     section_lv_3 = 3
    # elif section_lv_3 < 0:
    #     section_lv_3 = 0
    #
    #
    # if section_lv_4 < 1:
    #     if section_lv_3 == 0:
    #         print_lcd('CANH BAO',
    #                   '> Dien ap luoi',
    #                   'Dien ap may phat',
    #                   '')
    #     elif section_lv_3 == 1:
    #         print_lcd('CANH BAO',
    #                   'Dien ap luoi',
    #                   '> Dien ap may phat',
    #                   '')
    #     elif section_lv_3 == 2:
    #         print_lcd('CANH BAO',
    #                   '> Nhiet do',
    #                   'Do am',
    #                   '')
    #     elif section_lv_3 == 3:
    #         print_lcd('CANH BAO',
    #                   'Nhiet do',
    #                   '> Do am',
    #                   '')
    # LOGGER.info('section_lv_3: %s', str(section_lv_3))


def thiet_bi_ats():
    global section_lv_3
    global section_lv_4
    global section_lv_5
    global button

    ats_setting_lcd_service.listen_key_code(button)

    # LOGGER.info('Enter thiet_bi_ats function')
    # if button == OK:
    #     section_lv_4 += 1
    #
    # if button == DOWN:
    #     section_lv_3 += 1
    # elif button == UP:
    #     section_lv_3 -= 1
    # if section_lv_3 > 2:
    #     section_lv_3 = 2
    # elif section_lv_3 < 0:
    #     section_lv_3 = 0
    #
    # if section_lv_4 < 1:
    #     if section_lv_3 == 0:
    #         print_lcd('THIET BI ATS',
    #                   '> Cam chay M.phat',
    #                   'T.gian cam 1',
    #                   'T.gian cam 2')
    #     elif section_lv_3 == 1:
    #         print_lcd('THIET BI ATS',
    #                   'Cam chay M.phat',
    #                   '> T.gian cam 1',
    #                   'T.gian cam 2')
    #     elif section_lv_3 == 2:
    #         print_lcd('THIET BI ATS',
    #                   'Cam chay M.phat',
    #                   'T.gian cam 1',
    #                   '> T.gian cam 2')
    # LOGGER.info('section_lv_3: %s', str(section_lv_3))


def thiet_bi_rfid():
    # from services.lcd import rfid_setting_lcd_service
    global section_lv_3
    global section_lv_4
    global section_lv_5
    global button

    rfid_setting_lcd_service.listen_key_code(button)

    # LOGGER.info('Enter thiet_bi_rfid function')
    # if button == OK:
    #     section_lv_4 += 1
    #
    # if section_lv_4 == 1:
    #     if section_lv_3 == 0:
    #         print_lcd('cho phep doc')
    #     elif section_lv_3 == 1:
    #         print_lcd('Khong cho phep')
    #     return
    #
    # if button == DOWN:
    #     section_lv_3 = 1
    # elif button == UP:
    #     section_lv_3 = 0
    #
    # if section_lv_4 < 1:
    #     if section_lv_3 == 0:
    #         print_lcd('THIET BI RFID',
    #                   '> Cho phep doc',
    #                   'khong doc',
    #                   '')
    #     elif section_lv_3 == 1:
    #         print_lcd('THIET BI RFID',
    #                   'Cho phep doc',
    #                   '> khong doc',
    #                   '')
    # LOGGER.info('section_lv_3: %s', str(section_lv_3))


def main_menu(bt):
    global section_lv_1, section_lv_2, section_lv_3, section_lv_4, section_lv_5, button, time_count, cycle_flag, time_cycle
    LOGGER.info('Enter main_menu function')
    try:
        if bt != -1:
            button = bt
            time_count = time()
            cycle_flag = True

        if cycle_flag is True:
            time_cycle = time() - time_count

        LOGGER.info('Time out come back to main display: %ds', time_cycle)
        if time_cycle > TIME_OUT:
            time_count = 0
            time_cycle = 0
            section_lv_1 = 0

        if button in MENU_LV_1 and button != section_lv_1 or section_lv_5 == 1:
            section_lv_2 = 0
            section_lv_3 = -1
            section_lv_4 = -1
            section_lv_5 = 0
            ats_setting_lcd_service.reset_params()
            rfid_setting_lcd_service.reset_params()
        select_section_lv1()
        button = -1
    except Exception as ex:
        LOGGER.error('Error at call function in main_menu with message: %s', ex.message)
