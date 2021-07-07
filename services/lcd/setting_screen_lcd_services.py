from config import *
from config.common import UPDATE_VALUE
from config.common_lcd_services import *
from control import process_cmd_lcd


class __IPv4:
    def __init__(self):
        self.ip = ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_']

    def get_ip(self):
        return "{0}{1}{2}.{3}{4}{5}.{6}{7}{8}.{9}{10}{11}".format(self.ip[0], self.ip[1], self.ip[2]
                                                                  , self.ip[3], self.ip[4], self.ip[5]
                                                                  , self.ip[6], self.ip[7], self.ip[8]
                                                                  , self.ip[9], self.ip[10], self.ip[11])

    def get_oct(self):
        return [int("{0}{1}{2}".format(self.ip[0] if self.ip[0] != '_' else 0
                                       , self.ip[1] if self.ip[1] != '_' else 0
                                       , self.ip[2] if self.ip[2] != '_' else 0))
            , int("{0}{1}{2}".format(self.ip[3] if self.ip[3] != '_' else 0
                                     , self.ip[4] if self.ip[4] != '_' else 0
                                     , self.ip[5] if self.ip[5] != '_' else 0))
            , int("{0}{1}{2}".format(self.ip[6] if self.ip[6] != '_' else 0
                                     , self.ip[7] if self.ip[7] != '_' else 0
                                     , self.ip[8] if self.ip[8] != '_' else 0))
            , int("{0}{1}{2}".format(self.ip[9] if self.ip[9] != '_' else 0
                                     , self.ip[10] if self.ip[10] != '_' else 0
                                     , self.ip[11] if self.ip[11] != '_' else 0))]


class __Alarm:
    def __init__(self):
        self.alarm = ['_', '_', '_']

    def get_alarm(self):
        return "{0}{1}{2}".format(self.alarm[0], self.alarm[1], self.alarm[2])


# Man hinh setting nao
screen_setting_idx = 0
# Vi tri man hinh hien tai
screen_idx = 0
# con tro vi tri tren man hinh
pointer_idx = 0
# Network
network = 0
# Alarm
alarm = 0
# Idx man hinh
selection_setting = {
    "main": 0,
    "info": 1,
    "time": 2,
    "network": 3,
    "alarm": 4,
    "ats": 5,
    "rfid": 6
}

selection_setting_network = {
    "main": 0,
    "assign_ip": 1,
    "confirm_assign_ip": 2
}

selection_setting_alarm = {
    "main": 0,
    "choose_high_low": 1,
    "assign_alarm": 2,
    "confirm_assign_alarm": 3
}

screen_setting_alarm = {
    "ac": 0,
    "temp": 1,
    "humidity": 2
}

confirm = {
    "yes": 0,
    "no": 1
}

selection_chosen = [0, 0, 0, 0]


# Call khi chon setting can cau hinh
def choose_config(setting_idx):
    global screen_setting_idx
    screen_setting_idx = setting_idx


def reset_parameter():
    # call moi khi quay lai man hinh main config
    global pointer_idx, screen_idx
    pointer_idx = 0
    screen_idx = 0


# SonTH: Config network
# Main cua man hinh network
def call_screen_network():
    try:
        switcher = [
            {
                "row_2": '> IP address',
                "row_3": 'Subnet mask',
                "row_4": 'Default gateway'
            },
            {
                "row_2": 'IP address',
                "row_3": '> Subnet mask',
                "row_4": 'Default gateway'
            },
            {
                "row_2": 'IP address',
                "row_3": 'Subnet mask',
                "row_4": '> Default gateway'
            },
            {
                "row_2": '> Prefered DNS',
                "row_3": 'Alternate DNS',
                "row_4": ''
            },
            {
                "row_2": 'Prefered DNS',
                "row_3": '> Alternate DNS',
                "row_4": ''
            }
        ]
        # Update text
        process_cmd_lcd(ROW_1, UPDATE_VALUE, 'THONG SO MANG')
        process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[selection_chosen[screen_idx]]['row_2'])
        process_cmd_lcd(ROW_3, UPDATE_VALUE, switcher[selection_chosen[screen_idx]]['row_3'])
        process_cmd_lcd(ROW_4, UPDATE_VALUE, switcher[selection_chosen[screen_idx]]['row_4'])
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)


