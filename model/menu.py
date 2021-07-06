import json
from config import *
from services import lcd_cmd
from services.lcd_cmd import print_lcd

setting_mode = 0
menu_lv_1 = 0
menu_lv_2 = 0
menu_lv_3 = 0
menu_lv_4 = 0
menu_lv_5 = 0


def write_json():
    global menu_lv_1, menu_lv_2, menu_lv_3, menu_lv_4, menu_lv_5
    pass

def menu(button):
    global menu_lv_1, menu_lv_2, menu_lv_3, menu_lv_4, menu_lv_5

    with open('./config/menu.json') as json_file:
        data = json.load(json_file)
    menu_lv_1 = data["menu_lv1"]
    menu_lv_2 = data["menu_lv2"]
    menu_lv_3 = data["menu_lv3"]
    menu_lv_4 = data["menu_lv4"]
    menu_lv_5 = data["menu_lv5"]




# def menu_lv1():
#     global menu_lv_1
#
#     try:
#         LOGGER.info('Enter menu_list function')
#         switcher = {
#             0: main_display,
#             1: warning_display,
#             2: security_sensor_info_display,
#             3: air_info_display,
#             4: ats_display,
#             5: setting_display,
#             6: rfid_display
#         }
#
#         LOGGER.info('show display %s', str(menu_lv_1))
#         func = switcher.get(menu_lv_1)
#         return func()
#     except Exception as ex:
#         LOGGER.info('menu_list function error: %s', ex.message)


def main_display():
    # goi ham hien thi
    lcd_cmd.print_lcd('MAKE IN MOBIFONE',
                      'TIME',
                      'VALUE',
                      'ID')


def warning_display():
    lcd_cmd.print_lcd('BAN TIN CANH BAO',
                      'Ten canh bao',
                      'Thoi gian',
                      '')
    # goi ham hien thi


def security_sensor_info_display():
    global menu_lv_2

    if menu_lv_2 == 0:
        print_lcd('CAM BIEN AN NINH',
                  'Khoi: 0',
                  'Chay: 0',
                  'Ngap nuoc: 0')
        # goi ham hien thi
    if menu_lv_2 == 1:
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
    global menu_lv_2
    if menu_lv_2 == 0:
        print_lcd('THONG TIN ATS',
                  'Ket noi',
                  'Nguon: Dien luoi',
                  '')
        # goi ham hien thi
    elif menu_lv_2 == 1:
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
    global menu_lv_2
    global menu_lv_3

    if menu_lv_2 == 0:
        print_lcd('CAI DAT HE THONG',
                  '> Thong tin',
                  'Ngay gio',
                  'Thong so mang')
        # goi ham
    elif menu_lv_2 == 1:
        print_lcd('CAI DAT HE THONG',
                  'Thong tin',
                  '> Ngay gio',
                  'Thong so mang')
        # goi ham
    elif menu_lv_2 == 2:
        print_lcd('CAI DAT HE THONG',
                  'Thong tin',
                  'Ngay gio',
                  '> Thong so mang')
        # goi ham
    elif menu_lv_2 == 3:
        print_lcd('CAI DAT HE THONG',
                  '> Canh bao',
                  'Thiet bi ATS',
                  'Thiet bi RFID')
        # goi ham
    elif menu_lv_2 == 4:
        print_lcd('CAI DAT HE THONG',
                  'Canh bao',
                  '> Thiet bi ATS',
                  'Thiet bi RFID')
        # goi ham
    elif menu_lv_2 == 5:
        print_lcd('CAI DAT HE THONG',
                  'Canh bao',
                  'Thiet bi ATS',
                  '> Thiet bi RFID')
        # goi ham

    switcher = {
        0: cai_dat_thong_tin,
        1: thoi_gian,
        2: thong_so_mang,
        3: canh_bao,
        4: thiet_bi_ats,
        5: thiet_bi_rfid,
    }
    LOGGER.info('show display %s', str(menu_lv_3))
    func = switcher.get(menu_lv_3)
    return func()

def cai_dat_thong_tin():
    # goi ham cai dat
    pass

def thoi_gian():
    global menu_lv_4

    if menu_lv_4:
        print_lcd('THOI GIAN',
                  '> Ngay',
                  'Gio',
                  '')
        # goi ham xu ly
    else:
        print_lcd('THOI GIAN',
                  'Ngay',
                  '> Gio',
                  '')
        # goi ham xu ly

def thong_so_mang():
    global menu_lv_4

    if menu_lv_4 == 0:
        print_lcd('THONG SO MANG',
                  '> IP address',
                  'Subnet mask',
                  'Default gateway')
    elif menu_lv_4 == 1:
        print_lcd('THONG SO MANG',
                  'IP address',
                  '> Subnet mask',
                  'Default gateway')
    elif menu_lv_4 == 2:
        print_lcd('THONG SO MANG',
                  'IP address',
                  'Subnet mask',
                  '> Default gateway')
    elif menu_lv_4 == 3:
        print_lcd('THONG SO MANG',
                  '> Prefered DNS',
                  'AlternateDNS',
                  '')
    elif menu_lv_4 == 4:
        print_lcd('THONG SO MANG',
                  'Prefered DNS',
                  '> AlternateDNS',
                  '')

def canh_bao():
    global menu_lv_4

    if menu_lv_4:
        print_lcd('CANH BAO',
                  '> Nguong AC cao',
                  'Nguong AC thap',
                  '')
    else:
        print_lcd('CANH BAO',
                  'Nguong AC cao',
                  '> Nguong AC thap',
                  '')

def thiet_bi_ats():
    global menu_lv_4

    if menu_lv_4 == 0:
        print_lcd('THIET BI ATS',
                  '> Tu chay',
                  'Dien luoi',
                  'May phat')
    elif menu_lv_4 == 1:
        print_lcd('THIET BI ATS',
                  'Tu chay',
                  '> Dien luoi',
                  'May phat')
    elif menu_lv_4 == 2:
        print_lcd('THIET BI ATS',
                  'Tu chay',
                  'Dien luoi',
                  '> May phat')

def thiet_bi_rfid():
    global menu_lv_4

    if menu_lv_4 == 0:
        print_lcd('THIET BI RFID',
                  '> Cho phep doc',
                  'khong doc',
                  '')
    elif menu_lv_4 == 1:
        print_lcd('THIET BI RFID',
                  'Cho phep doc',
                  '> khong doc',
                  '')

def save():
    global menu_lv_5

    if menu_lv_5:
        print_lcd('XAC NHAN LUU',
                  '> Co',
                  'Khong',
                  '')
        print_lcd('XAC NHAN LUU',
                  'Co',
                  '> Khong',
                  '')

