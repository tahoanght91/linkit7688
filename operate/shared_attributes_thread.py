import time

from config import LOGGER, shared_attributes, default_data, CLIENT, commands_lock, commands


def call():
    period = shared_attributes.get('mccPeriodSendShared', default_data.mccPeriodSendShared)
    while True:
        if CLIENT.is_connected():
            for key, value in shared_attributes.items():
                commands_lock.acquire()
                commands[key] = value
                commands_lock.release()
                LOGGER.debug('Process command send shared attributes to stm32: device name: %s, value: %s', key, value)
        time.sleep(period)

