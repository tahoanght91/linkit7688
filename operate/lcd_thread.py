import time

import requests

from config import *
from config.common import *
from config.common_services import *
from devices.utils import read_services
from utility import bytes_to_int

URL_SEND_SA = ''
MENU_LEVEL_1 = [MCC, ACM, ATS]
dct_last_trace = {}


def call():
    LOGGER.error('Enter call function in menu_thread')
    try:
        period = 1
        while True:
            if CLIENT.is_connected():
                result = check_lcd_service(lcd_services, dct_last_trace)
                if result != '':
                    commands_lock.acquire()
                    commands[LCD_SERVICE] = result
                    commands_lock.release()
            time.sleep(period)
    except Exception as ex:
        LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)


def get_index_menu_lv1(key_code, key_event):
    LOGGER.info('Enter get_index_menu_lv1 function')
    index = -1
    level = 1
    value = -1
    last_index = dct_last_trace['index']
    try:
        if key_event == EVENT_NONE:
            index = last_index
        elif key_event == EVENT_UP:
            index = last_index + 1
            if index > MAX_INDEX_MENU:
                index = MIN_INDEX_MENU
        elif key_event == EVENT_DOWN:
            index = last_index - 1
            if index < MIN_INDEX_MENU:
                index = MAX_INDEX_MENU
        LOGGER.info('Index of menu level 1: %d', index)
        set_last_trace(key_code, key_event, level, index, value)
    except Exception as ex:
        LOGGER.error('Error at get_index_menu_lv1 function with message: %s', ex.message)
    LOGGER.info('Exit get_index_menu_lv1 function')
    return index


def get_index_menu_lv2(dict_attributes):
    pass


def extract_lcd_service(byte_data):
    LOGGER.info('Enter extract_lcd_service function')
    try:
        key_code = bytes_to_int(byte_data[0:2])
        key_event = bytes_to_int(byte_data[3])
        read_services('keyCode', key_code)
        read_services('keyEvent', key_event)
        LOGGER.info('After extract command lcd from STM32, key code: %d, key event: %d', key_code, key_event)
    except Exception as ex:
        LOGGER.error('Error at extract_lcd_service function with message: %s', ex.message)
    LOGGER.info('Exit extract_lcd_service function')


def check_lcd_service(dct_lcd_service, dct_last_trace):
    LOGGER.info('Enter check_lcd_service function')
    str_result = ''
    try:
        key_code = dct_lcd_service['keyCode']
        key_event = dct_lcd_service['keyEvent']
        init_last_trace(dct_lcd_service, dct_last_trace)
        str_lcd_service = switcher_lcd_service(key_code)
        if str_lcd_service is MENU:
            index_menu_lv1 = get_index_menu_lv1(key_code, key_event)
            if index_menu_lv1 > 0:
                str_result = MENU_LEVEL_1[index_menu_lv1]
    except Exception as ex:
        LOGGER.error('Error at check_lcd_service function with message: %s', ex.message)
    LOGGER.info('Exit check_lcd_service function')
    return str_result


def get_last_trace():
    return dct_last_trace


def set_last_trace(key_code, key_event, level, index, value):
    LOGGER.info('Enter set_last_trace function')
    try:
        dct_last_trace['keyCode'] = key_code
        dct_last_trace['keyEvent'] = key_event
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
            dct_last_trace['level'] = 1
            dct_last_trace['index'] = 0
            dct_last_trace['value'] = -1
            LOGGER.info('Init dictionary last trace successful!')
            result = True
    except Exception as ex:
        LOGGER.error('Error at init_last_trace function with message: %s', ex.message)
    LOGGER.info('Exit init_last_trace function')
    return result


def confirm_service(service, key_event):
    pass


def switcher_lcd_service(service):
    LOGGER.info('Enter switcher_lcd_service function')
    switcher_lcd_services = {
        1: MENU
    }
    LOGGER.info('Key is: %d, after parse is: %s', service, switcher_lcd_services.get(service, 'Out of range!'))
    LOGGER.info('Exit switcher_lcd_service function')
    return switcher_lcd_services.get(service, "Out of range!")


def delete_lcd_service(key_code, key_event):
    LOGGER.info('Enter delete_lcd_service function')
    result = False
    try:
        if key_code in lcd_services and key_event in lcd_services:
            del lcd_services[key_code]
            del lcd_services[key_event]
            result = True
    except Exception as ex:
        LOGGER.error('Error at delete_lcd_services function with message: %s', ex.message)
    LOGGER.info('Exit delete_lcd_services function')
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
