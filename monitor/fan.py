from config import *
from config.common import *


def _send_command(command):
    if command == 'on' and client_attributes.get('miscFanState', default_data.miscFanState) == 0:
        commands_lock.acquire()
        commands[DEVICE_MISC] = 'on'
        commands_lock.release()
        return 'on'
    elif command == 'off' and client_attributes.get('miscFanState', default_data.miscFanState) == 1:
        commands_lock.acquire()
        commands[DEVICE_MISC] = 'off'
        commands_lock.release()
        return 'off'
    return ''


def apply():
    if client_attributes.get('mccSmokeState', default_data.mccFireState) == 1 or client_attributes.get('mccFireState', default_data.mccFireState) == 1:
        LOGGER.debug('Smoke or fire detected, turn off fan')
        return _send_command('off')
    elif client_attributes.get('aircAirc1RunState', default_data.aircAirc1RunState) == 1 or client_attributes.get('aircAirc2RunState', default_data.aircAirc2RunState == 1):
        LOGGER.debug('AIRC running, turn off fan')
        return _send_command('off')
    elif telemetries.get('miscTemp', default_data.miscTemp) < shared_attributes.get('miscMinTemp', default_data.miscMinTemp):
        LOGGER.debug('Temperature too low, turn off fan')
        return _send_command('off')
    else:
        LOGGER.debug('Appropriate temperature, no smoke and fire, AIRC not running, turn on fan')
        return _send_command('on')
