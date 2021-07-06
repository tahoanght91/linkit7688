from config import *
from config.common import END_CMD, CLEAR
from config.common_lcd_services import *

section_lv_1 = -1
section_lv_2 = 0
section_lv_3 = -1
section_lv_4 = -1
section_lv_5 = -1

button = 0
set_string_ok = 0


def print_lcd(str1, str2, str3, str4):
    try:
        LOGGER.info('Send message print_lcd on lcd')
        str1 = str1 + SALT_DOLLAR_SIGN + str(ROW_1) + END_CMD
        str2 = str2 + SALT_DOLLAR_SIGN + str(ROW_1) + END_CMD
        str3 = str3 + SALT_DOLLAR_SIGN + str(ROW_1) + END_CMD
        str4 = str4 + SALT_DOLLAR_SIGN + str(ROW_1) + END_CMD

        cmd_lcd = {1: [5, str1], 2: [5, str2], 3: [5, str3], 4: [5, str4]}
        LOGGER.info('Send message print_lcd on lcd: %s', str(cmd_lcd))
    except Exception as ex:
        LOGGER.info('print_lcd_lcd function error: %s', ex.message)


def clear_display():
    cmd_lcd[CLEAR] = ''


def select_section_lv1():
    global section_lv_1
    global section_lv_2
    global button

    if button in MENU_LV_1:
        section_lv_1 = MENU_LV_1.index(button)
    switcher = {
        0: main_display,
        1: warning_display,
        2: security_sensor_info_display,
        3: air_info_display,
        4: ats_display,
        5: setting_display,
        6: rfid_display
    }

    func = switcher.get(section_lv_1)
    return func()


def main_display():
    # goi ham hien thi
    print_lcd('MAKE IN MOBIFONE',
              'TIME',
              'VALUE',
              'ID')


def warning_display():
    print_lcd('BAN TIN CANH BAO',
              'Ten canh bao',
              'Thoi gian',
              '')
    # goi ham hien thi


def security_sensor_info_display():
    global section_lv_2

    if button == LEFT:
        section_lv_2 = 0
    elif button == RIGHT:
        section_lv_2 = 1

    if section_lv_2 == 0:
        print_lcd('CAM BIEN AN NINH',
                  'Khoi: 0',
                  'Chay: 0',
                  'Ngap nuoc: 0')
        # goi ham hien thi
    if section_lv_2 == 1:
        print_lcd('CAM BIEN AN NINH',
                  'Ngap nuoc: 0',
                  'Cua: 0',
                  'chuyen dong: 1')
        # goi ham hien thi


def air_info_display():
    print_lcd('BAN TIN DIEU HOA',
              'DH1: bat, HD2:Tat',
              'Quat:Bat',
              'Che do: Auto')
    # goi ham hien thi


def ats_display():
    global section_lv_2

    if button == LEFT:
        section_lv_2 = 0
    elif button == RIGHT:
        section_lv_2 = 1
    if section_lv_2 == 0:
        print_lcd('THONG TIN ATS',
                  'Ket noi',
                  'Nguon: Dien luoi',
                  '')
        # goi ham hien thi
    elif section_lv_2 == 1:
        print_lcd('THONG TIN ATS',
                  '220V 220V 220V',
                  '220V 220V 220V',
                  '3.0A 4.0A 4.6A')
        # goi ham hien thi


def rfid_display():
    print_lcd('THONG TIN RFID',
              'Ket noi',
              'Ngay gio',
              'ma the')
    pass


def setting_display():
    global section_lv_2
    global section_lv_3
    global button

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


def cai_dat_thong_tin():
    global set_string_ok
    global section_lv_4

    pass


def thoi_gian():
    global section_lv_3
    global section_lv_4
    global button

    if button == OK:
        section_lv_4 += 1

    if section_lv_4 == 1:
        if section_lv_3 == 0:
            print_lcd('Vao man hinh cai dat ngay')
            # goi ham xu ly
        elif section_lv_3 == 1:
            print_lcd('Vao man hinh cai dat gio')
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


