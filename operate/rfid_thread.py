import time

import requests

from config import CLIENT, shared_attributes, update_attributes, LOGGER, commands_lock, commands
from config.common import SHARED_ATTRIBUTES_RFID_CARD
from operate.update_attributes_thread import replica_client_attributes


URL_SEND_LOG ='https://backend.smartsite.dft.vn/api/services/app/DMTram/LogQuetThe'


def call():
    period = 300
    while True:
        if CLIENT.is_connected():
            if 'mccListRfid' in shared_attributes:
                list_card = shared_attributes['mccListRfid']

                list_mcc_client_attributes = replica_client_attributes()
                LOGGER.info('Get rfid card list successful from tb2: %s', list_card)
                if len(list_card) > 0:
                    rfid_card = list_mcc_client_attributes['mccCardId']
                    result = compare_rfid_card(rfid_card, list_card)
                    log = write_log(rfid_card, result)
                    if log is not None:
                        commands_lock.acquire()
                        commands[SHARED_ATTRIBUTES_RFID_CARD] = result
                        commands_lock.release()
                        send_log(log)
                    else:
                        LOGGER.info('Log is null!')
        time.sleep(period)


def compare_rfid_card(rfid_card, list_card):
    result = -1
    try:
        LOGGER.info('Go into the function write_log')
        if rfid_card in list_card:
            LOGGER.info('Card %s is in the rfid card list', rfid_card)
            result = 1
        else:
            LOGGER.info('Card %s is not in the rfid card list', rfid_card)
            result = 0
        LOGGER.info('Exit the function write_log')
        return result
    except Exception as ex:
        LOGGER.info('Exception at compare_rfid_card function: %s', ex)


def write_log(rfid_card, status):
    try:
        LOGGER.info('Go into the function write_log')
        now = round(time.time() * 1000)
        body = {"rfidCard": rfid_card, "status": status, "createdAt": now}
        LOGGER.info('Content of log: %s', body)
        LOGGER.info('Exit the function write_log')
        return body
    except Exception as ex:
        LOGGER.info('Exception at write_log function: %s', ex)


def send_log(log):
    result = False
    try:
        LOGGER.info('Go into the function send_log')
        response = requests.post(url=URL_SEND_LOG, json=log)
        if response.status_code == 200:
            LOGGER.info('Send log request to Smartsite successful!')
            result = True
        else:
            LOGGER.info('Fail while send log request to Smartsite!')
        LOGGER.info('Exit the function send_log')
        return result
    except Exception as ex:
        LOGGER.info('Exception at write_log function: %s', ex)
