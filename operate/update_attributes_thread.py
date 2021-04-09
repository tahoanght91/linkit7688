import time

from config import *


# def call():
#     period = shared_attributes.get('periodUpdate', default_data.periodUpdate)
#     while True:
#         if CLIENT.is_connected():
#             update_attributes_lock.acquire()
#             update_attributes = fake_client_attributes()
#             if update_attributes:
#                 base = update_attributes.items()
#                 for key, value in base:
#                     CLIENT.gw_send_attributes(key, value)
#                 LOGGER.info('Sent changed client attributes')
#                 log_info = []
#                 for key, value in update_attributes.items():
#                     log_info.append('\t{:>20s}: {:>20s}'.format(str(key), str(value)))
#                 LOGGER.info('\n'.join(log_info))
#                 update_attributes.clear()
#             update_attributes_lock.release()
#         time.sleep(period)


def call():
    period = shared_attributes.get('periodUpdate', default_data.periodUpdate)
    while True:
        if CLIENT.is_connected():
            update_attributes_lock.acquire()
            real_client_attributes = format_client_attributes()
            if real_client_attributes:
                base = real_client_attributes.items()
                for key, value in base:
                    CLIENT.gw_send_attributes(key, value)
                LOGGER.info('Sent changed client attributes')
                log_info = []
                for key, value in update_attributes.items():
                    log_info.append('\t{:>20s}: {:>20s}'.format(str(key), str(value)))
                LOGGER.info('\n'.join(log_info))
                update_attributes.clear()
            update_attributes_lock.release()
        time.sleep(period)


def format_client_attributes():
    transform_client_attributes = {
        "device_misc": {
            "miscDin0": update_attributes['miscDin0'],
            "miscDin1": update_attributes['miscDin1'],
            "miscDin2": update_attributes['miscDin2'],
            "miscDin3": update_attributes['miscDin3'],
            "miscDin4": update_attributes['miscDin4'],
            "miscDin5": update_attributes['miscDin5'],
            "miscDin6": update_attributes['miscDin6'],
            "miscDin7": update_attributes['miscDin7'],
            "miscFanState": update_attributes['miscFanState'],
            "miscBellState": update_attributes['miscBellState'],
            "miscV12": update_attributes['miscV12'],
            "miscVbus": update_attributes['miscVbus']
        },
        "device_airc": {
            "aircOnlineStatus": update_attributes['aircOnlineStatus'],
            "aircAirc1RunState": update_attributes['aircAirc1RunState'],
            "aircAirc1Error": update_attributes['aircAirc1Error'],
            "aircAirc2RunState": update_attributes['aircAirc2RunState'],
            "aircAirc2Error": update_attributes['aircAirc2Error'],
            "aircAirc1RunThreshold": update_attributes['aircAirc1RunThreshold'],
            "aircAirc2RunThreshold": update_attributes['aircAirc2RunThreshold'],
            "aircAirc1Command": update_attributes['aircAirc1Command'],
            "aircAirc2Command": update_attributes['aircAirc2Command'],
            "aircIrStatus": update_attributes['aircIrStatus'],
            "aircLearnCmdId": update_attributes['aircLearnCmdId']
        },
        "device_ats": {
            "atsOnlineStatus": update_attributes['atsOnlineStatus'],
            "atsCommState": update_attributes['atsCommState'],
            "atsMode": update_attributes['atsMode'],
            "atsType": update_attributes['atsType'],
            "atsContactorState": update_attributes['atsContactorState'],
            "atsBatFull": update_attributes['atsBatFull'],
            "atsIsAllBatFull": update_attributes['atsIsAllBatFull'],
            "atsGscType": update_attributes['atsGscType'],
            "atsGscPwrCounter": update_attributes['atsGscPwrCounter'],
            "atsGscAlarm": update_attributes['atsGscAlarm']
        },
        "device_atu": {
            "atuOnlineStatus": update_attributes['atuOnlineStatus']
        },
        "device_dc": {
            "dcOnlineStatus": update_attributes['dcOnlineStatus'],
            "dcRectState": update_attributes['dcRectState']
        },
        "device_crmu": {
            "crmuOnlineStatus": update_attributes['crmuOnlineStatus'],
            "crmuCardId": update_attributes['crmuCardId'],
            "crmuDoorState": update_attributes['crmuDoorState']
        },
        "gateway_python_001": {
            "fireState": update_attributes['fireState'],
            "offOnFire": update_attributes['offOnFire'],
            "smokeState": update_attributes['smokeState'],
            "floodState": update_attributes['floodState'],
            "moveSensor": update_attributes['moveSensor']
        }
    }
    return transform_client_attributes


def fake_client_attributes():
    client_attributes = {
        "device_misc": {
            "miscDin0": 1,
            "miscDin1": 1,
            "miscDin2": 1,
            "miscDin3": 1,
            "miscDin4": 1,
            "miscDin5": 1,
            "miscDin6": 1,
            "miscDin7": 1,
            "miscFanState": 1,
            "miscBellState": 1,
            "miscV12": 1,
            "miscVbus": 1
        },
        "device_airc": {
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
            "aircLearnCmdId": 0
        },
        "device_ats": {
            "atsOnlineStatus": 1,
            "atsCommState": 1,
            "atsMode": 0,
            "atsType": 1,
            "atsContactorState": 1,
            "atsBatFull": 1,
            "atsIsAllBatFull": 0,
            "atsGscType": 1,
            "atsGscPwrCounter": 1,
            "atsGscAlarm": 0
        },
        "device_atu": {
            "atuOnlineStatus": 1
        },
        "device_dc": {
            "dcOnlineStatus": 1,
            "dcRectState": 1
        },
        "device_crmu": {
            "crmuOnlineStatus": 1,
            "crmuCardId": "AAA",
            "crmuDoorState": 1
        },
        "gateway_python_001": {
            "fireState": 0,
            "offOnFire": 0,
            "smokeState": 0,
            "floodState": 0,
            "moveSensor": 0
        }
    }
    return client_attributes