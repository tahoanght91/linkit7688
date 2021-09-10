from time import sleep

from devices.utils import read_lcd_services
from model.alarm_lcd import Alarm_lcd
from services.menu import *
from utility import bytes_to_int

url_send_sa = PREFIX + DOMAIN + API_UPDATE_SHARED_ATTRIBUTES
url_get_staff = PREFIX + DOMAIN + API_GET_STAFF
LIST_KEY_EVENT = [EVENT_NONE, EVENT_DOWN, EVENT_UP, EVENT_HOLD, EVENT_POWER]
LIST_KEY_CODE = [KEYCODE_11, KEYCODE_16, KEYCODE_14, KEYCODE_34, KEYCODE_26, KEYCODE_24, KEYCODE_13, KEYCODE_12]
json_file = open('config/lcd.json')
last_trace_lcd = './last_trace_lcd.json'
dct_lcd = json.load(json_file)
dct_lcd_menu = dct_lcd['lcd']['category']['menu']
dct_lcd_menu_level = dct_lcd_menu['level']
dct_lcd_menu_level_lv1 = dct_lcd_menu_level['lv1']
last_alarm_update = Alarm_lcd()
timeOld = '61'
time_pre = '61'
titleOld = ''
acmTempInOld = ''
acmTempOutOld = ''
acmHumidInOld = ''
warningOld = ''
last_stt_bt = 0


def call():
    try:
        while True:
            button = check_button(lcd_services)
            if button != -1:
                LOGGER.info('Send button value: %s', str(button))
            main_menu(button)
            if lcd_services:
                del lcd_services['key_code']
                del lcd_services['key_event']
            sleep(0.3)
    except Exception as ex:
        LOGGER.warning('Error at call function in lcd_thread with message: %s', ex.message)


def write_body_send_shared_attributes(key, value):
    body = {}
    try:
        now = int(time.time() * 1000)
        body = {"tramEntityId": str(device_config['device_id']), "value": str(value), "keyName": str(key),
                "changeAt": now}
        LOGGER.debug('Content of body send shared attributes to Smartsite: %s', body)
    except Exception as ex:
        LOGGER.warning('Error at write_body_send_shared_attributes function with message: %s', ex.message)
    return body


def send_shared_attributes(body):
    result = False
    try:
        response = requests.post(url=url_send_sa, json=body)
        if response.status_code == 200:
            LOGGER.debug('Send shared attributes to Smartsite successful!')
            result = True
        else:
            LOGGER.debug('Fail while send shared attributes to Smartsite!')
    except Exception as ex:
        LOGGER.warning('Error at write_log function with message: %s', ex.message)
    return result


def extract_lcd_service(byte_data):
    try:
        key_code = bytes_to_int(byte_data[0:2], byteorder=BYTE_ORDER)
        key_event = bytes_to_int(byte_data[2])
        read_lcd_services('key_code', key_code)
        read_lcd_services('key_event', key_event)
        LOGGER.debug('After extract command lcd from STM32, key code: %d, key event: %d', key_code, key_event)
    except Exception as ex:
        LOGGER.warning('Error at extract_lcd_service function with message: %s', ex.message)


def check_button(bt_info):
    global last_stt_bt
    event_bt = 0
    index_key = 0
    try:
        if bt_info:
            key_code = bt_info['key_code']
            key_event = bt_info['key_event']
            LOGGER.debug('check_button function key code: %s, key event: %s', str(key_code), str(key_event))
            if int(key_code) in LIST_KEYCODE:
                index_key = int(LIST_KEYCODE.index(key_code))
            if key_event == EVENT_UP:
                event_bt = EVENT_UP_BT
            elif key_event == EVENT_HOLD:
                event_bt = EVENT_HOLD_BT
            button = event_bt * index_key
            if last_stt_bt != button:
                last_stt_bt = button
                LOGGER.debug('return button value: %s', LOG_BUTTON[button])
            return button
        else:
            return -1
    except Exception as ex:
        LOGGER.warning('check_button function error: %s', ex.message)
