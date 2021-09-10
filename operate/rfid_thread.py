import time

import requests

from config import *
from config.common import RESPONSE_RFID
from config.common_api import *

from monitor import mcc

url_send_log_rfid = PREFIX + DOMAIN + API_SAVE_LOG_RFID
KEY_RFID = 'mccRfidCard'
lcd_setting_data_file = './lcd_setting_data_file.json'


def call():
    from control.utils import read_to_json
    period = 3
    while True:
        file_setting = read_to_json(lcd_setting_data_file)
        if CLIENT.is_connected() and file_setting['setting_rfid_allow'] == 1:
            if 'mccListRfid' in shared_attributes:
                list_card = shared_attributes['mccListRfid']
                LOGGER.debug('Get rfid card list successful from thingsboard: %s', list_card)
                if len(list_card) > 0:
                    if KEY_RFID in client_attributes:
                        rfid_card = client_attributes.get(KEY_RFID)
                        if isinstance(rfid_card, str) and rfid_card is not None:
                            result = compare_rfid_card(rfid_card, list_card)
                            if result == -1 or result == 0 or result == 1:
                                log = write_log(rfid_card, result)
                                client_attributes.pop(KEY_RFID)
                                if result == 0 or result == 1:
                                    commands_lock.acquire()
                                    commands[RESPONSE_RFID] = result
                                    commands_lock.release()
                                    if result == 1:
                                        mcc.open_door_with_auto_close()
                                if log is not None:
                                    send_log(log)
                                else:
                                    LOGGER.debug('Log is null!')
                            else:
                                LOGGER.debug('Response of compare card is not expected with result: %s', str(result))
                        else:
                            LOGGER.debug('Rfid card is not string or null')
                    else:
                        LOGGER.debug('Not found mccRfidCard in dictionary update_attributes')
                else:
                    LOGGER.debug('Length of card is 0 or less than 0')
            else:
                LOGGER.debug('Not found list of rfid card in shared attributes')
        else:
            LOGGER.debug('Gateway is disconnect from Thingsboard or allow read rfid is: 1')
        time.sleep(period)


def compare_rfid_card(rfid_card, list_card):
    result = -1
    try:
        set_temp = set(list_card)
        if rfid_card in set_temp:
            LOGGER.debug('Card %s is in the rfid card list', rfid_card)
            result = 1
        else:
            LOGGER.debug('Card %s is not in the rfid card list', rfid_card)
            result = 0
    except Exception as ex:
        LOGGER.warning('Error at compare_rfid_card function with message: %s', ex.message)
    return result


def write_log(rfid_card, status):
    try:
        now = round(time.time() * 1000)
        body = {"gatewayId": CLIENT_ID, "rfidCard": rfid_card, "status": status, "createdAt": now}
        LOGGER.info('Content of log: %s', body)
        return body
    except Exception as ex:
        LOGGER.warning('Error at write_log function with message: %s', ex.message)


def send_log(log):
    result = False
    try:
        response = requests.post(url=url_send_log_rfid, json=log)
        if response.status_code == 200:
            LOGGER.debug('Send log request to Smartsite successful!')
            result = True
        else:
            LOGGER.debug('Fail while send log request to Smartsite!')
        return result
    except Exception as ex:
        LOGGER.warning('Error at write_log function with message: %s', ex.message)

