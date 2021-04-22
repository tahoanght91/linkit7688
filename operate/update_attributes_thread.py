import time

from config import *
from config.common import *


def call():
    period = shared_attributes.get('periodUpdate', default_data.periodUpdate)
    while True:
        if CLIENT.is_connected():
            update_attributes_lock.acquire()
            gw_client_attributes = format_client_attributes()
            if gw_client_attributes:
                for key, value in gw_client_attributes.items():
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
        "aircAirc1Command": 0,
        "aircAirc2Command": 0,
        "aircFanCommand": 1,
        "aircThrTemp1": 1,
        "aircThrTemp2": 26,
        "aircThrTemp3": 0,
        "aircThrTemp4": 1,
        "aircAirc2RunThreshold": 0,
        "aircCount": 26,
        "aircModeAutoEn": 0,

        "atsCommState": 1,
        "atsMode": 1,
        "atsType": 0,
        "atsContactorState": 1,

        "atuOnlineStatus": 1,

        "crmuCardId": "AAA",
        "crmuDoorState": 1,
        "crmuLen": 1,

        "miscBellState": 0,
        "miscFanState": 0,
        "miscVbus": 1,
        "miscV12": 1,
        "floodState": 1,
        "moveSensor": 1,
        "fireState": 1,
        "smokeState": 1,
        "miscDin7": 0,
        "miscDin6": 0,
        "miscDin5": 0,
        "miscDin4": 0,

        "dcOnlineStatus": 22,
        "dcRectState": 111
    }

    return attributes


def format_client_attributes():
    list_client_attributes = {DEVICE_MISC: {}, DEVICE_AIRC: {}, DEVICE_ATS: {}, DEVICE_ATU: {},
                              DEVICE_DC: {}, DEVICE_CRMU: {}, DEVICE_FIRE_SENSOR: {}, DEVICE_SMOKE_SENSOR: {},
                              DEVICE_MOVE_SENSOR: {}, DEVICE_FLOOD_SENSOR: {}}
    client_attributes_misc = {}
    client_attributes_airc = {}
    client_attributes_ats = {}
    client_attributes_atu = {}
    client_attributes_dc = {}
    client_attributes_crmu = {}
    client_attributes_fire_sensor = {}
    client_attributes_smoke_sensor = {}
    client_attributes_move_sensor = {}
    client_attributes_flood_sensor = {}
    data_from_stm32 = replica_client_attributes()

    for key, value in data_from_stm32.items():
        if 'misc' in key:
            client_attributes_misc[key] = value
        elif 'airc' in key:
            client_attributes_airc[key] = value
        elif 'ats' in key:
            client_attributes_ats[key] = value
        elif 'dc' in key:
            client_attributes_dc[key] = value
        elif 'atu' in key:
            client_attributes_atu[key] = value
        elif 'crmu' in key:
            client_attributes_crmu[key] = value
        elif 'fireState' in key:
            client_attributes_fire_sensor[key] = value
        elif 'smokeState' in key:
            client_attributes_smoke_sensor[key] = value
        elif 'moveSensor' in key:
            client_attributes_move_sensor[key] = value
        elif 'floodState' in key:
            client_attributes_flood_sensor[key] = value

    if client_attributes_misc:
        list_client_attributes[DEVICE_MISC] = client_attributes_misc
    if client_attributes_airc:
        list_client_attributes[DEVICE_AIRC] = client_attributes_airc
    if client_attributes_ats:
        list_client_attributes[DEVICE_ATS] = client_attributes_ats
    if client_attributes_atu:
        list_client_attributes[DEVICE_ATU] = client_attributes_atu
    if client_attributes_dc:
        list_client_attributes[DEVICE_DC] = client_attributes_dc
    if client_attributes_crmu:
        list_client_attributes[DEVICE_CRMU] = client_attributes_crmu
    if client_attributes_fire_sensor:
        list_client_attributes[DEVICE_FIRE_SENSOR] = client_attributes_fire_sensor
    if client_attributes_smoke_sensor:
        list_client_attributes[DEVICE_SMOKE_SENSOR] = client_attributes_smoke_sensor
    if client_attributes_move_sensor:
        list_client_attributes[DEVICE_MOVE_SENSOR] = client_attributes_move_sensor
    if client_attributes_flood_sensor:
        list_client_attributes[DEVICE_FLOOD_SENSOR] = client_attributes_flood_sensor

    return list_client_attributes
