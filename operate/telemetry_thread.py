import time

from config import *
from config.common import *


def call():
    period = shared_attributes.get('periodSendTelemetry', default_data.periodSendTelemetry)
    while True:
        if CLIENT.is_connected():
            telemetry = format_telemetry()
            for key, value in telemetry.items():
                CLIENT.gw_send_telemetry(key, value)
            LOGGER.info('Sent telemetry data')
            telemetries_lock.acquire()
            telemetries.clear()
            telemetries_lock.release()
        time.sleep(period)


def replica_telemetry():
    telemetry = {
        "miscTemp": 190,
        "miscHumid": 600,
        "aircTempIndoor": 35,
        "aircTempOutdoor": 85,
        "aircHumidIndoor": 30,
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
        "atuAtu1X": 10,
        "atuAtu1Y": 20,
        "atuAtu1Z": 30,
        "atuAtu2X": 10,
        "atuAtu2Y": 20,
        "atuAtu2Z": 30,
        "atuAtu3X": 10,
        "atuAtu3Y": 20,
        "atuAtu3Z": 30,
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


def format_telemetry():
    list_telemetry = {DEVICE_MISC: [{}], DEVICE_AIRC: [{}], DEVICE_ATS: [{}], DEVICE_ATU: [{}], DEVICE_DC: [{}]}
    telemetry_misc = {}
    telemetry_airc = {}
    telemetry_ats = {}
    telemetry_atu = {}
    telemetry_dc = {}
    data_from_stm32 = replica_telemetry()
    for key, value in data_from_stm32.items():
        if 'misc' in key:
            telemetry_misc[key] = value
        elif 'airc' in key:
            telemetry_airc[key] = value
        elif 'ats' in key:
            telemetry_ats[key] = value
        elif 'atu' in key:
            telemetry_atu[key] = value
        elif 'dc' in key:
            telemetry_dc[key] = value

    if telemetry_misc:
        list_telemetry[DEVICE_MISC] = [telemetry_misc]
    if telemetry_airc:
        list_telemetry[DEVICE_AIRC] = [telemetry_airc]
    if telemetry_ats:
        list_telemetry[DEVICE_ATS] = [telemetry_ats]
    if telemetry_atu:
        list_telemetry[DEVICE_ATU] = [telemetry_atu]
    if telemetry_dc:
        list_telemetry[DEVICE_DC] = [telemetry_dc]

    return list_telemetry
