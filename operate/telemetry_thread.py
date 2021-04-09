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
                "miscTemp": telemetries['miscTemp'],
                "miscHumid": telemetries['miscHumid']
            }
        ],
        "device_airc": [
            {
                "aircTemp": telemetries['aircTemp'],
                "aircHumid": telemetries['aircHumid'],
                "aircAirc1Temp": telemetries['aircAirc1Temp'],
                "aircAirc2Temp": telemetries['aircAirc2Temp'],
                "aircOutdoorTemp": telemetries['aircOutdoorTemp']
            }
        ],
        "device_ats": [
            {
                "atsVacP1": telemetries['atsVacP1'],
                "atsVacP2": telemetries['atsVacP2'],
                "atsVacP3": telemetries['atsVacP3'],
                "atsVacFreq": telemetries['atsVacFreq'],
                "atsVgenP1": telemetries['atsVgenP1'],
                "atsVgenP2": telemetries['atsVgenP2'],
                "atsVgenP3": telemetries['atsVgenP3'],
                "atsVgenFreq": telemetries['atsVgenFreq'],
                "atsVloadP1": telemetries['atsVloadP1'],
                "atsVloadP2": telemetries['atsVloadP2'],
                "atsVloadP3": telemetries['atsVloadP3'],
                "atsVloadFreq": telemetries['atsVloadFreq'],
                "atsIloadP1": telemetries['atsIloadP1'],
                "atsIloadP2": telemetries['atsIloadP2'],
                "atsIloadP3": telemetries['atsIloadP3'],
                "atsGscOil": telemetries['atsGscOil'],
                "atsGscCoolantTemp": telemetries['atsGscCoolantTemp'],
                "atsGscFuel": telemetries['atsGscFuel'],
                "atsGscVbat": telemetries['atsGscVbat'],
                "atsGscSpeed": telemetries['atsGscSpeed'],
                "atsGscPowerTotal": telemetries['atsGscPowerTotal'],
                "atsGscPower1": telemetries['atsGscPower1'],
                "atsGscPower2": telemetries['atsGscPower2'],
                "atsGscPower3": telemetries['atsGscPower3'],
                "atsGscKvaTotal": telemetries['atsGscKvaTotal'],
                "atsGscKva1": telemetries['atsGscKva1'],
                "atsGscKva2": telemetries['atsGscKva2'],
                "atsGscKva3": telemetries['atsGscKva3'],
                "atsGscRunHoursCounter": telemetries['atsGscRunHoursCounter'],
                "atsGscCrankCounter": telemetries['atsGscCrankCounter']
            }
        ],
        "device_atu": [
            {
                "atuAtu1X": telemetries['atuAtu1X'],
                "atuAtu1Y": telemetries['atuAtu1Y'],
                "atuAtu1Z": telemetries['atuAtu1Z'],
                "atuAtu2X": telemetries['atuAtu2X'],
                "atuAtu2Y": telemetries['atuAtu2Y'],
                "atuAtu2Z": telemetries['atuAtu2Z'],
                "atuAtu3X": telemetries['atuAtu3X'],
                "atuAtu3Y": telemetries['atuAtu3Y'],
                "atuAtu3Z": telemetries['atuAtu3Z']
            }
        ],
        "device_dc": [
            {
                "dcVdc": telemetries['dcVdc'],
                "dcIbat1": telemetries['dcIbat1'],
                "dcBat1Temp": telemetries['dcBat1Temp'],
                "dcVbat1Div2": telemetries['dcVbat1Div2'],
                "dcIbat2": telemetries['dcIbat2'],
                "dcBat2Temp": telemetries['dcBat2Temp'],
                "dcVbat2Div2": telemetries['dcVbat2Div2'],
                "dcIbat3": telemetries['dcIbat3'],
                "dcBat3Temp": telemetries['dcBat3Temp'],
                "dcVbat3Div2": telemetries['dcVbat3Div2'],
                "dcIbat4": telemetries['dcIbat4'],
                "dcBat4Temp": telemetries['dcBat4Temp'],
                "dcVbat4Div2": telemetries['dcVbat4Div2']
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