def refresh_screen_assign_ip_address():
    try:
        global network
        network = get_net_info()
        switcher = [
            {
                "row_2": 'IP address'
            },
            {
                "row_2": 'Subnet mask'
            },
            {
                "row_2": 'Default gateway'
            },
            {
                "row_2": 'Prefered DNS'
            },
            {
                "row_2": 'Alternate DNS'
            }
        ]
        confirm = [
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
        if screen_idx % 2:
            # Man hinh xac nhan luu
            process_cmd_lcd(ROW_1, UPDATE_VALUE, 'XAC NHAN LUU')
            process_cmd_lcd(ROW_2, UPDATE_VALUE, confirm[pointer_idx]["row_2"])
            process_cmd_lcd(ROW_2, UPDATE_VALUE, confirm[pointer_idx]["row_3"])
        else:
            # Man hinh nhap ip - subnet - ...
            process_cmd_lcd(ROW_1, UPDATE_VALUE, 'THONG SO MANG')
            process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[selection_chosen[screen_idx]])
            process_cmd_lcd(ROW_3, UPDATE_VALUE, network.get_ip())

        LOGGER.info('ASSIGN IP SCREEN: %s', str(network.get_ip()))
        # Update nhap nhay
        # ...
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)


def get_net_info():
    # Todo: Get thong tin ip dang su dung, neu khong co thi tra ve null
    # result = {
    #    "IP": __ipv4('', '', '', ''),
    #    "SUBNET": __ipv4('', '', '', ''),
    #    "HOST": __ipv4('', '', '', '')
    # }
    result = __IPv4()

    # Get thong tin ip dang su dung
    # ...

    # Tam fake bang 192.168.1.11
    result.ip = [1, 9, 2, 1, 6, 8, '', '', 1, '', 1, 1]
    return result


def get_alarm_info():
    # Todo: Get thong tin alarm dang su dung, neu khong co thi tra ve null
    result = __Alarm()

    # Get thong tin alarm dang su dung
    # ...

    # Tam fake bang 77
    result.ip = [7, 7, '_']
    return result


def get_next_number(keycode, number):
    if keycode == BUTTON_34_EVENT_UP:
        return 0 if number > 9 else number + 1
    else:
        return 9 if number == 0 else number - 1


# Register func nay
def listen_key_code(keycode):
    if screen_setting_idx == selection_setting["network"]:
        if screen_idx == selection_setting_network["main"]:
            # Neu la man hinh main config
            main_network_listen_key(keycode)
        else:
            # Neu la man hinh cau hinh thong so
            assign_ip_listen_key(keycode)

        # refresh screen
        refresh_screen_assign_ip_address()
    elif screen_setting_idx == selection_setting["alarm"]:
        if screen_idx == selection_setting_alarm["main"] or screen_idx == selection_setting_alarm[
            "choose_high_low"] or screen_idx == selection_setting_alarm[
            "confirm_assign_alarm"]:
            alarm_selection_listen_key()
        else:
            # Neu la man hinh cau hinh thong so
            assign_alarm_listen_key()
        return
    else:
        return


def main_network_listen_key(keycode):
    global pointer_idx, screen_idx
    if keycode == BUTTON_34_EVENT_UP:
        # key down
        pointer_idx = 4 if pointer_idx == 4 else pointer_idx + 1
    elif keycode == BUTTON_14_EVENT_UP:
        # key up
        pointer_idx = 0 if pointer_idx == 0 else pointer_idx - 1
    elif keycode == BUTTON_24_EVENT_UP:
        # key ok
        selection_chosen[screen_idx] = pointer_idx
        screen_idx = 0 if screen_idx == 2 else screen_idx + 1
        # refresh gia tri pointer index
        pointer_idx = 0
        # refresh man hinh
        refresh_screen_assign_ip_address()
    else:
        return


