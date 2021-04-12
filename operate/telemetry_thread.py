import time

from config import *


# def call():
#     period = shared_attributes.get('periodSendTelemetry', default_data.periodSendTelemetry)
#     while True:
#         if CLIENT.is_connected():
#             fake_telemetry = generate_fake_telemetry()
#             base = fake_telemetry.items()
#             for key, value in base:
#                 CLIENT.gw_send_telemetry(key, value)
#             LOGGER.info('Sent telemetry data')
#             telemetries_lock.acquire()
#             telemetries.clear()
#             telemetries_lock.release()
#         time.sleep(period)


def call():
    period = shared_attributes.get('periodSendTelemetry', default_data.periodSendTelemetry)
    while True:
        if CLIENT.is_connected():
            real_telemetry = format_telemetry()
            base = real_telemetry.items()
            for key, value in base:
                CLIENT.gw_send_telemetry(key, value)
            LOGGER.info('Sent telemetry data')
            telemetries_lock.acquire()
            telemetries.clear()
            telemetries_lock.release()
        time.sleep(period)


def format_telemetry():
    transform_telemetry = {
        "device_misc": [
            {
                "miscTemp": telemetries['miscTemp'] if 'miscTemp' in telemetries else 0,
                "miscHumid": telemetries['miscHumid'] if 'miscHumid' in telemetries else 0
            }
        ],
        "device_airc": [
            {
                "aircTemp": telemetries['aircTemp'] if 'aircTemp' in telemetries else 0,
                "aircHumid": telemetries['aircHumid'] if 'aircHumid' in telemetries else 0,
                "aircAirc1Temp": telemetries['aircAirc1Temp'] if 'aircAirc1Temp' in telemetries else 0,
                "aircAirc2Temp": telemetries['aircAirc2Temp'] if 'aircAirc2Temp' in telemetries else 0,
                "aircOutdoorTemp": telemetries['aircOutdoorTemp'] if 'aircOutdoorTemp' in telemetries else 0
            }
        ],
        "device_ats": [
            {
                "atsVacP1": telemetries['atsVacP1'] if 'atsVacP1' in telemetries else 0,
                "atsVacP2": telemetries['atsVacP2'] if 'atsVacP2' in telemetries else 0,
                "atsVacP3": telemetries['atsVacP3'] if 'atsVacP3' in telemetries else 0,
                "atsVacFreq": telemetries['atsVacFreq'] if 'atsVacFreq' in telemetries else 0,
                "atsVgenP1": telemetries['atsVgenP1'] if 'atsVgenP1' in telemetries else 0,
                "atsVgenP2": telemetries['atsVgenP2'] if 'atsVgenP2' in telemetries else 0,
                "atsVgenP3": telemetries['atsVgenP3'] if 'atsVgenP3' in telemetries else 0,
                "atsVgenFreq": telemetries['atsVgenFreq'] if 'atsVgenFreq' in telemetries else 0,
                "atsVloadP1": telemetries['atsVloadP1'] if 'atsVloadP1' in telemetries else 0,
                "atsVloadP2": telemetries['atsVloadP2'] if 'atsVloadP2' in telemetries else 0,
                "atsVloadP3": telemetries['atsVloadP3'] if 'atsVloadP3' in telemetries else 0,
                "atsVloadFreq": telemetries['atsVloadFreq'] if 'atsVloadFreq' in telemetries else 0,
                "atsIloadP1": telemetries['atsIloadP1'] if 'atsIloadP1' in telemetries else 0,
                "atsIloadP2": telemetries['atsIloadP2'] if 'atsIloadP2' in telemetries else 0,
                "atsIloadP3": telemetries['atsIloadP3'] if 'atsIloadP3' in telemetries else 0,
                "atsGscOil": telemetries['atsGscOil'] if 'atsGscOil' in telemetries else 0,
                "atsGscCoolantTemp": telemetries['atsGscCoolantTemp'] if 'atsGscCoolantTemp' in telemetries else 0,
                "atsGscFuel": telemetries['atsGscFuel'] if 'atsGscFuel' in telemetries else 0,
                "atsGscVbat": telemetries['atsGscVbat'] if 'atsGscVbat' in telemetries else 0,
                "atsGscSpeed": telemetries['atsGscSpeed'] if 'atsGscSpeed' in telemetries else 0,
                "atsGscPowerTotal": telemetries['atsGscPowerTotal'] if 'atsGscPowerTotal' in telemetries else 0,
                "atsGscPower1": telemetries['atsGscPower1'] if 'atsGscPower1' in telemetries else 0,
                "atsGscPower2": telemetries['atsGscPower2'] if 'atsGscPower2' in telemetries else 0,
                "atsGscPower3": telemetries['atsGscPower3'] if 'atsGscPower3' in telemetries else 0,
                "atsGscKvaTotal": telemetries['atsGscKvaTotal'] if 'atsGscKvaTotal' in telemetries else 0,
                "atsGscKva1": telemetries['atsGscKva1'] if 'atsGscKva1' in telemetries else 0,
                "atsGscKva2": telemetries['atsGscKva2'] if 'atsGscKva2' in telemetries else 0,
                "atsGscKva3": telemetries['atsGscKva3'] if 'atsGscKva3' in telemetries else 0,
                "atsGscRunHoursCounter": telemetries['atsGscRunHoursCounter'] if 'atsGscRunHoursCounter' in telemetries else 0,
                "atsGscCrankCounter": telemetries['atsGscCrankCounter'] if 'atsGscCrankCounter' in telemetries else 0
            }
        ],
        "device_atu": [
            {
                "atuAtu1X": telemetries['atuAtu1X']  if 'atuAtu1X' in telemetries else 0,
                "atuAtu1Y": telemetries['atuAtu1Y']  if 'atuAtu1Y' in telemetries else 0,
                "atuAtu1Z": telemetries['atuAtu1Z']  if 'atuAtu1Z' in telemetries else 0,
                "atuAtu2X": telemetries['atuAtu2X']  if 'atuAtu2X' in telemetries else 0,
                "atuAtu2Y": telemetries['atuAtu2Y']  if 'atuAtu2Y' in telemetries else 0,
                "atuAtu2Z": telemetries['atuAtu2Z']  if 'atuAtu2Z' in telemetries else 0,
                "atuAtu3X": telemetries['atuAtu3X']  if 'atuAtu3X' in telemetries else 0,
                "atuAtu3Y": telemetries['atuAtu3Y']  if 'atuAtu3Y' in telemetries else 0,
                "atuAtu3Z": telemetries['atuAtu3Z']  if 'atuAtu3Z' in telemetries else 0
            }
        ],
        "device_dc": [
            {
                "dcVdc": telemetries['dcVdc'] if 'dcVdc' in telemetries else 0,
                "dcIbat1": telemetries['dcIbat1'] if 'dcIbat1' in telemetries else 0,
                "dcBat1Temp": telemetries['dcBat1Temp'] if 'dcBat1Temp' in telemetries else 0,
                "dcVbat1Div2": telemetries['dcVbat1Div2'] if 'dcVbat1Div2' in telemetries else 0,
                "dcIbat2": telemetries['dcIbat2'] if 'dcIbat2' in telemetries else 0,
                "dcBat2Temp": telemetries['dcBat2Temp'] if 'dcBat2Temp' in telemetries else 0,
                "dcVbat2Div2": telemetries['dcVbat2Div2'] if 'dcVbat2Div2' in telemetries else 0,
                "dcIbat3": telemetries['dcIbat3'] if 'dcIbat3' in telemetries else 0,
                "dcBat3Temp": telemetries['dcBat3Temp'] if 'dcBat3Temp' in telemetries else 0,
                "dcVbat3Div2": telemetries['dcVbat3Div2'] if 'dcVbat3Div2' in telemetries else 0,
                "dcIbat4": telemetries['dcIbat4'] if 'dcIbat4' in telemetries else 0,
                "dcBat4Temp": telemetries['dcBat4Temp'] if 'dcBat4Temp' in telemetries else 0,
                "dcVbat4Div2": telemetries['dcVbat4Div2'] if 'dcVbat4Div2' in telemetries else 0
            }
        ]
    }
    return transform_telemetry


def generate_fake_telemetry():
    telemetry = {
        "device_misc": [
            {
                "miscTemp": 19,
                "miscHumid": 60
            }
        ],
        "device_airc": [
            {
                "aircTemp": 35,
                "aircHumid": 85,
                "aircAirc1Temp": 55,
                "aircAirc2Temp": 52,
                "aircOutdoorTemp": 36
            }
        ],
        "device_ats": [
            {
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
                "atsGscCrankCounter": 10
            }
        ],
        "device_atu": [
            {
                "atuAtu1X": 10,
                "atuAtu1Y": 20,
                "atuAtu1Z": 30,
                "atuAtu2X": 10,
                "atuAtu2Y": 20,
                "atuAtu2Z": 30,
                "atuAtu3X": 10,
                "atuAtu3Y": 20,
                "atuAtu3Z": 30
            }
        ],
        "device_dc": [
            {
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
        ]
    }
    return telemetry
