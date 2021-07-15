import subprocess
import time

import requests
from config.common_api import *
from config import *
from config.common import UPDATE_VALUE
from config.common_lcd_services import *

url_send_sa = PREFIX + DOMAIN + API_UPDATE_SHARED_ATTRIBUTES


class __IPv4:
    def __init__(self):
        self.ip = ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_']

    def get_ip(self):
        return "{0}{1}{2}.{3}{4}{5}.{6}{7}{8}.{9}{10}{11}".format(self.ip[0]
                                                                  , self.ip[1]
                                                                  , self.ip[2]
                                                                  , self.ip[3]
                                                                  , self.ip[4]
                                                                  , self.ip[5]
                                                                  , self.ip[6]
                                                                  , self.ip[7]
                                                                  , self.ip[8]
                                                                  , self.ip[9]
                                                                  , self.ip[10]
                                                                  , self.ip[11])

    def get_ip_number(self):
        return "{0}{1}{2}.{3}{4}{5}.{6}{7}{8}.{9}{10}{11}".format(self.ip[0] if self.ip[0] != '_' else ''
                                                                  , self.ip[1] if self.ip[1] != '_' else ''
                                                                  , self.ip[2] if self.ip[2] != '_' else ''
                                                                  , self.ip[3] if self.ip[3] != '_' else ''
                                                                  , self.ip[4] if self.ip[4] != '_' else ''
                                                                  , self.ip[5] if self.ip[5] != '_' else ''
                                                                  , self.ip[6] if self.ip[6] != '_' else ''
                                                                  , self.ip[7] if self.ip[7] != '_' else ''
                                                                  , self.ip[8] if self.ip[8] != '_' else ''
                                                                  , self.ip[9] if self.ip[9] != '_' else ''
                                                                  , self.ip[10] if self.ip[10] != '_' else ''
                                                                  , self.ip[11] if self.ip[11] != '_' else '')

    def get_oct(self):
        for v in self.get_ip_number().split("."):
            if v == '' or int(v) > 225:
                # Chua nhap octet nay
                # ip khong duoc lon hon 225
                return 0

        return self.get_ip().split(".")

        # return [int("{0}{1}{2}".format(self.ip[0]
        #                                , self.ip[1]
        #                                , self.ip[2]))
        #     , int("{0}{1}{2}".format(self.ip[3]
        #                              , self.ip[4]
        #                              , self.ip[5]))
        #     , int("{0}{1}{2}".format(self.ip[6]
        #                              , self.ip[7]
        #                              , self.ip[8]))
        #     , int("{0}{1}{2}".format(self.ip[9]
        #                              , self.ip[10]
        #                              , self.ip[11]))]

        # return [int("{0}{1}{2}".format(self.ip[0] if self.ip[0] != '_' else 0
        #                                , self.ip[1] if self.ip[1] != '_' else 0
        #                                , self.ip[2] if self.ip[2] != '_' else 0))
        #     , int("{0}{1}{2}".format(self.ip[3] if self.ip[3] != '_' else 0
        #                              , self.ip[4] if self.ip[4] != '_' else 0
        #                              , self.ip[5] if self.ip[5] != '_' else 0))
        #     , int("{0}{1}{2}".format(self.ip[6] if self.ip[6] != '_' else 0
        #                              , self.ip[7] if self.ip[7] != '_' else 0
        #                              , self.ip[8] if self.ip[8] != '_' else 0))
        #     , int("{0}{1}{2}".format(self.ip[9] if self.ip[9] != '_' else 0
        #                              , self.ip[10] if self.ip[10] != '_' else 0
        #                              , self.ip[11] if self.ip[11] != '_' else 0))]


class __Alarm:
    def __init__(self):
        self.alarm = ['_', '_', '_']

    def get_alarm_number(self):
        result = ''.join(self.alarm)
        return 0 if result == '___' else result

    def get_alarm(self):
        array = []
        for v in self.alarm:
            array.append('_' if v == '' else v)
        return ''.join(array)


