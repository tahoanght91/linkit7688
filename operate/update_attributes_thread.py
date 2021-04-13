import time

from config import *
import mqtt


def call():
    period = shared_attributes.get('periodUpdate', default_data.periodUpdate)
    while True:
        if CLIENT.is_connected():
            update_attributes_lock.acquire()
            if update_attributes:
                CLIENT.send_attributes(update_attributes)
                LOGGER.info('Sent changed client attributes')
                log_info = []
                for key, value in update_attributes.items():
                    log_info.append('\t{:>20s}: {:>20s}'.format(str(key), str(value)))
                LOGGER.info('\n'.join(log_info))
                update_attributes.clear()
            update_attributes_lock.release()
        time.sleep(period)