def main_alarm_listen_key(keycode):
    global pointer_idx, screen_idx
    # main co 3 dong, choose co 2 dong
    max_pointer_idx = 3 if screen_idx == selection_setting_alarm["alarm"] else 2
    if keycode == BUTTON_34_EVENT_UP:
        # key down
        pointer_idx = max_pointer_idx if pointer_idx == max_pointer_idx else pointer_idx + 1
    elif keycode == BUTTON_14_EVENT_UP:
        # key up
        pointer_idx = 0 if pointer_idx == 0 else pointer_idx - 1
    elif keycode == BUTTON_24_EVENT_UP:
        # key ok
        selection_chosen[screen_idx] = pointer_idx
        screen_idx = 0 if screen_idx == 3 else screen_idx + 1
        # refresh gia tri pointer index
        pointer_idx = 0
        # refresh man hinh
        call_screen_alarm_selection()
    else:
        return


def assign_ip_listen_key(keycode):
    global pointer_idx, screen_idx
    if keycode == BUTTON_23_EVENT_UP:
        # key left
        pointer_idx -= 1
        pointer_idx = pointer_idx if pointer_idx > 0 else 0
    elif keycode == BUTTON_25_EVENT_UP:
        # key right
        maxLength = 3
        pointer_idx += 1
        pointer_idx = pointer_idx if pointer_idx < maxLength else maxLength
    elif keycode == BUTTON_14_EVENT_UP or keycode == BUTTON_34_EVENT_UP:
        # key up or key down
        network.ip[pointer_idx] = get_next_number(keycode, network.ip[pointer_idx])
    elif keycode == BUTTON_24_EVENT_UP:
        # key ok
        selection_chosen[screen_idx] = pointer_idx
        if screen_idx == selection_setting_network["assign_ip"]:
            screen_idx += 1
            pointer_idx = 0
        else:
            if pointer_idx == confirm["yes"]:
                save_ip()
                pointer_idx = 0
                screen_idx = selection_setting_network["main"]
                # refresh screen
                call_screen_network()
                return
            else:
                return
    else:
        return
    # refresh screen
    refresh_screen_assign_ip_address()


def alarm_selection_listen_key(keycode):
    global pointer_idx, screen_idx
    if keycode == BUTTON_34_EVENT_UP:
        # key down
        pointer_idx = 2 if pointer_idx == 2 else pointer_idx + 1
    elif keycode == BUTTON_14_EVENT_UP:
        # key up
        pointer_idx = 0 if pointer_idx == 0 else pointer_idx - 1
    elif keycode == BUTTON_24_EVENT_UP:
        # key ok
        selection_chosen[screen_idx] = pointer_idx
        if screen_idx == selection_setting_network["main"] or screen_idx == selection_setting_network[
            "choose_high_low"]:
            screen_idx += 1
            pointer_idx = 0
            call_screen_alarm_selection()
        elif screen_idx == selection_setting_network["confirm_assign_alarm"]:
            if pointer_idx == confirm["yes"]:
                save_alarm()
                screen_idx = selection_setting_network["main"]
                pointer_idx = 0
                call_screen_alarm_selection()
            else:
                return
        else:
            maxLength = 3
            pointer_idx += 1
            pointer_idx = pointer_idx if pointer_idx < maxLength else maxLength
            refresh_screen_assign_alarm()
    else:
        return