# Man hinh setting nao
screen_setting_idx = 0
# Vi tri man hinh hien tai
# Gia tri khoi tao la -1, se tang len thanh 0 khi lan dau tien render man hinh
screen_idx = -1
# con tro vi tri tren man hinh
pointer_idx = 0
# Network
network = 0
# Alarm
alarm = 0
# Fix loi goi choose_config nhieu lan khi dang trong man hinh nay roi
isChosen = 0

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
    global screen_setting_idx, screen_idx, isChosen
    if isChosen:
        LOGGER.info('Do nothing and return in choose_config')
        return
    isChosen = 1
    screen_idx = -1
    screen_setting_idx = setting_idx
    LOGGER.info('IN choose_config: %s, %s', screen_idx, screen_setting_idx)


def reset_parameter():
    # call moi khi quay lai man hinh main config
    global pointer_idx, screen_idx
    pointer_idx = 0
    screen_idx = 0


# SonTH: Config network
# Main cua man hinh network
def call_screen_network(keycode):
    from control import process_cmd_lcd
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
        # LOGGER.info('Enter call_screen_network function: %s', str(switcher[selection_chosen]))
        # Update text
        if keycode == OK:
            process_cmd_lcd(ROW_1, UPDATE_VALUE, 'THONG SO MANG')
        process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[selection_chosen[screen_idx]]['row_2'])
        process_cmd_lcd(ROW_3, UPDATE_VALUE, switcher[selection_chosen[screen_idx]]['row_3'])
        process_cmd_lcd(ROW_4, UPDATE_VALUE, switcher[selection_chosen[screen_idx]]['row_4'])
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)


def refresh_screen_assign_ip_address(keycode):
    from control import process_cmd_lcd
    try:
        global network
        network = get_net_info() if network == 0 else network
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

        switcher_2 = [
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

        # Update text
        if screen_idx % 2 == 0:
            # Man hinh xac nhan luu
            LOGGER.info('Enter refresh_screen_assign_ip_address function: %s', str(switcher_2[pointer_idx]))
            if keycode == OK:
                process_cmd_lcd(ROW_1, UPDATE_VALUE, 'XAC NHAN LUU')
            process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher_2[pointer_idx]["row_2"])
            process_cmd_lcd(ROW_3, UPDATE_VALUE, switcher_2[pointer_idx]["row_3"])
            process_cmd_lcd(ROW_4, UPDATE_VALUE, switcher_2[pointer_idx]["row_4"])
        else:
            # Man hinh nhap ip - subnet - ...
            LOGGER.info('Enter refresh_screen_assign_ip_address function: %s', str(switcher[selection_chosen[screen_idx]]))
            if keycode == OK:
                process_cmd_lcd(ROW_1, UPDATE_VALUE, 'THONG SO MANG')
            process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[selection_chosen[screen_idx]]['row_2'])
            process_cmd_lcd(ROW_3, UPDATE_VALUE, network.get_ip())
            process_cmd_lcd(ROW_4, UPDATE_VALUE, '')

        # LOGGER.info('ASSIGN IP SCREEN: %s', str(network.get_ip()))
        # Update nhap nhay
        # ...
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)


def get_net_info():
    # Todo: Get thong tin ip dang su dung, neu khong co thi tra ve null
    file_json = read_from_json('./last_cmd_network.json')
    key = ""
    for k in set_ip_idx:
        if selection_chosen[0] == set_ip_idx[k]:
            key = "row{}".format(set_ip_idx[k] + 1)
            continue
    if len(key) == 0:
        return
    array = file_json[key].split(".")
    result = __IPv4()
    if len(array) > 0 and array[0] != '':
        result.ip = convert_to_array_number(array)

    # Tam fake bang 192.168.1.11
    # result.ip = [1, 9, 2, 1, 6, 8, '', '', 1, '', 1, 1]
    return result


def convert_to_array_number(array):
    result = []
    for v in array:
        if v != '' and v != '_':
            while int(v) >= 10:
                result.append(int(v) % 10)
                v = int(int(v) / 10)
            result.append(int(v))

    return result


def get_alarm_info():
    # Todo: Get thong tin alarm dang su dung, neu khong co thi tra ve null
    result = __Alarm()
    file_json = read_from_json('./last_cmd_alarm.json')
    key = ""
    for k in set_alarm_idx:
        if selection_chosen[0] == set_alarm_idx[k]:
            key = "row{}".format(set_alarm_idx[k] + 1)
            continue
    if len(key) == 0:
        return
    if file_json[key] != '':
        result.alarm = convert_to_array_number([file_json[key]])
    # Tam fake bang 77
    # result.alarm = [7, 7, '_']
    return result


