import time
from config import *


def _send_command(command):
    if command == 'on' and client_attributes.get('miscBellState', default_data.miscBellState) == 0:
        commands_lock.acquire()
        commands['bell'] = 'on'
        commands_lock.release()
        return 'on'
    elif command == 'off' and client_attributes.get('miscBellState', default_data.miscBellState) == 1:
        commands_lock.acquire()
        commands['bell'] = 'off'
        commands_lock.release()
        return 'off'
    return ''


def check_status():
    now = time.localtime()
    if client_attributes.get('mccSmokeState', default_data.mccSmokeState):
        LOGGER.debug('Smoke detected, ring the bell')
    if client_attributes.get('mccFireState', default_data.mccFireState):
        LOGGER.debug('Fire detected, ring the bell')
    if client_attributes.get('mccFloodState', default_data.mccFloodState):
        LOGGER.debug('Flood detected, ring the bell')
    if client_attributes.get('crmuDoorState', default_data.crmuDoorState) and (now.tm_hour > 17 or now.tm_hour < 7):
        LOGGER.debug('Unexpected door opened, ring the bell')
    if client_attributes.get('moveSensor', default_data.moveSensor) and (now.tm_hour > 17 or now.tm_hour < 7):
        LOGGER.debug('Unexpected motion sensed, ring the bell')

    if (client_attributes.get('mccSmokeState', default_data.mccSmokeState)
            or client_attributes.get('mccFireState', default_data.mccFireState)
            or client_attributes.get('mccFloodState', default_data.mccFloodState)
            or client_attributes.get('crmuDoorState', default_data.crmuDoorState)
            and (now.tm_hour > 17 or now.tm_hour < 7)
            or client_attributes.get('moveSensor', default_data.moveSensor)
            and (now.tm_hour > 17 or now.tm_hour < 7)):
        return _send_command('on')
    else:
        return _send_command('off')
