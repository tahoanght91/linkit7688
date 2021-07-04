import time

from config import *
from config.common_lcd_services import *
from services.lcd import ats_service
from services.lcd.rfid_screen_lcd_sevices import rfid_screen
from services import lcd_cmd

setting_mode = 0
menu_lv_1 = 0
# class Display:
#     def __init__(self):
#         self.last_menu = '0'
#
#     def main_display(self):
#         try:
#             # USER CODE BEGIN
#             lcd_cmd.clear_display()
#             # self.print_lcd('1.Main display', ROW_3)
#             # button_status[0] = str(MENU[BUTTON_12_EVENT_UP])
#             while True:
#                 if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_11_EVENT_UP]):
#                     # Recheck = {"title": '', "time": '61', "acmTempOutdoor": 0, "acmHumidIndoor": 0, "acmTempIndoor": 0, "isWarning": ""}
#                     # write_to_json(Recheck, './main_screen.json')
#                     self.menu(button_status[0])
#                 # mainScreen = main_screen()
#                 # mainScreen.get_datetime_title_now()
#                 # mainScreen.get_temp_tram()
#                 # mainScreen.get_user_tram()
#                 # time.sleep(3)
#                 # lcd_services['key_code'] = KEYCODE_13
#                 # lcd_services['key_event'] = EVENT_UP
#             # USER CODE END
#         except Exception as ex:
#             LOGGER.error('Error at call function in menu.python with message: %s', ex.message)
#
#     def warning_display(self):
#         try:
#             # USER CODE BEGIN
#             lcd_cmd.clear_display()
#             # warning_service = alarm_lcd_service()
#             while True:
#                 if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_12_EVENT_UP]):
#                     LOGGER.info('Send button value : %s', str(button_status[0]))
#                     self.menu(button_status[0])
#                 # else:
#                     # warning_service.check_alarm(tel_lcd=telemetries)
#                 time.sleep(3)
#             # USER CODE END
#         except Exception as ex:
#             LOGGER.error('Error at call function in menu.python with message: %s', ex.message)
#
#     def security_sensor_info_display(self):
#         # USER CODE BEGIN
#         lcd_cmd.clear_display()
#         lcd_cmd.print_lcd('3. Secure sensor', ROW_1)
#         while True:
#             if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_31_EVENT_UP]):
#                 LOGGER.info('Send button value : %s', str(button_status[0]))
#                 self.menu(button_status[0])
#         # USER CODE END
#
#     def air_info_display(self):
#         # USER CODE BEGIN
#         lcd_cmd.clear_display()
#         lcd_cmd.print_lcd('4. Air condition', ROW_1)
#         while True:
#             if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_13_EVENT_UP]):
#                 LOGGER.info('Send button value : %s', str(button_status[0]))
#                 self.menu(button_status[0])
#             # lcd_services['key_code'] = KEYCODE_11
#             # lcd_services['key_event'] = EVENT_UP
#         # USER CODE END
#
#     def ats_display(self):
#         # USER CODE BEGIN
#         goto_display = 1
#         lcd_cmd.clear_display()
#         ats_service.header()
#         while True:
#             if button_status[0] in MENU and button_status[0] != BUTTON_35_EVENT_UP:
#                 LOGGER.info('Send button value : %s', str(button_status[0]))
#                 self.menu(button_status[0])
#                 break
#             if button_status[0] == BUTTON_25_EVENT_UP:
#                 goto_display = 2
#                 lcd_cmd.clear_display()
#             elif button_status[0] == BUTTON_23_EVENT_UP:
#                 goto_display = 1
#                 lcd_cmd.clear_display()
#
#             if goto_display == 1:
#                 ats_service.display1()
#             elif goto_display == 2:
#                 ats_service.display2()
#             time.sleep(3)
#         # USER CODE END
#
#     def rfid_display(self):
#         try:
#             lcd_cmd.clear_display()
#             # self.print_lcd('7. RFID display', ROW_1)
#             rfidScreen = rfid_screen()
#             rfidScreen.get_title_rfid()
#             while True:
#                 if button_status[0] in MENU and button_status[0] != str(MENU[BUTTON_15_EVENT_UP]):
#                     LOGGER.info('Send button value : %s', str(button_status[0]))
#                     self.menu(button_status[0])
#                 rfidScreen.get_info_rfid()
#                 time.sleep(3)
#         except Exception as ex:
#             LOGGER.error('Error at rfid_display function with message: %s', ex.message)



def menu_list(number_menu):
    global menu_lv_1

    try:
        LOGGER.info('Enter menu_list function')
        switcher = {
            BUTTON_11_EVENT_UP: main_display,
            BUTTON_12_EVENT_UP: warning_display,
            BUTTON_31_EVENT_UP: security_sensor_info_display,
            BUTTON_13_EVENT_UP: air_info_display,
            BUTTON_35_EVENT_UP: ats_display,
            BUTTON_33_EVENT_UP: setting_display,
            BUTTON_15_EVENT_UP: rfid_display
        }
        if number_menu in MENU_LV_1:
            menu_lv_1 = number_menu
        else:
            pass
        LOGGER.info('show display %s', str(number_menu))
        func = switcher.get(menu_lv_1)
        return func()
    except Exception as ex:
        LOGGER.info('menu_list function error: %s', ex.message)


def main_display():
    pass

def warning_display():
    pass

def security_sensor_info_display():
    pass

def air_info_display():
    pass

def ats_display():
    pass

def setting_display():
    global setting_mode
    try:
        if button_status[0] == BUTTON_14_EVENT_UP:
            setting_mode += 1
        elif button_status[0] == BUTTON_34_EVENT_UP:
            setting_mode -= 1
        elif button_status[0] == BUTTON_23_EVENT_UP:
            setting_mode = 0
        elif button_status[0] == BUTTON_25_EVENT_UP:
            setting_mode = 3
        if setting_mode > 5:
            setting_mode = 5
        elif setting_mode < 0:
            setting_mode = 0
        LOGGER.info('Enter setting_display function')
        LOGGER.info('mode setting : %s', str(setting_mode))
        # vao man hinh setting thong so da chon
        if button_status[0] == BUTTON_24_EVENT_UP:
            LOGGER.info('Send button value : %s', str(button_status[0]))
            button_status[0] = None
        if setting_mode == 0:
            lcd_cmd.print_lcd('CAI DAT HE THONG',
                              '-> TT he thong  ',
                              '   Thoi gian    ',
                              '   Thong so mang')
        elif setting_mode == 1:
            lcd_cmd.print_lcd('CAI DAT HE THONG',
                              '   TT he thong  ',
                              '-> Thoi gian    ',
                              '   Thong so mang')
        elif setting_mode == 2:
            lcd_cmd.print_lcd('CAI DAT HE THONG',
                              '   TT he thong  ',
                              '   Thoi gian    ',
                              '-> Thong so mang')
        elif setting_mode == 3:
            lcd_cmd.print_lcd('CAI DAT HE THONG',
                              '-> Canh bao     ',
                              '   ATS          ',
                              '   Phu kien     ')
        elif setting_mode == 4:
            lcd_cmd.print_lcd('CAI DAT HE THONG',
                              '   Canh bao     ',
                              '-> ATS          ',
                              '   Phu kien     ')
        elif setting_mode == 5:
            lcd_cmd.print_lcd('CAI DAT HE THONG',
                              '   Canh bao     ',
                              '   ATS          ',
                              '-> Phu kien     ')
        button_status[0] = None
    except Exception as ex:
        LOGGER.info('switch setting menu false: %s', ex.message)

def rfid_display():
    pass