def get_next_number(keycode, number):
    if number == '_':
        number = 0
    if keycode == UP:
        return 0 if number >= 9 else number + 1
    elif keycode == DOWN:
        return 9 if number == 0 else number - 1


# Register func nay
def listen_key_code(keycode):
    global isChosen
    if keycode == ESC:
        # Ben menu da xu ly thoat ve man hinh menu roi
        # Reset lai cac gia tri de lan sau goi
        isChosen = 0
        reset_parameter()
        return

    if screen_setting_idx == selection_setting["network"]:
        get_func_keycode(network_keycode_func_idx, keycode)
    elif screen_setting_idx == selection_setting["alarm"]:
        get_func_keycode(alarm_keycode_func_idx, keycode)
    else:
        return


def main_network_listen_key(keycode):
    global pointer_idx, screen_idx
    # 5 dong
    LOGGER.info('SHOW key_code NOW: %s', str(keycode))
    max_pointer_idx = 4
    if keycode == BUTTON_34_EVENT_UP:
        # key down
        pointer_idx = max_pointer_idx if pointer_idx == max_pointer_idx else pointer_idx + 1
    elif keycode == BUTTON_14_EVENT_UP:
        # key up
        pointer_idx = 0 if pointer_idx == 0 else pointer_idx - 1
    elif keycode == BUTTON_24_EVENT_UP:
        # key ok
        LOGGER.info('Show screen_idx: %s', str(screen_idx))
        if screen_idx > -1:
            # lan dau tien load man hinh screen_idx = -1, khong update gia tri chon
            selection_chosen[screen_idx] = pointer_idx
        screen_idx = 0 if screen_idx == 2 else screen_idx + 1
        LOGGER.info('--- Show screen_idx: %s', str(screen_idx))
        # refresh gia tri pointer index
        pointer_idx = 0
    else:
        return
    LOGGER.info('Enter main_network_listen_key function, screen_idx: %s, pointer_idx: %s', str(screen_idx), str(pointer_idx))
    # refresh man hinh
    get_func_render(network_screen_idx, keycode)

# def main_alarm_listen_key(keycode):
#     global pointer_idx, screen_idx
#     # main co 4 dong, choose co 2 dong
#     max_pointer_idx = 3 if screen_idx == selection_setting_alarm["alarm"] else 1
#     if keycode == BUTTON_34_EVENT_UP:
#         # key down
#         pointer_idx = max_pointer_idx if pointer_idx == max_pointer_idx else pointer_idx + 1
#     elif keycode == BUTTON_14_EVENT_UP:
#         # key up
#         pointer_idx = 0 if pointer_idx == 0 else pointer_idx - 1
#     elif keycode == BUTTON_24_EVENT_UP:
#         # key ok
#         selection_chosen[screen_idx] = pointer_idx
#         screen_idx = 0 if screen_idx == 3 else screen_idx + 1
#         # refresh gia tri pointer index
#         pointer_idx = 0
#     else:
#         return
#     # refresh man hinh
#     call_screen_alarm_selection()


def assign_ip_listen_key(keycode):
    global pointer_idx, screen_idx
    if keycode == BUTTON_23_EVENT_UP:
        # key left
        pointer_idx -= 1
        pointer_idx = pointer_idx if pointer_idx > 0 else 0
    elif keycode == BUTTON_25_EVENT_UP:
        # key right
        max_pointer_idx = 11
        pointer_idx += 1
        pointer_idx = pointer_idx if pointer_idx < max_pointer_idx else max_pointer_idx
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
                if save_ip() == 0:
                    return
                pointer_idx = 0
                screen_idx = selection_setting_network["main"]
            else:
                return
    else:
        return

    LOGGER.info('Enter assign_ip_listen_key function, screen_idx: %s, pointer_idx: %s', str(screen_idx), str(pointer_idx))
    # refresh screen
    get_func_render(network_screen_idx, keycode)


