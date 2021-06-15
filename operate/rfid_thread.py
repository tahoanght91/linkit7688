import time

import requests

from config import CLIENT, shared_attributes, update_attributes, LOGGER
from monitor import mcc

URL_SEND_LOG ='https://backend.smartsite.dft.vn/api/services/app/DMTram/LogQuetThe'
KEY_RFID = 'mccRfidCard'


def call():
    period = 1
    while True:
        if CLIENT.is_connected():
            if 'mccListRfid' in shared_attributes:
                LOGGER.info('List rfid existence in shared attributes')
                list_card = shared_attributes['mccListRfid']
                LOGGER.info('Get rfid card list successful from thingsboard: %s', list_card)
                if len(list_card) > 0:
                    rfid_card = check_key(KEY_RFID, update_attributes)
                    if isinstance(rfid_card, str) and rfid_card is not None:
                        result = compare_rfid_card(rfid_card, list_card)
                        if result == -1 or result == 0 or result == 1:
                            log = write_log(rfid_card, result)
                            del update_attributes[KEY_RFID]
                            if log is not None:
                                mcc.open_door_with_auto_close()
                                send_log(log)
                            else:
                                LOGGER.info('Log is null!')
                        else:
                            LOGGER.info('Response of compare card is not expected with result: %s', str(result))
                    else:
                        LOGGER.info('Rfid card is not string or null')
                else:
                    LOGGER.info('Length of card is 0 or less than 0')
            else:
                LOGGER.info('Not found list of rfid card in shared attributes')
        time.sleep(period)


def check_key(key, dict):
    LOGGER.info('Enter check_key function')
    try:
        if key in dict.keys():
            LOGGER.info('Key existence in client attributes')
            LOGGER.info('Exit check_key function')
            return key
        else:
            LOGGER.info('Key not existence in client attributes')
            LOGGER.info('Exit check_key function')
            return -1
    except Exception as ex:
        LOGGER.error('Error at check_key function with message: %s', ex.message)


def compare_rfid_card(rfid_card, list_card):
    LOGGER.info('Enter compare_rfid_card function ')
    result = -1
    try:
        set_temp = set(list_card)
        if rfid_card in set_temp:
            LOGGER.info('Card %s is in the rfid card list', rfid_card)
            result = 1
        else:
            LOGGER.info('Card %s is not in the rfid card list', rfid_card)
            result = 0
    except Exception as ex:
        LOGGER.error('Error at compare_rfid_card function with message: %s', ex.message)
    LOGGER.info('Exit compare_rfid_card function')
    return result


def write_log(rfid_card, status):
    try:
        LOGGER.info('Enter write_log function')
        now = round(time.time() * 1000)
        body = {"rfidCard": rfid_card, "status": status, "createdAt": now}
        LOGGER.info('Content of log: %s', body)
        LOGGER.info('Exit the function write_log')
        return body
    except Exception as ex:
        LOGGER.info('Error at write_log function with message: %s', ex.message)


def send_log(log):
    result = False
    try:
        LOGGER.info('Enter send_log function')
        response = requests.post(url=URL_SEND_LOG, json=log)
        if response.status_code == 200:
            LOGGER.info('Send log request to Smartsite successful!')
            result = True
        else:
            LOGGER.info('Fail while send log request to Smartsite!')
        LOGGER.info('Exit the function send_log')
        return result
    except Exception as ex:
        LOGGER.info('Error at write_log function with message: %s', ex.message)

