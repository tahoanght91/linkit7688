from config import *
from config.common import *


def _send_command(command):
    if command == 'on' and not client_attributes.get('crmuDoorState', default_data.crmuDoorState):
        commands_lock.acquire()
        commands[DEVICE_CRMU] = 'on'
        commands_lock.release()
        return 'on'
    elif command == 'off' and client_attributes.get('crmuDoorState', default_data.crmuDoorState):
        commands_lock.acquire()
        commands[DEVICE_CRMU] = 'off'
        commands_lock.release()
        return 'off'
    return ''


def check_status():
    if (client_attributes.get('mccSmokeState', default_data.mccSmokeState) == 1
            or client_attributes.get('mccFireState', default_data.mccFireState) == 1
            or client_attributes.get('mccFloodState', default_data.mccFloodState) == 1):
        LOGGER.debug('Smoke or fire or flood detected, turn off the CRMU')
        return _send_command('off')
    else:
        LOGGER.debug('No smoke and fire and flood, CRMU operate normally')
        return _send_command('on')