def alarm_selection_listen_key(keycode):
    try:
        global pointer_idx, screen_idx
        # main co 4 dong, choose co 2 dong
        max_pointer_idx = 3 if screen_idx == selection_setting_alarm["assign_alarm"] else 1
        if keycode == BUTTON_34_EVENT_UP:
            # key down
            pointer_idx = max_pointer_idx if pointer_idx == max_pointer_idx else pointer_idx + 1
        elif keycode == BUTTON_14_EVENT_UP:
            # key up
            pointer_idx = 0 if pointer_idx == 0 else pointer_idx - 1
        elif keycode == BUTTON_24_EVENT_UP:
            # key ok
            if screen_idx > -1:
                # lan dau tien load man hinh screen_idx = -1, khong update gia tri chon
                selection_chosen[screen_idx] = pointer_idx
            screen_idx += 1
            # refresh gia tri pointer index
            pointer_idx = 0
            if screen_idx == selection_setting_alarm["confirm_assign_alarm"] + 1:
                if pointer_idx == confirm["yes"]:
                    if save_alarm() == 0:
                        return
                    screen_idx = selection_setting_alarm["main"]
                else:
                    return
        else:
            return
        # Call function render
        get_func_render(alarm_screen_idx, keycode)
        LOGGER.info('Enter alarm_selection_listen_key function, screen_idx: %s, pointer_idx: %s', str(screen_idx),
                    str(pointer_idx))
        LOGGER.info('Run function alarm_selection_listen_key')
    except Exception as ex:
        LOGGER.error('Error at call function in alarm_selection_listen_key with message: %s', ex.message)


def assign_alarm_listen_key(keycode):
    global pointer_idx, screen_idx
    max_pointer_idx = 2
    if keycode == BUTTON_23_EVENT_UP:
        # key left
        pointer_idx -= 1
        pointer_idx = pointer_idx if pointer_idx > 0 else 0
    elif keycode == BUTTON_25_EVENT_UP:
        # key right
        pointer_idx += 1
        pointer_idx = pointer_idx if pointer_idx < max_pointer_idx else max_pointer_idx
    elif keycode == BUTTON_14_EVENT_UP or keycode == BUTTON_34_EVENT_UP:
        # key up or key down
        alarm.alarm[pointer_idx] = get_next_number(keycode, alarm.alarm[pointer_idx])
    elif keycode == BUTTON_24_EVENT_UP:
        # key ok
        selection_chosen[screen_idx] = pointer_idx
        screen_idx += 1
        # refresh gia tri pointer index
        pointer_idx = 0
    else:
        return
    # refresh screen
    LOGGER.info('Enter assign_alarm_listen_key function, screen_idx: %s, pointer_idx: %s', str(screen_idx),
                str(pointer_idx))
    get_func_render(alarm_screen_idx, keycode)


def save_ip():
    LOGGER.info('Enter assign_alarm_listen_key function')
    if network.get_oct() == 0:
        return
    # for i, v in network.get_oct():
    #     if v > 225 or v < 0:
    #         # ip in range (0 - 225)
    #         LOGGER.error('Error at octet %s: %s', i, v)
    #         return 0
    # Luu ip vao const
    save_to_file('./last_cmd_network.json', network.get_ip(), selection_chosen[0] + 1)
    # Luu ip vao bash
    for k in set_ip_idx:
        save_to_set_ip(network.get_ip(), k) if selection_chosen[0] == set_ip_idx[k] else 1
    reset_parameter()
    return 1


def save_alarm():
    if alarm.get_alarm_number() == 0:
        return 0
    LOGGER.info('Enter save_alarm function')
    # Luu alarm vao const
    save_to_file('./last_cmd_alarm.json', alarm.get_alarm_number(), selection_chosen[0] + 1)
    # Call API de luu alarm
    for k in key_attr:
        if key_attr[k]["index_screen_1"] == selection_chosen[0] and key_attr[k]["index_screen_2"] == selection_chosen[1]:
            # Man hinh 1 chon loai alarm
            # Man hinh 2 chon set nguong cao hay thap
            write_body_send_shared_attributes(alarm.get_alarm_number(), k)
            break
    # Reset cac tham so dieu huong man hinh
    reset_parameter()
    return 1


