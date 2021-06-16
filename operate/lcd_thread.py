import time

import requests

from config import *
from config.common import *
from config.common_lcd_services import *
from devices.utils import read_lcd_services
from utility import bytes_to_int

URL_SEND_SA = ''
menu_level_1 = [MCC, ACM, ATS]
LIST_KEY_EVENT = [EVENT_NONE, EVENT_DOWN, EVENT_UP, EVENT_HOLD, EVENT_POWER]
LIST_KEY_CODE = [KEYCODE_16_MENU]
dct_last_trace = {}


def call():
    LOGGER.error('Enter call function in menu_thread')
    try:
        period = 10
        while True:
            if CLIENT.is_connected():
                # TODO: warning
                init_last_trace(lcd_services, dct_last_trace)
                result_check_lcd = check_lcd_service(lcd_services)
                if len(result_check_lcd) == 0:
                    LOGGER.info('result_check_lcd is not none: %s', result_check_lcd)
                    result_switch_lcd = switch_lcd_service(result_check_lcd['key_code'], result_check_lcd['key_event'])
                    if result_switch_lcd != '':
                        commands_lock.acquire()
                        commands[LCD_SERVICE] = result_switch_lcd
                        commands_lock.release()
                        lcd_services.clear()
                else:
                    LOGGER.info('result_check_lcd is none: %s', result_check_lcd)
            time.sleep(period)
    except Exception as ex:
        LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)


def get_index_menu_lv1(key_code, key_event):
    LOGGER.info('Enter get_index_menu_lv1 function')
    index = -1
    category = KEYCODE_16_MENU
    level = 1
    value = -1
    last_index = dct_last_trace['index']
    try:
        if key_code == KEYCODE_16_MENU:
            index = last_index
        elif key_code == KEYCODE_15_UP:
            index = last_index + 1
            if index > MAX_INDEX_MENU:
                index = MIN_INDEX_MENU
        elif key_code == KEYCODE_36_DOWN:
            index = last_index - 1
            if index < MIN_INDEX_MENU:
                index = MAX_INDEX_MENU
        LOGGER.info('Index of menu level 1: %d', index)
        set_last_trace(key_code, key_event, category, level, index, value)
    except Exception as ex:
        LOGGER.error('Error at get_index_menu_lv1 function with message: %s', ex.message)
    LOGGER.info('Exit get_index_menu_lv1 function')
    return index


def get_menu_lv2(index):
    str_menu_lv2 = ''
    if index == 0:
        str_menu_lv2 = get_menu_lv2_mcc(index)
    elif index == 1:
        str_menu_lv2 = get_menu_lv2_acm(index)
    elif index == 2:
        str_menu_lv2 = get_menu_lv2_ats(index)
    return str_menu_lv2


def switch_lcd_service(key_code, key_event):
    LOGGER.info('Enter switch_lcd_service function')
    result = ''
    try:
        if key_event == EVENT_UP:
            if key_code == KEYCODE_16_MENU:
                result = menu_level_1[0]
            elif key_code == KEYCODE_15_UP or key_code == KEYCODE_36_DOWN:
                result = navigate_lcd_service(key_code)
            elif key_code == KEYCODE_11:
                result = enter_lcd_service()
        else:
            LOGGER.info('Key event != EVENT_UP so do nothing')
    except Exception as ex:
        LOGGER.info('Error at switch_lcd_service function with message: %s', ex.message)
    LOGGER.info('Exit switch_lcd_service function')
    return result


def enter_lcd_service():
    result = ''
    try:
        temp_category = dct_last_trace['category']
        temp_level = dct_last_trace['level']
        temp_index = dct_last_trace['index']
        temp_value = dct_last_trace['value']
        if temp_category == KEYCODE_16_MENU:
            if temp_level == MENU_LEVEL_1:
                result = get_menu_lv2(temp_index)
            elif temp_level == MENU_LEVEL_2:
                pass
        else:
            pass
    except Exception as ex:
        LOGGER.error('Error at confirm_lcd_service function with message: %s', ex.message)
    return result


def navigate_lcd_service(key_code):
    index = -1
    result = ''
    try:
        temp_category = dct_last_trace['category']
        temp_level = dct_last_trace['level']
        temp_index = dct_last_trace['index']
        temp_value = dct_last_trace['value']
        if temp_category == KEYCODE_16_MENU and temp_level == MENU_LEVEL_1:
            if key_code == KEYCODE_15_UP:
                index = temp_index + 1
                if index > MAX_INDEX_MENU:
                    index = MIN_INDEX_MENU
            elif key_code == KEYCODE_36_DOWN:
                index = temp_index - 1
                if index < MIN_INDEX_MENU:
                    index = MAX_INDEX_MENU
            result = menu_level_1[index]
        elif temp_category == KEYCODE_16_MENU and temp_level == MENU_LEVEL_2:
            pass
    except Exception as ex:
        LOGGER.error('Error at confirm_lcd_service function with message: %s', ex.message)
    return result


