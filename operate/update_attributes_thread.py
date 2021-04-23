import time

from config import *
from config.common import *


def call():
    period = shared_attributes.get('periodUpdate', default_data.periodUpdate)
    while True:
        if CLIENT.is_connected():
            update_attributes_lock.acquire()
            gw_client_attributes = format_client_attributes(replica_client_attributes())
            gw_shared_attributes = format_client_attributes(fake_shared_attributes())
            if gw_client_attributes:
                for key, value in gw_client_attributes.items():
                    CLIENT.gw_send_attributes(key, value)
                if gw_shared_attributes:
                    for key, value in gw_shared_attributes.items():
                        CLIENT.gw_send_attributes(key, value)
                LOGGER.info('Sent changed client attributes')
                log_info = []
                for key, value in update_attributes.items():
                    log_info.append('\t{:>20s}: {:>20s}'.format(str(key), str(value)))
                LOGGER.info('\n'.join(log_info))
                update_attributes.clear()
            update_attributes_lock.release()
        time.sleep(period)


def replica_client_attributes():
    attributes = {
        "fireState": 0,
        "offOnFire": 0,
        "smokeState": 0,
        "floodState": 0,
        "moveSensor": 0,
        "miscDin4": 0,
        "miscDin5": 0,
        "miscDin6": 0,
        "miscDin7": 0,
        "miscFanState": 0,
        "miscBellState": 0,
        "miscV12": 1,
        "miscVbus": 1,
        "aircOnlineStatus": 1,
        "aircAirc1RunState": 0,
        "aircAirc1Error": 0,
        "aircAirc2RunState": 0,
        "aircAirc2Error": 0,
        "aircAirc1RunThreshold": 26,
        "aircAirc2RunThreshold": 26,
        "aircAirc1Command": 1,
        "aircAirc2Command": 1,
        "aircIrStatus": 1,
        "aircLearnCmdId": 0,
        "atsOnlineStatus": 1,
        "atsCommState": 1,
        "atsMode": 0,
        "atsType": 1,
        "atsContactorState": 1,
        "atsBatFull": 1,
        "atsIsAllBatFull": 0,
        "atsGscType": 1,
        "atsGscPwrCounter": 1,
        "atsGscAlarm": 0,
        "atuOnlineStatus": 1,
        "crmuOnlineStatus": 1,
        "crmuCardId": "AAA",
        "crmuDoorState": 1,
        "dcOnlineStatus": 1,
        "dcRectState": 1
    }

    return attributes


def fake_shared_attributes():
    attributes = {
        "periodReadDataIO": 0.05,
        "periodSendTelemetry": 50,
        "periodUpdate": 5,
        "miscExpectedTemp": 26,
        "miscMinTemp": 20,
        "miscMaxTemp": 32,
        "miscMaxHumid": 80,
        "miscFanControlAuto": 1,
        "aircControlAuto": 1,
        "aircBalance": 2,
        "aircVacThThreshold": 180,
        "aircGenAllow": 1,
        "aircCycle": 180,
        "atsControlAuto": 1,
        "atsMaxRunTime": 240,
        "atsMinRestTime": 120,
        "atsTestEn": 0,
        "atsVdcThreshold": 48,
        "atsVacThreshold": 160,
        "atsTestStart": 0,
        "atsTestCycle": 10080,
        "atsTestTime": 5,
        "crmuControlAuto": 1
    }

    return attributes


def format_client_attributes(dict_attributes):
    list_client_attributes = {DEVICE_MDC_1: {}, DEVICE_MCC_1: {}, DEVICE_ATS_1: {}, DEVICE_ACM_1: {}}
    client_attributes_mdc_1 = {}
    client_attributes_mcc_1 = {}
    client_attributes_ats_1 = {}
    client_attributes_acm_1 = {}
    data_from_stm32 = dict_attributes

    for key, value in data_from_stm32.items():
        if 'crmu' in key:
            client_attributes_mdc_1[key] = value
        elif 'ats' in key:
            client_attributes_ats_1[key] = value
        elif 'airc' in key:
            client_attributes_acm_1[key] = value
        else:
            client_attributes_mcc_1[key] = value

    if client_attributes_mdc_1:
        list_client_attributes[DEVICE_MDC_1] = client_attributes_mdc_1
    if client_attributes_ats_1:
        list_client_attributes[DEVICE_ATS_1] = client_attributes_ats_1
    if client_attributes_acm_1:
        list_client_attributes[DEVICE_ACM_1] = client_attributes_acm_1
    if client_attributes_mcc_1:
        list_client_attributes[DEVICE_MCC_1] = client_attributes_mcc_1

    return list_client_attributes


def get_list_key(dict_attributes):
    list_keys = []
    for key in dict_attributes.keys():
        list_keys.append(key)

    return list_keys