# SonTH: Main screen alarm
def call_screen_alarm_selection(keycode):
    from control import process_cmd_lcd
    try:
        row_1 = 'CANH BAO'
        switcher = [
            {
                "row_2": '> Dien ap luoi',
                "row_3": 'Dien ap may phat'
            },
            {
                "row_2": 'Dien ap luoi',
                "row_3": '> Dien ap may phat'
            },
            {
                "row_2": '> Nhiet do',
                "row_3": 'Do am'
            },
            {
                "row_2": 'Nhiet do',
                "row_3": '> Do am'
            }
        ]

        if screen_idx == selection_setting_alarm["choose_high_low"]:
            switcher = [
                {
                    "row_2": '> Nguong cao',
                    "row_3": 'Nguong thap'
                },
                {
                    "row_2": 'Nguong cao',
                    "row_3": '> Nguong thap'
                }
            ]
        elif screen_idx == selection_setting_alarm["confirm_assign_alarm"]:
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
            row_1 = 'XAC NHAN LUU'
        # Update text
        if keycode == OK:
            process_cmd_lcd(ROW_1, UPDATE_VALUE, row_1)
        process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[selection_chosen[screen_idx]]['row_2'])
        process_cmd_lcd(ROW_3, UPDATE_VALUE, switcher[selection_chosen[screen_idx]]['row_3'])
        LOGGER.info('Write output in function call_screen_alarm_selection: {0} - {1} - {2}', row_1,
                    switcher[selection_chosen[screen_idx]]['row_2'], switcher[selection_chosen[screen_idx]]['row_3'])
    except Exception as ex:
        LOGGER.error('Error at call function in call_screen_alarm_selection with message: %s', ex.message)


def refresh_screen_assign_alarm(keycode):
    from control import process_cmd_lcd
    try:
        global alarm
        alarm = get_alarm_info() if alarm == 0 else alarm
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
        if keycode == OK:
            process_cmd_lcd(ROW_1, UPDATE_VALUE, 'CANH BAO')
            process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[selection_chosen[screen_idx - 1]]["row_2"])
        process_cmd_lcd(ROW_2, UPDATE_VALUE, "{0}{1}".format(alarm.get_alarm(), text))

        LOGGER.info('ASSIGN ALARM in func call refresh_screen_assign_alarm: %s', str(alarm.get_alarm()))
        # Update nhap nhay
        # ...
    except Exception as ex:
        LOGGER.error('Error at call function in refresh_screen_assign_alarm with message: %s', ex.message)


# Helper save/read file

set_ip_idx = {
    "ip": 0,
    "gateway": 2,
    "subnet": 1,
    "primary_dns": 3,
    "secondary_dns": 4
}

set_alarm_idx = {
    "dien_ap_luoi": 0,
    "dien_ap_may_phat": 1,
    "temp": 2,
    "humidity": 3
}


row_format = {
    "ip": {
        "number": 1,
        "format": "uci set network.lan.ipaddr=\'{0}\'\n"
    },
    "gateway": {
        "number": 2,
        "format": "uci set network.lan.gateway=\'{0}\'\n"
    },
    "subnet": {
        "number": 3,
        "format": "uci set network.lan.netmask=\'{0}\'\n"
    },
    "primary_dns": {
        "number": 5,
        "format": "uci add_list network.lan.dns=\'{0}\'\n"
    },
    "secondary_dns": {
        "number": 6,
        "format": "uci add_list network.lan.dns=\'{0}\'\n"
    }
}


def save_to_set_ip(str_saved, key):
    try:
        save_to_file_txt('./setIp.sh', row_format[key]["format"].format(str_saved), row_format[key]["number"])
        LOGGER.info('Call save file ./setIp.sh')
        # run bash .sh
        bashCmd = ["./setIp.sh"]
        process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
        output, error = process.communicate()
        LOGGER.info('Run ./setIp.sh with output: {0} and error{1}', output, error)
    except Exception as ex:
        LOGGER.error('Error at call function in save_to_set_ip with message: %s', ex.message)


def save_to_file(file_path, str_saved, number):
    try:
        all_row = read_from_json(file_path)
        if number == ROW_1:
            all_row['row1'] = str_saved
        elif number == ROW_2:
            all_row['row2'] = str_saved
        elif number == ROW_3:
            all_row['row3'] = str_saved
        elif number == ROW_4:
            all_row['row4'] = str_saved
        elif number == ROW_5:
            all_row['row5'] = str_saved
        write_to_json(all_row, file_path)
        LOGGER.info('Saved file {0}', file_path)
    except Exception as ex:
        LOGGER.error('Error at call function in save_to_file with message: %s', ex.message)


