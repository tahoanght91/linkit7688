import time

from config import *
from config.common import *

CONTINUOUS_RUN = 180 * 60  # time run
period_start = 0


def _send_command(device, command):
    if device == DEVICE_AIRC_1:
        if command == 'on' and client_attributes.get('aircAirc1RunState', default_data.aircAirc1RunState) == 0:
            commands_lock.acquire()
            commands[DEVICE_AIRC_1] = 'on'
            commands_lock.release()
            return DEVICE_AIRC_1 + ': on'
        elif command == 'off' and client_attributes.get('aircAirc1RunState', default_data.aircAirc1RunState) == 1:
            commands_lock.acquire()
            commands[DEVICE_AIRC_1] = 'off'
            commands_lock.release()
            return DEVICE_AIRC_1 + ': off'
    elif device == DEVICE_AIRC_2:
        if command == 'on' and client_attributes.get('aircAirc2RunState', default_data.aircAirc2RunState) == 0:
            commands_lock.acquire()
            commands[DEVICE_AIRC_2] = 'on'
            commands_lock.release()
            return DEVICE_AIRC_2 + ': on'
        elif command == 'off' and client_attributes.get('aircAirc2RunState', default_data.aircAirc2RunState) == 1:
            commands_lock.acquire()
            commands[DEVICE_AIRC_2] = 'off'
            commands_lock.release()
            return DEVICE_AIRC_2 + ': off'
    return ''


def apply():
    global period_start
    now = time.time()
    if client_attributes.get('smokeState', default_data.smokeState) or client_attributes.get('fireState', default_data.fireState):
        LOGGER.debug('Smoke or fire detected, turn off AIRC')
        period_start = 0
        return _send_command(DEVICE_AIRC_1, 'off') + ', ' + _send_command(DEVICE_AIRC_2, 'off')
    elif telemetries.get('miscTemp', default_data.miscTemp) > shared_attributes.get('miscMaxTemp', default_data.miscMaxTemp):
        LOGGER.debug('Temperature too high, turn on AIRC')
        period_start = 0
        return _send_command(DEVICE_AIRC_1, 'on') + ', ' + _send_command(DEVICE_AIRC_2, 'on')
    elif (telemetries.get('miscTemp', default_data.miscTemp) < shared_attributes.get('miscExpectedTemp', default_data.miscExpectedTemp)
          and telemetries.get('miscHumid', default_data.miscHumid) < shared_attributes.get('miscMaxHumid', default_data.miscMaxHumid)):
        LOGGER.debug('Temperature lower than expected and humidity lower than acceptable, turn off AIRC')
        period_start = 0
        return _send_command(DEVICE_AIRC_1, 'off') + ', ' + _send_command(DEVICE_AIRC_2, 'off')
    else:
        LOGGER.debug('Temperature not too high or lower than expected with high humidity, no smoke and fire, run AIRC in alternate mode')
        if now - period_start > CONTINUOUS_RUN:
            period_start = now
            if client_attributes.get('aircAirc1RunState', default_data.aircAirc1RunState) == 0:
                return _send_command(DEVICE_AIRC_1, 'on') + ', ' + _send_command(DEVICE_AIRC_2, 'off')
            else:
                return _send_command(DEVICE_AIRC_1, 'off') + ', ' + _send_command(DEVICE_AIRC_2, 'on')
