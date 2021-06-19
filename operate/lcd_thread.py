import time

import requests

from config import *
from config.common import *
from config.common_lcd_services import *
from devices.utils import read_lcd_services
from model.lcd import Lcd
from utility import bytes_to_int

URL_SEND_SA = 'https://backend.smartsite.dft.vn/api/services/app/DMTram/ChangeValueTemplate'
menu_level_1 = [MCC, ACM, ATS]
LIST_KEY_EVENT = [EVENT_NONE, EVENT_DOWN, EVENT_UP, EVENT_HOLD, EVENT_POWER]
LIST_KEY_CODE = [KEYCODE_MENU, KEYCODE_UP, KEYCODE_DOWN, KEYCODE_ENTER]


def call():
    LOGGER.error('Enter call function in menu_thread')
    try:
        period = 1.5
        while True:
            if CLIENT.is_connected():
                result_check_input = check_lcd_service(lcd_services)
                if result_check_input.key_code > 0 and result_check_input.key_event > 0:
                    result_switch_lcd = switch_lcd_service(result_check_input)
                    cmd_lcd_lock.acquire()
                    cmd_lcd[CLEAR] = 0
                    cmd_lcd[UPDATE_VALUE] = result_switch_lcd.name
                    cmd_lcd_lock.release()
                    set_last_trace(result_switch_lcd)
                    lcd_services.clear()
            time.sleep(period)
    except Exception as ex:
        LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)


def get_menu_lv2(last_trace):
    name = ''
    try:
        if last_trace.index == 0:
            name = get_menu_lv2_mcc(0)
        elif last_trace.index == 1:
            name = get_menu_lv2_acm(0)
        elif last_trace.index == 2:
            name = get_menu_lv2_ats(0)
    except Exception as ex:
        LOGGER.error('Error at get_menu_lv2 function with message: %s', ex.message)
    return name


def switch_lcd_service(input_lcd):
    last_trace = Lcd()
    try:
        key_event = input_lcd.key_event
        key_code = input_lcd.key_code
        if key_event == EVENT_UP:
            if key_code == KEYCODE_MENU:
                index = 0
                last_trace.category = KEYCODE_MENU
                last_trace.level = MENU_LEVEL_1
                last_trace.index = index
                last_trace.name = menu_level_1[index]
                last_trace.value = -1
            elif key_code == KEYCODE_UP or key_code == KEYCODE_DOWN:
                last_trace = navigate_lcd_service(key_code)
            # elif key_code == KEYCODE_ENTER:
            #     last_trace = enter_lcd_service()

            last_trace.key_code = input_lcd.key_code
            last_trace.key_event = input_lcd.key_event
        else:
            LOGGER.info('Key event != EVENT_UP so do nothing')
    except Exception as ex:
        LOGGER.info('Error at switch_lcd_service function with message: %s', ex.message)
    return last_trace


def enter_lcd_service():
    last_trace = get_last_trace()
    try:
        if last_trace.category == KEYCODE_MENU:
            if last_trace.level == MENU_LEVEL_1:
                name = get_menu_lv2(last_trace)
                last_trace.level = MENU_LEVEL_2
                last_trace.index = 0
                last_trace.name = name
            # elif temp_level == MENU_LEVEL_2:
            #     pass
        else:
            pass
    except Exception as ex:
        LOGGER.error('Error at confirm_lcd_service function with message: %s', ex.message)
    return last_trace


def navigate_lcd_service(key_code):
    index = -1
    last_trace = get_last_trace()
    try:
        if last_trace.category == KEYCODE_MENU and last_trace.level == MENU_LEVEL_1:
            if key_code == KEYCODE_UP:
                index = last_trace.index + 1
                if index > MAX_INDEX_MENU:
                    index = MIN_INDEX_MENU
            elif key_code == KEYCODE_DOWN:
                index = last_trace.index - 1
                if index < MIN_INDEX_MENU:
                    index = MAX_INDEX_MENU
        # elif last_trace.category == KEYCODE_MENU and last_trace.level ==  MENU_LEVEL_2:
        #     pass
        last_trace.index = index
        last_trace.name = menu_level_1[index]
    except Exception as ex:
        LOGGER.error('Error at confirm_lcd_service function with message: %s', ex.message)
    return last_trace


def write_body_send_shared_attributes(key, value):
    body = {}
    try:
        now = round(time.time() * 1000)
        body = {"tramEntityId": device_config['device_id'], "value": value, "keyName": key, "changeAt": now}
        LOGGER.info('Content of body send shared attributes to Smartsite: %s', body)
    except Exception as ex:
        LOGGER.info('Error at write_body_send_shared_attributes function with message: %s', ex.message)
    return body


def send_shared_attributes(body):
    result = False
    try:
        response = requests.post(url=URL_SEND_SA, json=body)
        if response.status_code == 200:
            LOGGER.info('Send shared attributes to Smartsite successful!')
            result = True
        else:
            LOGGER.info('Fail while send shared attributes to Smartsite!')
    except Exception as ex:
        LOGGER.info('Error at write_log function with message: %s', ex.message)
    return result


