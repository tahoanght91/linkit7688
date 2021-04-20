from config import *
from config.common import DEVICE_CRMU


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


def apply():
    if (client_attributes.get('smokeState', default_data.smokeState) == 1
            or client_attributes.get('fireState', default_data.fireState) == 1
            or client_attributes.get('floodState', default_data.floodState) == 1):
        LOGGER.debug('Smoke or fire or flood detected, turn off the CRMU')
        return _send_command('off')
    else:
        LOGGER.debug('No smoke and fire and flood, CRMU operate normally')
        return _send_command('on')
