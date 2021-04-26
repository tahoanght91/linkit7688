import time

from config import *
from config.common import *


def call():
    period = shared_attributes.get('periodSendTelemetry', default_data.periodSendTelemetry)
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
        "fireState": 0,
        "offOnFire": 0,
        "smokeState": 0,
        "floodState": 0,
        "moveSensor": 0,
        "miscTemp": 19,
        "miscHumid": 60,
        "aircTemp": 35,
        "aircHumid": 85,
        "aircAirc1Temp": 30,
        "aircAirc2Temp": 26,
        "aircOutdoorTemp": 36,
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
        "atsGscPower1": 45,
        "atsGscPower2": 40,
        "atsGscPower3": 40,
        "atsGscKvaTotal": 40,
        "atsGscKva1": 10,
        "atsGscKva2": 20,
        "atsGscKva3": 10,
        "atsGscRunHoursCounter": 60,
        "atsGscCrankCounter": 10,
        "atuAtu1X": 10,
        "atuAtu1Y": 20,
        "atuAtu1Z": 30,
        "atuAtu2X": 10,
        "atuAtu2Y": 20,
        "atuAtu2Z": 30,
        "atuAtu3X": 10,
        "atuAtu3Y": 20,
        "atuAtu3Z": 30,
        "dcVdc": 21,
        "dcIbat1": 22,
        "dcBat1Temp": 23,
        "dcVbat1Div2": 30,
        "dcIbat2": 12,
        "dcBat2Temp": 13,
        "dcVbat2Div2": 14,
        "dcIbat3": 15,
        "dcBat3Temp": 16,
        "dcVbat3Div2": 17,
        "dcIbat4": 18,
        "dcBat4Temp": 19,
        "dcVbat4Div2": 20
    }

    return telemetry


def format_telemetry(dict_telemetry):
    list_telemetry = {DEVICE_MDC_1: [{}], DEVICE_MCC_1: [{}], DEVICE_ATS_1: [{}], DEVICE_ACM_1: [{}]}
    telemetry_mdc_1 = {}
    telemetry_mcc_1 = {}
    telemetry_ats_1 = {}
    telemetry_acm_1 = {}
    data_from_stm32 = dict_telemetry

    for key, value in data_from_stm32.items():
        if 'crmu' in key:
            telemetry_mdc_1[key] = value
        elif 'ats' in key:
            telemetry_ats_1[key] = value
        elif 'airc' in key:
            telemetry_acm_1[key] = value
        else:
            telemetry_mcc_1[key] = value

    if telemetry_mdc_1:
        list_telemetry[DEVICE_MDC_1] = [telemetry_mdc_1]
    if telemetry_mcc_1:
        list_telemetry[DEVICE_MCC_1] = [telemetry_mcc_1]
    if telemetry_ats_1:
        list_telemetry[DEVICE_ATS_1] = [telemetry_ats_1]
    if telemetry_acm_1:
        list_telemetry[DEVICE_ACM_1] = [telemetry_acm_1]

    return list_telemetry


# def format_telemetry():
#     list_telemetry = {DEVICE_MISC: [{}], DEVICE_AIRC: [{}], DEVICE_ATS: [{}], DEVICE_ATU: [{}], DEVICE_DC: [{}]}
#     telemetry_misc = {}
#     telemetry_airc = {}
#     telemetry_ats = {}
#     telemetry_atu = {}
#     telemetry_dc = {}
#     data_from_stm32 = replica_telemetry()
#     for key, value in data_from_stm32.items():
#         if 'misc' in key:
#             telemetry_misc[key] = value
#         elif 'airc' in key:
#             telemetry_airc[key] = value
#         elif 'ats' in key:
#             telemetry_ats[key] = value
#         elif 'atu' in key:
#             telemetry_atu[key] = value
#         elif 'dc' in key:
#             telemetry_dc[key] = value
#
#     if telemetry_misc:
#         list_telemetry[DEVICE_MISC] = [telemetry_misc]
#     if telemetry_airc:
#         list_telemetry[DEVICE_AIRC] = [telemetry_airc]
#     if telemetry_ats:
#         list_telemetry[DEVICE_ATS] = [telemetry_ats]
#     if telemetry_atu:
#         list_telemetry[DEVICE_ATU] = [telemetry_atu]
#     if telemetry_dc:
#         list_telemetry[DEVICE_DC] = [telemetry_dc]
#
#     return list_telemetry