def thong_so_mang():
    global section_lv_3
    global section_lv_4
    global button

    if button == OK:
        section_lv_4 += 1

    if section_lv_4 == 1:
        if section_lv_3 == 0:
            print_lcd('Vao cai dat IP address')
            # goi ham xu ly
        elif section_lv_3 == 1:
            print_lcd('Vao cai dat subnet mask')
            # goi ham xu ly
        elif section_lv_3 == 2:
            print_lcd('Vao cai dat Default gateway')
            # goi ham xy ly
        elif section_lv_3 == 3:
            print_lcd('Vao cai dat Prefered DNS')
            # goi ham xu ly
        elif section_lv_3 == 4:
            print_lcd('Vao cai dat AlternateDNS')
            # goi ham xu ly
        return

    if button == DOWN:
        section_lv_3 += 1
    elif button == UP:
        section_lv_3 -= 1
    if button == RIGHT:
        section_lv_3 = 3
    elif button == LEFT:
        section_lv_3 = 0
    if section_lv_3 > 4:
        section_lv_3 = 4
    elif section_lv_3 < 0:
        section_lv_3 = 0
    if section_lv_4 < 1:
        if section_lv_3 == 0:
            print_lcd('THONG SO MANG',
                      '> IP address',
                      'Subnet mask',
                      'Default gateway')
        elif section_lv_3 == 1:
            print_lcd('THONG SO MANG',
                      'IP address',
                      '> Subnet mask',
                      'Default gateway')
        elif section_lv_3 == 2:
            print_lcd('THONG SO MANG',
                      'IP address',
                      'Subnet mask',
                      '> Default gateway')
        elif section_lv_3 == 3:
            print_lcd('THONG SO MANG',
                      '> Prefered DNS',
                      'AlternateDNS',
                      '')
        elif section_lv_3 == 4:
            print_lcd('THONG SO MANG',
                      'Prefered DNS',
                      '> AlternateDNS',
                      '')


def canh_bao():
    global section_lv_3
    global section_lv_4
    global button

    if button == OK:
        section_lv_4 += 1

    if section_lv_4 == 1:
        if section_lv_3 == 0:
            print_lcd('Vao cai dat Nguong AC cao')
            # goi ham xu ly
        elif section_lv_3 == 1:
            print_lcd('Vao cai dat Nguong AC thap')
            # goi ham xu ly
        return

    if button == DOWN:
        section_lv_3 = 1
    elif button == UP:
        section_lv_3 = 0

    if section_lv_4 < 1:
        if section_lv_3 == 0:
            print_lcd('CANH BAO ',
                      '> Nguong AC cao',
                      'Nguong AC thap',
                      '')
        elif section_lv_3 == 1:
            print_lcd('CANH BAO ',
                      'Nguong AC cao',
                      '> Nguong AC thap',
                      '')


def thiet_bi_ats():
    global section_lv_3
    global section_lv_4
    global section_lv_5
    global button

    if button == OK:
        section_lv_4 += 1

    if section_lv_4 == 1:
        if section_lv_3 == 0:
            print_lcd('Chay auto')
            # goi ham xu ly
        elif section_lv_3 == 1:
            print_lcd('Chay dien luoi')
            # goi ham xu ly
        elif section_lv_3 == 2:
            print_lcd('Chay may phat')
        # section_lv_5 = 0
        # save()
        return

    if button == DOWN:
        section_lv_3 += 1
    elif button == UP:
        section_lv_3 -= 1
    if section_lv_3 > 2:
        section_lv_3 = 2
    elif section_lv_3 < 0:
        section_lv_3 = 0

    if section_lv_4 < 1:
        if section_lv_3 == 0:
            print_lcd('THIET BI ATS',
                      '> Tu chay',
                      'Dien luoi',
                      'May phat')
        elif section_lv_3 == 1:
            print_lcd('THIET BI ATS',
                      'Tu chay',
                      '> Dien luoi',
                      'May phat')
        elif section_lv_3 == 2:
            print_lcd('THIET BI ATS',
                      'Tu chay',
                      'Dien luoi',
                      '> May phat')


def thiet_bi_rfid():
    global section_lv_3
    global section_lv_4
    global section_lv_5
    global button

    if button == OK:
        section_lv_4 += 1

    if section_lv_4 == 1:
        if section_lv_3 == 0:
            print_lcd('cho phep doc')
        elif section_lv_3 == 1:
            print_lcd('Khong cho phep')
        # section_lv_5 = 0
        # save()
        # goi ham xu ly
        return

    if button == DOWN:
        section_lv_3 = 1
    elif button == UP:
        section_lv_3 = 0

    if section_lv_4 < 1:
        if section_lv_3 == 0:
            print_lcd('THIET BI RFID',
                      '> Cho phep doc',
                      'khong doc',
                      '')
        elif section_lv_3 == 1:
            print_lcd('THIET BI RFID',
                      'Cho phep doc',
                      '> khong doc',
                      '')

    #
    #
    # while True:
    #     if section_lv_1 == -1:
    #         main_display()
    #     button = str(input('nhấn nút:'))
    #     if button in MAP and button != section_lv_1 or section_lv_5 == 1:
    #         section_lv_2 = 0
    #         section_lv_3 = -1
    #         section_lv_4 = -1
    #         section_lv_5 = 0
    #
    #     select_section_lv1()
    #     button = -1
    #
