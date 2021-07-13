import json
import subprocess
import time

import requests

from config import *
from config.common_api import *

COMMAND_RESET_SERVICE_7688 = 'reboot'
url_check_connection = PREFIX + DOMAIN + API_CHECK_CONNECTION
params = {'gatewayId': CLIENT_ID}
TEN_MINUTES = 600
TEN_SECONDS = 10


def call():
    period = TEN_SECONDS
    checked = False
    while True:
        try:
            time.sleep(period)
            LOGGER.info('Pinging to Google: %s', subprocess.check_output(['ping', '-c', '4', 'google.com']))
            response = requests.get(url=url_check_connection, params=params)
            if response.status_code == 200:
                LOGGER.info('Send check connection request to Smartsite successful!')
                active = json.loads(response.content)['result']
                if active:
                    checked = True
                    period = TEN_SECONDS
                    LOGGER.info('Gateway is online. Change period time from 600 seconds to 10 seconds')
                else:
                    CLIENT.gw_disconnect_device(DEVICE_MCC)
                    CLIENT.gw_disconnect_device(DEVICE_ATS)
                    CLIENT.gw_disconnect_device(DEVICE_ACM)
                    CLIENT.disconnect()
                    period = TEN_MINUTES
                    LOGGER.info('Gateway is offline. So disconnect all device and client. Change period time from 10 seconds to 600 seconds')
            else:
                CLIENT.gw_disconnect_device(DEVICE_MCC)
                CLIENT.gw_disconnect_device(DEVICE_ATS)
                CLIENT.gw_disconnect_device(DEVICE_ACM)
                CLIENT.disconnect()
                period = TEN_MINUTES
                LOGGER.info('Response from Smartsite is not 200. So disconnect all device and client. Change period time from 10 seconds to 600 seconds')
            if not checked:
                CLIENT.gw_connect_device(DEVICE_MCC, "default")
                CLIENT.gw_connect_device(DEVICE_ATS, "default")
                CLIENT.gw_connect_device(DEVICE_ACM, "default")
                period = TEN_SECONDS
                LOGGER.info('Reconnect all devices to Thingsboard!')
        except Exception as ex:
            LOGGER.info('Error when check connection with message: %s', ex.message)
            subprocess.Popen(COMMAND_RESET_SERVICE_7688, shell=True, stdout=subprocess.PIPE)