def assign_alarm_listen_key(keycode):
    global pointer_idx, screen_idx
    if keycode == BUTTON_23_EVENT_UP:
        # key left
        pointer_idx -= 1
        pointer_idx = pointer_idx if pointer_idx > 0 else 0
    elif keycode == BUTTON_25_EVENT_UP:
        # key right
        pointer_idx += 1
        maxLength = 3
        pointer_idx = pointer_idx if pointer_idx < maxLength else maxLength
    elif keycode == BUTTON_14_EVENT_UP or keycode == BUTTON_34_EVENT_UP:
        # key up or key down
        alarm.alarm[pointer_idx] = get_next_number(keycode, alarm.alarm[pointer_idx])
    elif keycode == BUTTON_24_EVENT_UP:
        # key ok
        screen_idx += 1
    else:
        return
    # refresh screen
    call_screen_alarm_selection()


def save_ip():
    for i, v in network.get_oct():
        if v > 225 or v < 1:
            # ip in range (1 - 225)
            LOGGER.error('Error at octet %s: %s', i, v)
            return 0
    # Luu ip vao const
    # ...
    reset_parameter()
    return 1


def save_alarm():
    # Luu ip vao const
    # ...
    reset_parameter()
    return 1


# Nghi ti da
# Co 2 van de can hoi lai
# 1. Lam cach nao de register event ban phim thiet bi, de them function da viet
# 2. Blink chu cai o man hien thi thi dung cai gi
# 3. Chot lai cach doc/ghi vao json

# SonTH: Main screen alarm
def call_screen_alarm_selection():
    try:
        row_1 = 'CANH BAO'
        switcher = [
            {
                "row_2": '> Nguong AC Luoi',
                "row_3": 'Nguong nhiet do',
                "row_4": 'Nguong do am'
            },
            {
                "row_2": 'Nguong AC Luoi',
                "row_3": '> Nguong nhiet do',
                "row_4": 'Nguong do am'
            },
            {
                "row_2": 'Nguong AC Luoi',
                "row_3": 'Nguong nhiet do',
                "row_4": '> Nguong do am'
            }
        ]

        if screen_idx == selection_setting_alarm["choose_high_low"]:
            switcher = [
                {
                    "row_2": '> Nguong cao',
                    "row_3": 'Nguong thap',
                    "row_4": ''
                },
                {
                    "row_2": 'Nguong cao',
                    "row_3": '> Nguong thap',
                    "row_4": ''
                }
            ]
        elif screen_idx == selection_setting_alarm["confirm_assign_alarm"]:
            switcher = [
                {
                    "row_2": '> Co',
                    "row_3": 'Khong',
                    "row_4": ''
                },
                {
                    "row_2": 'Co',
                    "row_3": '> Khong',
                    "row_4": ''
                }
            ]
            row_1 = 'XAC NHAN LUU'
        # Update text
        process_cmd_lcd(ROW_1, UPDATE_VALUE, row_1)
        process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[selection_chosen[screen_idx]]['row_2'])
        process_cmd_lcd(ROW_3, UPDATE_VALUE, switcher[selection_chosen[screen_idx]]['row_3'])
        process_cmd_lcd(ROW_4, UPDATE_VALUE, switcher[selection_chosen[screen_idx]]['row_4'])
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_alarm with message: %s', ex.message)


def refresh_screen_assign_alarm():
    try:
        global alarm
        alarm = get_alarm_info()
        switcher = [
            {
                "row_2": 'Nguong cao'
            },
            {
                "row_2": 'Nguong thap'
            }
        ]
        text = 'V'
        if selection_chosen[0] == screen_setting_alarm["temp"]:
            text = 'C'
        elif selection_chosen[0] == screen_setting_alarm["humidity"]:
            text = '%'
        # Update text
        process_cmd_lcd(ROW_1, UPDATE_VALUE, 'CANH BAO')
        process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[selection_chosen[screen_idx - 1]]["row_2"])
        process_cmd_lcd(ROW_2, UPDATE_VALUE, "{0}{1}".format(alarm.get_alarm(), text))

        LOGGER.info('ASSIGN IP ALARM: %s', str(alarm.get_alarm()))
        # Update nhap nhay
        # ...
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)