def write_body_send_shared_attributes(key, value):
    LOGGER.info('Enter write_body_send_shared_attributes function')
    body = {}
    try:
        now = round(time.time() * 1000)
        body = {"key": key, "value": value, "createdAt": now}
        LOGGER.info('Content of body send shared attributes to Smartsite: %s', body)
    except Exception as ex:
        LOGGER.info('Error at write_body_send_shared_attributes function with message: %s', ex.message)
    LOGGER.info('Exit write_body_send_shared_attributes function')
    return body


def send_shared_attributes(body):
    result = False
    try:
        LOGGER.info('Enter send_shared_attributes function')
        response = requests.post(url=URL_SEND_SA, json=body)
        if response.status_code == 200:
            LOGGER.info('Send shared attributes to Smartsite successful!')
            result = True
        else:
            LOGGER.info('Fail while send shared attributes to Smartsite!')
    except Exception as ex:
        LOGGER.info('Error at write_log function with message: %s', ex.message)
    LOGGER.info('Exit the function send_log')
    return result


def extract_lcd_service(byte_data):
    LOGGER.info('Enter extract_lcd_service function')
    byte_data_decode = ':'.join(x.encode('hex') for x in byte_data)
    LOGGER.info('Byte_data_decode after decode: %s', byte_data_decode)
    try:
        key_code = bytes_to_int(byte_data[0:1], byteorder=BYTE_ORDER)
        key_event = bytes_to_int(byte_data[2])
        read_lcd_services('keyCode', key_code)
        read_lcd_services('keyEvent', key_event)
        LOGGER.info('After extract command lcd from STM32, key code: %d, key event: %d', key_code, key_event)
    except Exception as ex:
        LOGGER.error('Error at extract_lcd_service function with message: %s', ex.message)
    LOGGER.info('Exit extract_lcd_service function')


def get_last_trace():
    return dct_last_trace


def set_last_trace(key_code, key_event, category, level, index, value):
    LOGGER.info('Enter set_last_trace function')
    try:
        dct_last_trace['keyCode'] = key_code
        dct_last_trace['keyEvent'] = key_event
        dct_last_trace['category'] = category
        dct_last_trace['level'] = level
        dct_last_trace['index'] = index
        dct_last_trace['value'] = value
        LOGGER.info('Command information just send: %s', dct_last_trace)
    except Exception as ex:
        LOGGER.error('Error at set_last_trace function with message: %s', ex.message)
    LOGGER.info('Exit set_last_trace function')


def init_last_trace(dct_lcd_service, dct_last_trace):
    LOGGER.info('Enter init_last_trace function')
    result = False
    try:
        if len(dct_last_trace) == 0:
            dct_last_trace = dct_lcd_service.copy()
            dct_last_trace['category'] = 0
            dct_last_trace['level'] = 1
            dct_last_trace['index'] = 0
            dct_last_trace['value'] = -1
            LOGGER.info('Init dictionary last trace successful!')
            result = True
    except Exception as ex:
        LOGGER.error('Error at init_last_trace function with message: %s', ex.message)
    LOGGER.info('Exit init_last_trace function')
    return result


def check_lcd_service(dct_lcd_service):
    LOGGER.info('Enter check_lcd_service function')
    result = {}
    key_code_checked = False
    key_event_checked = False
    try:
        key_code = dct_lcd_service['keyCode']
        key_event = dct_lcd_service['keyEvent']

        if key_code in LIST_KEY_CODE:
            key_code_checked = True
            LOGGER.info('Key code: %d, exist in LIST_KEY_CODE', key_code)
        else:
            LOGGER.info('Key code: %d not exists LIST_KEY_CODE', key_code)

        if key_event in LIST_KEY_EVENT:
            key_event_checked = True
            LOGGER.info('Key event: %d exists in LIST_KEY_EVENT', key_event)
        else:
            LOGGER.info('Key event: %d not exists in LIST_KEY_EVENT', key_event)

        if key_code_checked and key_event_checked:
            result = dct_lcd_service
            LOGGER.info('Check key code & key event successful')
        else:
            LOGGER.info('Fail while check ')
    except Exception as ex:
        LOGGER.error('Error at check_lcd_service function with message: %s', ex.message)
    LOGGER.info('Exit check_lcd_service function')
    return result


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


def get_menu_lv2_mcc(index):
    switcher_menu_lv2_mcc = {
        0: 'mccPeriodReadDataIO',
        1: 'mccPeriodSendTelemetry',
        2: 'mccPeriodUpdate',
        3: 'mccDcMinThreshold'
    }
    return switcher_menu_lv2_mcc.get(index, "Out of range!")