def save_to_file_txt(file_path, str_saved, number):
    try:
        all_row = read_from_txt(file_path)
        all_row[number - 1] = str_saved
        write_to_txt(''.join(all_row), file_path)
        LOGGER.info('Saved file {0}', file_path)
    except Exception as ex:
        LOGGER.error('Error at call function in save_to_file with message: %s', ex.message)


def write_to_json(body, file_url):
    try:
        json_last_trace = json.dumps(body)
        with io.open(file_url, 'wb') as last_trace_file:
            last_trace_file.write(json_last_trace)
        LOGGER.info('Command information just send: %s', body)
    except Exception as ex:
        LOGGER.error('Error at write_to_json function with message: %s', ex.message)


def read_from_json(file_url):
    try:
        json_file = open(file_url, )
        json_info = json.load(json_file)
    except Exception as ex:
        LOGGER.error('Error at call function in read_to_json with message: %s', ex.message)
    return json_info


def write_to_txt(body, file_url):
    try:
        with io.open(file_url, 'wb') as last_trace_file:
            last_trace_file.write(body)
        LOGGER.info('Command information just send: %s', body)
    except Exception as ex:
        LOGGER.error('Error at write_to_txt function with message: %s', ex.message)


def read_from_txt(file_url):
    try:
        with io.open(file_url) as last_trace_file:
            bash_info = last_trace_file.readlines()
    except Exception as ex:
        LOGGER.error('Error at call function in read_from_txt with message: %s', ex.message)
    return bash_info


# Helper call api
key_attr = {
    "atsVacMaxThreshold": {
        "index_screen_1": 0,
        "index_screen_2": 0
    },
    "atsVacMinThreshold": {
        "index_screen_1": 0,
        "index_screen_2": 1
    },
    "atsVgenMaxThreshold": {
        "index_screen_1": 1,
        "index_screen_2": 0
    },
    "atsVgenMinThreshold": {
        "index_screen_1": 1,
        "index_screen_2": 1
    },
    "acmMaxTempThreshold": {
        "index_screen_1": 2,
        "index_screen_2": 0
    },
    "acmMinTempThreshold": {
        "index_screen_1": 2,
        "index_screen_2": 1
    },
    "acmMaxHumidThreshold": {
        "index_screen_1": 3,
        "index_screen_2": 0
    },
    "acmMinHumidThreshold": {
        "index_screen_1": 3,
        "index_screen_2": 1
    }
}


def write_body_send_shared_attributes(key, value):
    body = {}
    try:
        now = int(time.time() * 1000)
        body = {"tramEntityId": str(device_config['device_id']), "value": str(value), "keyName": str(key),
                "changeAt": now}
        LOGGER.info('Content of body send shared attributes to Smartsite: %s', body)
    except Exception as ex:
        LOGGER.info('Error at write_body_send_shared_attributes function with message: %s', ex.message)
    return body


def send_shared_attributes(body):
    result = False
    try:
        response = requests.post(url=url_send_sa, json=body)
        if response.status_code == 200:
            LOGGER.info('Send shared attributes to Smartsite successful!')
            result = True
        else:
            LOGGER.info('Fail while send shared attributes to Smartsite!')
    except Exception as ex:
        LOGGER.info('Error at write_log function with message: %s', ex.message)
    return result


# Co van de can hoi lai
# 1. Blink chu cai o man hien thi thi dung cai gi


network_screen_idx = {
    0: call_screen_network,
    1: refresh_screen_assign_ip_address,
    2: refresh_screen_assign_ip_address
}

network_keycode_func_idx = {
    0: main_network_listen_key,
    1: assign_ip_listen_key,
    2: assign_ip_listen_key
}

alarm_screen_idx = {
    0: call_screen_alarm_selection,
    1: call_screen_alarm_selection,
    2: refresh_screen_assign_alarm,
    3: call_screen_alarm_selection
}

alarm_keycode_func_idx = {
    0: alarm_selection_listen_key,
    1: alarm_selection_listen_key,
    2: assign_alarm_listen_key,
    3: alarm_selection_listen_key
}


def get_func_render(o, keycode):
    scene_idx = 0 if screen_idx < 0 else screen_idx
    func = o.get(scene_idx)
    return func(keycode)


def get_func_keycode(o, kc):
    scene_idx = 0 if screen_idx < 0 else screen_idx
    func = o.get(scene_idx)
    return func(kc)
