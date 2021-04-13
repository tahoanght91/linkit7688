import time

from config import *
import mqtt


# def call():
#     period = shared_attributes.get('periodUpdate', default_data.periodUpdate)
#     while True:
#         if CLIENT.is_connected():
#             update_attributes_lock.acquire()
#             if update_attributes:
#                 CLIENT.send_attributes(update_attributes)
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
            client_attr_temp1 = format_telemetry()
            client_attr_temp2 = client_attr_temp1

            client_attr = {**client_attr_temp1, **client_attr_temp2}
            if client_attr:
                CLIENT.send_attributes(client_attr)
                LOGGER.info('Sent changed client attributes')
                log_info = []
                for key, value in update_attributes.items():
                    log_info.append('\t{:>20s}: {:>20s}'.format(str(key), str(value)))
                LOGGER.info('\n'.join(log_info))
                update_attributes.clear()
            update_attributes_lock.release()
        time.sleep(period)

def format_telemetry():
    transform_telemetry = {
        "miscDin0": update_attributes['miscDin0'] if 'miscDin0' in update_attributes else 0,
        "miscDin1": update_attributes['miscDin1'] if 'miscDin1' in update_attributes else 0,
        "miscDin2": update_attributes['miscDin2'] if 'miscDin2' in update_attributes else 0,
        "miscDin3": update_attributes['miscDin3'] if 'miscDin3' in update_attributes else 0,
        "miscDin4": update_attributes['miscDin4'] if 'miscDin4' in update_attributes else 0,
        "miscDin5": update_attributes['miscDin5'] if 'miscDin5' in update_attributes else 0,
        "miscDin6": update_attributes['miscDin6'] if 'miscDin6' in update_attributes else 0,
        "miscDin7": update_attributes['miscDin7'] if 'miscDin7' in update_attributes else 0,
        "miscFanState": update_attributes['miscFanState'] if 'miscFanState' in update_attributes else 0,
        "miscBellState": update_attributes['miscBellState'] if 'miscBellState' in update_attributes else 0,
        "miscV12": update_attributes['miscV12'] if 'miscV12' in update_attributes else 0,
        "miscVbus": update_attributes['miscVbus'] if 'miscVbus' in update_attributes else 0,
        "aircOnlineStatus": update_attributes['aircOnlineStatus'] if 'aircOnlineStatus' in update_attributes else 0,
        "aircAirc1RunState": update_attributes['aircAirc1RunState'] if 'aircAirc1RunState' in update_attributes else 0,
        "aircAirc1Error": update_attributes['aircAirc1Error'] if 'aircAirc1Error' in update_attributes else 0,
        "aircAirc2RunState": update_attributes['aircAirc2RunState'] if 'aircAirc2RunState' in update_attributes else 0,
        "aircAirc2Error": update_attributes['aircAirc2Error'] if 'aircAirc2Error' in update_attributes else 0,
        "aircAirc1RunThreshold": update_attributes['aircAirc1RunThreshold'] if 'aircAirc1RunThreshold' in update_attributes else 0,
        "aircAirc2RunThreshold": update_attributes['aircAirc2RunThreshold'] if 'aircAirc2RunThreshold' in update_attributes else 0,
        "aircAirc1Command": update_attributes['aircAirc1Command'] if 'aircAirc1Command' in update_attributes else 0,
        "aircAirc2Command": update_attributes['aircAirc2Command'] if 'aircAirc2Command' in update_attributes else 0,
        "aircIrStatus": update_attributes['aircIrStatus'] if 'aircIrStatus' in update_attributes else 0,
        "aircLearnCmdId": update_attributes['aircLearnCmdId'] if 'aircLearnCmdId' in update_attributes else 0,
        "atsOnlineStatus": update_attributes['atsOnlineStatus'] if 'atsOnlineStatus' in update_attributes else 0,
        "atsCommState": update_attributes['atsCommState'] if 'atsCommState' in update_attributes else 0,
        "atsMode": update_attributes['atsMode'] if 'atsMode' in update_attributes else 0,
        "atsType": update_attributes['atsType'] if 'atsType' in update_attributes else 0,
        "atsContactorState": update_attributes['atsContactorState'] if 'atsContactorState' in update_attributes else 0,
        "atsBatFull": update_attributes['atsBatFull'] if 'atsBatFull' in update_attributes else 0,
        "atsIsAllBatFull": update_attributes['atsIsAllBatFull'] if 'atsIsAllBatFull' in update_attributes else 0,
        "atsGscType": update_attributes['atsGscType'] if 'atsGscType' in update_attributes else 0,
        "atsGscPwrCounter": update_attributes['atsGscPwrCounter'] if 'atsGscPwrCounter' in update_attributes else 0,
        "atuOnlineStatus": update_attributes['atuOnlineStatus'] if 'atuOnlineStatus' in update_attributes else 0,
        "crmuOnlineStatus": update_attributes['crmuOnlineStatus'] if 'crmuOnlineStatus' in update_attributes else 0,
        "crmuCardId": update_attributes['crmuCardId'] if 'crmuCardId' in update_attributes else 0,
        "crmuDoorState": update_attributes['crmuDoorState'] if 'crmuDoorState' in update_attributes else 0,
        "dcOnlineStatus": update_attributes['dcOnlineStatus'] if 'dcOnlineStatus' in update_attributes else 0,
        "dcRectState": update_attributes['dcRectState'] if 'dcRectState' in update_attributes else 0,
        "fireState": update_attributes['fireState'] if 'fireState' in update_attributes else 0,
        "offOnFire": update_attributes['offOnFire'] if 'offOnFire' in update_attributes else 0,
        "smokeState": update_attributes['smokeState'] if 'smokeState' in update_attributes else 0,
        "floodState": update_attributes['floodState'] if 'floodState' in update_attributes else 0,
        "moveSensor": update_attributes['moveSensor'] if 'moveSensor' in update_attributes else 0,
    }
    return transform_telemetry
