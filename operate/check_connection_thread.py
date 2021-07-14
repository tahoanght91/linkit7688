import subprocess
import time

import requests

from config import *
from config.common_api import *

COMMAND_RESET_SERVICE_7688 = 'reboot'
url_check_connection = PREFIX + DOMAIN + API_CHECK_CONNECTION
params = {'gatewayId': CLIENT_ID}
TEN_SECONDS = 10


def call():
    period = TEN_SECONDS
    while True:
        try:
            time.sleep(period)
            LOGGER.info('Pinging to Google: %s', subprocess.check_output(['ping', '-c', '4', 'google.com']))
            response = requests.get(url=url_check_connection, params=params)
            if response.status_code == 200:
                LOGGER.info('Send check connection request to Smartsite successful!')
                active = json.loads(response.content)['result']
                if active:
                    LOGGER.info('Gateway is online !!!')
                else:
                    LOGGER.info('Gateway is offline !!!')
                    CLIENT.disconnect()
            else:
                LOGGER.info('Response from Smartsite is not 200')
                CLIENT.disconnect()
        except Exception as ex:
            LOGGER.info('Error when check connection with message: %s', ex.message)
            subprocess.Popen(COMMAND_RESET_SERVICE_7688, shell=True, stdout=subprocess.PIPE)
