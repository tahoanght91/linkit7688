import time

from config import CLIENT, shared_attributes, update_attributes, LOGGER
from operate.update_attributes_thread import replica_client_attributes


def call():
    period = 30
    while True:
        if CLIENT.is_connected():
            if 'mccListRfid' in shared_attributes:
                list_card = shared_attributes['mccListRfid']
                list_mcc_client_attributes = update_attributes
                LOGGER.info('Get rfid card list successful from tb2: %s', list_card)
                if len(list_card) > 0:
                    rfid_card = list_mcc_client_attributes['mccCardId']
                    result = compare_rfid_card(rfid_card, list_card)
                    if result == 1:
                        print('OK')
                    else:
                        print('ERROR')
        time.sleep(period)


def compare_rfid_card(rfid_card, list_card):
    if rfid_card in list_card:
        LOGGER.info('Card %s is in the rfid card list', rfid_card)
        return 1
    else:
        LOGGER.info('Card %s is not in the rfid card list', rfid_card)
        return -1

