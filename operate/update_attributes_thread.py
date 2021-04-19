import time

from config import *


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
        "aircAirc2RunState": 0,
        "aircAirc1RunState": 0,
        "aircOnlineStatus": 1,
        "aircAirc1Command": 1,
        "aircAirc1RunThreshold": 26,
        "aircLearnCmdId": 0,
        "aircAirc2Command": 1,
        "aircAirc1Error": 0,
        "aircAirc2RunThreshold": 26,
        "aircAirc2Error": 0,
        "aircIrStatus": 1,
        "atsBatFull": 1,
        "atsGscType": 1,
        "atsIsAllBatFull": 0,
        "atsGscPwrCounter": 1,
        "atsGscAlarm": 0,
        "atsMode": 0,
        "atsContactorState": 1,
        "atsCommState": 1,
        "atsOnlineStatus": 1,
        "atsType": 1,
        "atuOnlineStatus": 1,
        "crmuCardId": "AAA",
        "crmuOnlineStatus": 1,
        "crmuDoorState": 1,
        "miscBellState": 0,
        "miscFanState": 0,
        "miscVbus": 1,
        "miscV12": 1,
        "miscDin3": 0,
        "miscDin2": 0,
        "miscDin1": 0,
        "miscDin0": 0,
        "miscDin7": 0,
        "miscDin6": 0,
        "miscDin5": 0,
        "miscDin4": 0,
        "dcOnlineStatus": 22,
        "dcRectState": 111,
        "moveSensor": 1,
        "smokeState": 1,
        "fireState": 1,
        "offOnFire": 1,
        "floodState": 1
    }

    return attributes


def format_client_attributes():
    list_client_attributes = {'device_misc': {}, 'device_airc': {}, 'device_ats': {}, 'device_atu': {},
                              'device_dc': {}, 'device_crmu': {}, 'device_fire_sensor': {}, 'device_smoke_sensor': {},
                              'device_move_sensor': {}, 'device_flood_sensor': {}}
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
        elif 'atu' in key:
            client_attributes_atu[key] = value
        elif 'dc' in key:
            client_attributes_dc[key] = value
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
        list_client_attributes['device_misc'] = client_attributes_misc
    if client_attributes_airc:
        list_client_attributes['device_airc'] = client_attributes_airc
    if client_attributes_ats:
        list_client_attributes['device_ats'] = client_attributes_ats
    if client_attributes_atu:
        list_client_attributes['device_atu'] = client_attributes_atu
    if client_attributes_dc:
        list_client_attributes['device_dc'] = client_attributes_dc
    if client_attributes_crmu:
        list_client_attributes['device_crmu'] = client_attributes_crmu
    if client_attributes_fire_sensor:
        list_client_attributes['device_fire_sensor'] = client_attributes_fire_sensor
    if client_attributes_smoke_sensor:
        list_client_attributes['device_smoke_sensor'] = client_attributes_smoke_sensor
    if client_attributes_move_sensor:
        list_client_attributes['device_move_sensor'] = client_attributes_move_sensor
    if client_attributes_flood_sensor:
        list_client_attributes['device_flood_sensor'] = client_attributes_flood_sensor

    return list_client_attributes
