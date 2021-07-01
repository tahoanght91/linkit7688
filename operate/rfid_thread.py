import time

import requests

from config import *
from config.common import RESPONSE_RFID
from monitor import mcc

URL_SEND_LOG ='https://backend.smartsite.dft.vn/api/services/app/DMTram/LogQuetThe'
KEY_RFID = 'mccRfidCard'


def call():
    period = 3
    while True:
        if CLIENT.is_connected():
            if 'mccListRfid' in shared_attributes:
                LOGGER.info('List rfid existence in shared attributes')
                list_card = shared_attributes['mccListRfid']
                LOGGER.info('Get rfid card list successful from thingsboard: %s', list_card)
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
        time.sleep(period)


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
        body = {"gatewayId": CLIENT_ID, "rfidCard": rfid_card, "status": status, "createdAt": now}
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