# OK
def extract_lcd_service(byte_data):
    try:
        key_code = bytes_to_int(byte_data[0:2], byteorder=BYTE_ORDER)
        key_event = bytes_to_int(byte_data[2])
        read_lcd_services('key_code', key_code)
        read_lcd_services('key_event', key_event)
        LOGGER.info('After extract command lcd from STM32, key code: %d, key event: %d', key_code, key_event)
    except Exception as ex:
        LOGGER.error('Error at extract_lcd_service function with message: %s', ex.message)


# OK
def get_last_trace():
    lcd_last_trace = Lcd()
    try:
        json_file = open('./last_trace_lcd.json',)
        dct_last_trace = json.load(json_file)
        lcd_last_trace.key_code = dct_last_trace['key_code']
        lcd_last_trace.key_event = dct_last_trace['key_event']
        lcd_last_trace.category = dct_last_trace['category']
        lcd_last_trace.level = dct_last_trace['level']
        lcd_last_trace.index = dct_last_trace['index']
        lcd_last_trace.value = dct_last_trace['value']
        lcd_last_trace.name = dct_last_trace['name']
    except Exception as ex:
        LOGGER.error('Error at get_last_trace with message: %s', ex.message)
    return lcd_last_trace


# OK
def set_last_trace(input_lcd):
    try:
        dct_last_trace = input_lcd.__dict__
        json_last_trace = json.dumps(dct_last_trace)
        with io.open('./last_trace_lcd.json', 'wb') as last_trace_file:
            last_trace_file.write(json_last_trace)
        LOGGER.info('Command information just send: %s', dct_last_trace)
    except Exception as ex:
        LOGGER.error('Error at set_last_trace function with message: %s', ex.message)


# OK
def check_lcd_service(dct_lcd_service):
    LOGGER.info('Enter check_lcd_service function')
    key_code_checked = False
    key_event_checked = False
    input_lcd = Lcd()
    try:
        input_lcd.key_code = dct_lcd_service['key_code']
        input_lcd.key_event = dct_lcd_service['key_event']
        key_code = input_lcd.key_code
        key_event = input_lcd.key_event

        if input_lcd.key_code in LIST_KEY_CODE:
            key_code_checked = True
            LOGGER.info('Key code: %d, exist in LIST_KEY_CODE', key_code)
        else:
            LOGGER.info('Key code: %d not exists LIST_KEY_CODE', key_code)

        if input_lcd.key_event in LIST_KEY_EVENT:
            key_event_checked = True
            LOGGER.info('Key event: %d exists in LIST_KEY_EVENT', key_event)
        else:
            LOGGER.info('Key event: %d not exists in LIST_KEY_EVENT', key_event)

        if key_code_checked and key_event_checked:
            LOGGER.info('Check key code & key event successful')
        else:
            input_lcd.key_code = -1
            input_lcd.key_event = -1
            LOGGER.info('Fail while check ')
    except Exception as ex:
        LOGGER.error('Error at check_lcd_service function with message: %s', ex.message)
    LOGGER.info('Exit check_lcd_service function')
    return input_lcd


# OK
def get_menu_lv2_ats(index):
    switcher_menu_ats = {
        1: 'atsVacMaxThreshold',
        2: 'atsVacMinThreshold',
        3: 'atsVgenMaxThreshold',
        4: 'atsVgenMinThreshold',
        5: 'atsVacStabilizeTimeout',
        6: 'atsVgenIdleCoolingTimeout',
        7: 'atsVgenIdleWarmUpTimeout',
        8: 'atsGenInactiveStartTime',
        9: 'atsGenInactiveEndTime',
        10: 'atsGenActiveDuration',
        11: 'atsGenAutoResetMode',
        12: 'atsGenAutoResetTimeout',
        13: 'atsGenAutoResetMax',
        14: 'atsGenDeactivateMode',
        15: 'atsVacThresholdState',
        16: 'atsVgenThresholdState'
    }
    return switcher_menu_ats.get(index, "Out of range!")


# OK
def get_menu_lv2_acm(index):
    switcher_menu_acm = {
        1: 'acmControlAuto',
        2: 'acmAlternativeTime',
        3: 'acmRunTime',
        4: 'acmRestTime',
        5: 'acmGenAllow',
        6: 'acmVacThreshold',
        7: 'acmMinTemp',
        8: 'acmMaxTemp',
        9: 'acmMinHumid',
        10: 'acmMaxHumid',
        11: 'acmExpectedTemp',
        12: 'acmExpectedTemp',
        13: 'acmT1Temp',
        14: 'acmT2Temp',
        15: 'acmT3Temp',
        16: 'acmT4Temp'
    }
    return switcher_menu_acm.get(index, "Out of range!")


# OK
def get_menu_lv2_mcc(index):
    switcher_menu_lv2_mcc = {
        0: 'mccPeriodReadDataIO',
        1: 'mccPeriodSendTelemetry',
        2: 'mccPeriodUpdate',
        3: 'mccDcMinThreshold'
    }
    return switcher_menu_lv2_mcc.get(index, "Out of range!")