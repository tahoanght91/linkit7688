import time
from config import *
from config.common import *

door_opened_time = 0


# Method for other thread to open door (and then automatically close after delay)
def open_door_with_auto_close():
    global door_opened_time
    door_opened_time = time.time()
    return _send_command(COMMAND_MCC_OPEN_DOOR) + ' | '


def _send_command(command):
    commands_lock.acquire()
    commands[DEVICE_MCC_1] = command
    commands_lock.release()
    return DEVICE_MCC_1 + ':' + command


'''
Auto procedure to control:
- Open Door & Ring Bell in emergency & security breach
- Bell will be off when everything is normal
- Close the door when everything is normal and only after pressing Door button or RFID card for a timeout
'''


def check_status():
    print('shared_attributes')
    print(shared_attributes)
    LOGGER.info('Enter monitor:mcc:check_status')
    global door_opened_time

    timestamp = time.time()
    door_opening_elapsed = timestamp - door_opened_time

    now = time.localtime()

    mccDcMinThreshold = shared_attributes('mccDcMinThreshold', default_data.mccDcMinThreshold)
    mccDoorOpenTime = shared_attributes('mccDoorOpenTime', default_data.mccDoorOpenTime)

    mccSmokeState = client_attributes('mccSmokeState', default_data.mccSmokeState)
    mccFireState = client_attributes('mccFireState', default_data.mccFireState)
    mccMoveState = client_attributes('mccMoveState', default_data.mccMoveState)
    mccDoorState = client_attributes('mccDoorState', default_data.mccDoorState)
    mccFloodState = client_attributes('mccFloodState', default_data.mccFloodState)
    mccDoorButton = client_attributes('mccDoorButton', default_data.mccDoorButton)
    Reserved = client_attributes('Reserved', default_data.Reserved)
    Reserved = client_attributes('Reserved', default_data.Reserved)
    mccBellState = client_attributes('mccBellState', default_data.mccBellState)
    mccDeviceTemp = client_attributes('mccDeviceTemp', default_data.mccDeviceTemp)
    mccRackTemp = client_attributes('mccRackTemp', default_data.mccRackTemp)
    mccDcBat1Temp = client_attributes('mccDcBat1Temp', default_data.mccDcBat1Temp)
    mccDcBat2Temp = client_attributes('mccDcBat2Temp', default_data.mccDcBat2Temp)
    mccDcBat3Temp = client_attributes('mccDcBat3Temp', default_data.mccDcBat3Temp)
    mccDcAccuState = client_attributes('mccDcAccuState', default_data.mccDcAccuState)
    mccDcV1 = client_attributes('mccDcV1', default_data.mccDcV1)
    mccDcI1 = client_attributes('mccDcI1', default_data.mccDcI1)
    mccDcP1 = client_attributes('mccDcP1', default_data.mccDcP1)
    mccDcV2 = client_attributes('mccDcV2', default_data.mccDcV2)
    mccDcI2 = client_attributes('mccDcI2', default_data.mccDcI2)
    mccDcP2 = client_attributes('mccDcP2', default_data.mccDcP2)
    mccDcV3 = client_attributes('mccDcV3', default_data.mccDcV3)
    mccDcI3 = client_attributes('mccDcI3', default_data.mccDcI3)
    mccDcP3 = client_attributes('mccDcP3', default_data.mccDcP3)
    mccDcV4 = client_attributes('mccDcV4', default_data.mccDcV4)
    mccDcI4 = client_attributes('mccDcI4', default_data.mccDcI4)
    mccDcP4 = client_attributes('mccDcP4', default_data.mccDcP4)
    mccDcV5 = client_attributes('mccDcV5', default_data.mccDcV5)
    mccDcI5 = client_attributes('mccDcI5', default_data.mccDcI5)
    mccDcP5 = client_attributes('mccDcP5', default_data.mccDcP5)
    mccSystemClock = client_attributes('mccSystemClock', default_data.mccSystemClock)
    mccRfidConnectState = client_attributes('mccRfidConnectState', default_data.mccRfidConnectState)
    mccDcCabinetSate = client_attributes('mccDcCabinetSate', default_data.mccDcCabinetSate)

    # Whether we want the door to be opened or not
    door_to_open = mccDoorButton == 1   # Open door when button pressed
    bell_to_ring = False

    if mccSmokeState == 1:
        LOGGER.debug('Smoke detected, ring the bell')
        door_to_open = True
        bell_to_ring = True
    if mccFireState == 1:
        LOGGER.debug('Fire detected, ring the bell')
        door_to_open = True
        bell_to_ring = True
    if mccFloodState == 1:
        LOGGER.debug('Flood detected, ring the bell')
        door_to_open = True
        bell_to_ring = True
    if mccDoorState == 1 and (now.tm_hour > 17 or now.tm_hour < 7):
        LOGGER.debug('Door opened outside working time (7am-5pm), ring the bell')
        bell_to_ring = True
    if mccMoveState == 1 and (now.tm_hour > 17 or now.tm_hour < 7):
        LOGGER.debug('Unexpected motion sensed outside working time (7am-5pm), ring the bell')
        bell_to_ring = True

    rtn = ''
    if door_to_open and mccDoorState == 0:
        rtn += open_door_with_auto_close()

    # Close door after timeout time (started by Door button or RFID card)
    if not door_to_open and mccDoorState == 1 \
            and door_opening_elapsed > mccDoorOpenTime:
        rtn += _send_command(COMMAND_MCC_CLOSE_DOOR) + ' | '
        door_opened_time = 0    # Reset door timer

    if bell_to_ring and mccBellState == 0:
        rtn += _send_command(COMMAND_MCC_ON_BELL) + ' | '
    if not bell_to_ring and mccBellState == 1:
        rtn += _send_command(COMMAND_MCC_OFF_BELL) + ' | '

    LOGGER.info('Exit monitor:mcc:check_status - ' + rtn)
    return rtn
