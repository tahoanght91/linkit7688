import time
from random import randint

from config import *
from config.common import *


def call():
    period = shared_attributes.get('mccPeriodSendTelemetry', default_data.mccPeriodSendTelemetry)
    while True:
        if CLIENT.is_connected():
            telemetry = format_telemetry(replica_telemetry())
            for key, value in telemetry.items():
                CLIENT.gw_send_telemetry(key, value)
            LOGGER.info('Sent telemetry data')
            telemetries_lock.acquire()
            telemetries.clear()
            telemetries_lock.release()
        time.sleep(period)


def replica_telemetry():
    telemetry = {
        "mccFireState": 0,
        "mccSmokeState": 0,
        "mccFloodState": 0,
        "mccMoveSensor": 0,
        "acmAircTemp": randint(0, 100),
        "acmAircHumid": randint(0, 100),
        "acmAirc1Temp": 30,
        "acmAirc2Temp": 26,
        "acmOutdoorTemp": 36,
        "atsVacP1": 220,
        "atsVacP2": 10,
        "atsVacP3": 11,
        "atsVacFreq": 13,
        "atsVgenP1": 10,
        "atsVgenP2": 11,
        "atsVgenP3": 12,
        "atsVgenFreq": 17,
        "atsVloadP1": 20,
        "atsVloadP2": 21,
        "atsVloadP3": 22,
        "atsVloadFreq": 23,
        "atsIloadP1": 24,
        "atsIloadP2": 21,
        "atsIloadP3": 22,
        "atsGscOil": 11,
        "atsGscCoolantTemp": 27,
        "atsGscFuel": 31,
        "atsGscVbat": 34,
        "atsGscSpeed": 32,
        "atsGscPowerTotal": 125,
        "atsGscPower1": randint(0, 100),
        "atsGscPower2": randint(0, 100),
        "atsGscPower3": randint(0, 100),
        "atsGscKvaTotal": 40,
        "atsGscKva1": 10,
        "atsGscKva2": 20,
        "atsGscKva3": 10,
        "atsGscRunHoursCounter": 60,
        "atsGscCrankCounter": 10,
        "atsCommState": 1,
        "atsMode": 0,
        "atsContactorState": 1,
        "mccDcVdc": 21,
        "mccDcIbat1": 22,
        "mccDcBat1Temp": 23,
        "mccDcVbat1Div2": 30,
        "mccDcIbat2": 12,
        "mccDcBat2Temp": 13,
        "mccDcVbat2Div2": 14,
        "mccDcIbat3": 15,
        "mccDcBat3Temp": 16,
        "mccDcVbat3Div2": 17,
        "mccDcIbat4": 18,
        "mccDcBat4Temp": 19,
        "mccDcVbat4Div2": 20,
        "mccDoorState": 1

    }

    return telemetry


def format_telemetry(dict_telemetry):
    list_telemetry = {DEVICE_MCC_1: [{}], DEVICE_ATS_1: [{}], DEVICE_ACM_1: [{}]}
    telemetry_mcc_1 = {}
    telemetry_ats_1 = {}
    telemetry_acm_1 = {}
    data_from_stm32 = dict_telemetry

    for key, value in data_from_stm32.items():
        if 'mcc' in key:
            telemetry_mcc_1[key] = value
        elif 'ats' in key:
            telemetry_ats_1[key] = value
        elif 'acm' in key:
            telemetry_acm_1[key] = value

    if telemetry_mcc_1:
        list_telemetry[DEVICE_MCC_1] = [telemetry_mcc_1]
    if telemetry_ats_1:
        list_telemetry[DEVICE_ATS_1] = [telemetry_ats_1]
    if telemetry_acm_1:
        list_telemetry[DEVICE_ACM_1] = [telemetry_acm_1]

    return list_telemetry
