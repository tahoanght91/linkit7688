from config import *
from config.common_lcd_services import *

UPDATE_VALUE = 5
def add_cmd_lcd(dict_cmd):
    cmd = ''
    for i in dict_cmd:
        cmd += dict_cmd[i]
    commands[UPDATE_VALUE] += cmd

def creat_cmd_rule(dict_cmd, string, row):
    dict_cmd[str(row)] = str(string) + SALT_DOLLAR_SIGN + str(row) + END_CMD

class Display:
    def __init__(self):
        self.last_menu = '0'

    def clear_display(self):
        lcd_services.clear()

    def print_lcd(self, string, row):
        LOGGER.info('Enter print_lcd function')
        creat_cmd_rule(dict_cmd, string, row)
        add_cmd_lcd(dict_cmd)
        LOGGER.info('Exit print_lcd function')

    def main_display(self):
        self.print_lcd('1.Main display', ROW_3)

    def warning_display(self):
        self.print_lcd('2.Warningdisplay', ROW_3)

    def security_sensor_info_display(self):
        self.print_lcd('3. Secure sensor', ROW_3)

    def air_info_display(self):
        self.print_lcd('4. Air condition', ROW_3)

    def ats_display(self):
        self.print_lcd('5. ATS display', ROW_3)

    def rfid_display(self):
        self.print_lcd('7. RFID display', ROW_3)

    def menu(self, number_menu):
        if number_menu in MENU:
            self.last_menu = MENU[number_menu]
            return getattr(self, 'case_' + str(MENU[number_menu]))()
        else:
            return getattr(self, 'case_' + str(self.last_menu))()

    def case_0(self):
        return self.main_display()

    def case_1(self):
        return self.warning_display()

    def case_2(self):
        return self.security_sensor_info_display()

    def case_3(self):
        return self.air_info_display()

    def case_4(self):
        return self.ats_display()

    def case_5(self):
        return self.setting_display()

    def case_6(self):
        return self.rfid_display()

    def setting_display(self):
        button = Button()
        mode_setting = 0

        while True:
            if button.check_button(lcd_services) == BUTTON_14_EVENT_UP:
                mode_setting += 1
            elif button.check_button(lcd_services) == BUTTON_34_EVENT_UP:
                mode_setting -= 1
            if mode > 5:
                mode = 0
            elif mode < 0:
                mode = 5
            self.setting_menu(mode)

    def setting_menu(self, setting_mode):
        return getattr(self, 'setting_menu_' + str(setting_mode))()

    def setting_menu_0(self):
        self.print_lcd('CAI DAT HE THONG', ROW_1)
        self.print_lcd('-> TT he thong  ', ROW_2)
        self.print_lcd('   Thoi gian    ', ROW_3)
        self.print_lcd('   Thong so mang', ROW_4)

    def setting_menu_1(self):
        self.print_lcd('CAI DAT HE THONG', ROW_1)
        self.print_lcd('   TT he thong  ', ROW_2)
        self.print_lcd('-> Thoi gian    ', ROW_3)
        self.print_lcd('   Thong so mang', ROW_4)

    def setting_menu_2(self):
        self.print_lcd('CAI DAT HE THONG', ROW_1)
        self.print_lcd('   TT he thong  ', ROW_2)
        self.print_lcd('   Thoi gian    ', ROW_3)
        self.print_lcd('-> Thong so mang', ROW_4)

    def setting_menu_3(self):
        self.print_lcd('CAI DAT HE THONG', ROW_1)
        self.print_lcd('-> Canh bao     ', ROW_2)
        self.print_lcd('   ATS          ', ROW_3)
        self.print_lcd('   Phu kien     ', ROW_4)

    def setting_menu_4(self):
        self.print_lcd('CAI DAT HE THONG', ROW_1)
        self.print_lcd('   Canh bao     ', ROW_2)
        self.print_lcd('-> ATS          ', ROW_3)
        self.print_lcd('   Phu kien     ', ROW_4)

    def setting_menu_5(self):
        self.print_lcd('CAI DAT HE THONG', ROW_1)
        self.print_lcd('   Canh bao     ', ROW_2)
        self.print_lcd('   ATS          ', ROW_3)
        self.print_lcd('-> Phu kien     ', ROW_4)


class Button():
    def __init__(self):
        self.button = 0

    def check_button(self, dct_lcd_service):
        key_code = dct_lcd_service['key_code']
        key_event = dct_lcd_service['key_event']

        for i in range(len(LIST_KEYCODE)):
            if key_code == LIST_KEYCODE[i]:
                index_key = i
                break

        if key_event == EVENT_UP:
            event = EVENT_UP_BT
        elif key_event == EVENT_HOLD:
            event = EVENT_HOLD_BT
        self.button = event * index_key

        return str(self.button)
