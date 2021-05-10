import time

from config import *
from config.common import *


def call():
    period = shared_attributes.get('mccPeriodUpdate', default_data.mccPeriodUpdate)
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
        "mccDin4": 0,
        "mccDin5": 0,
        "mccDin6": 0,
        "mccDin7": 0,
        "mccFanState": 0,
        "mccBellState": 0,
        "mccV12": 1,
        "mccVbus": 1,
        "acmOnlineStatus": 1,
        "acmAirc1RunState": 0,
        "acmAirc1Error": 0,
        "acmAirc2RunState": 0,
        "acmAirc2Error": 0,
        "acmAirc1RunThreshold": 26,
        "acmAirc2RunThreshold": 26,
        "acmAirc1Command": 1,
        "acmAirc2Command": 1,
        "acmIrStatus": 1,
        "acmLearnCmdId": 0,
        "atsOnlineStatus": 1,
        "atsType": 1,
        "atsBatFull": 1,
        "atsIsAllBatFull": 0,
        "atsGscType": 1,
        "atsGscPwrCounter": 1,
        "atsGscAlarm": 0,
        "mccOnlineStatus": 1,
        "mccCardId": "AAA",
        "dcOnlineStatus": 1,
        "dcRectState": 1
    }

    return attributes


def fake_shared_attributes():
    attributes = {
        "mccPeriodReadDataIO": 0.05,
        "mccPeriodSendTelemetry": 50,
        "mccPeriodUpdate": 5,
        "mccExpectedTemp": 26,
        "mccMinTemp": 20,
        "mccMaxTemp": 32,
        "mccMaxHumid": 80,
        "mccFanControlAuto": 1,
        "acmControlAuto": 1,
        "acmBalance": 2,
        "acmVacThThreshold": 180,
        "acmGenAllow": 1,
        "acmCycle": 180,
        "atsControlAuto": 1,
        "atsMaxRunTime": 240,
        "atsMinRestTime": 120,
        "atsTestEn": 0,
        "atsVdcThreshold": 48,
        "atsVacThreshold": 160,
        "atsTestStart": 0,
        "atsTestCycle": 10080,
        "atsTestTime": 5,
        "mccControlAuto": 1
    }

    return attributes


def format_client_attributes(dict_attributes):
    list_client_attributes = {DEVICE_MCC_1: {}, DEVICE_ATS_1: {}, DEVICE_ACM_1: {}}
    client_attributes_mcc_1 = {}
    client_attributes_ats_1 = {}
    client_attributes_acm_1 = {}
    data_from_stm32 = dict_attributes

    for key, value in data_from_stm32.items():
        if 'mcc' in key:
            client_attributes_mcc_1[key] = value
        elif 'ats' in key:
            client_attributes_ats_1[key] = value
        elif 'acm' in key:
            client_attributes_acm_1[key] = value

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
