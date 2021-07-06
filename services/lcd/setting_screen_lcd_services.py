from config import button_status, LOGGER
from config.common_lcd_services import *
from services import lcd_cmd


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
                              '> Thong tin     ',
                              'Ngay gio        ',
                              'Thong so mang   ')
        elif setting_mode == 1:
            lcd_cmd.print_lcd('CAI DAT HE THONG',
                              'Thong tin       ',
                              '> Ngay gio      ',
                              'Thong so mang   ')
        elif setting_mode == 2:
            lcd_cmd.print_lcd('CAI DAT HE THONG',
                              '   TT he thong  ',
                              '   Thoi gian    ',
                              '> Thong so mang ')
        elif setting_mode == 3:
            lcd_cmd.print_lcd('CAI DAT HE THONG',
                              '> Canh bao      ',
                              'Thiet bi ATS    ',
                              'Thiet bi RFID   ')
        elif setting_mode == 4:
            lcd_cmd.print_lcd('CAI DAT HE THONG',
                              '  Canh bao      ',
                              '> Thiet bi ATS  ',
                              'Thiet bi RFID   ')
        elif setting_mode == 5:
            lcd_cmd.print_lcd('CAI DAT HE THONG',
                              '  Canh bao      ',
                              'Thiet bi ATS    ',
                              '> Thiet bi RFID ')
        button_status[0] = None
    except Exception as ex:
        LOGGER.info('switch setting menu false: %s', ex.message)