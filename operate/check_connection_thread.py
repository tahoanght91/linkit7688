import json
import os
import socket
import subprocess
import time

import requests

from config import LOGGER, CLIENT_ID, CLIENT
from config.common_api import *

COMMAND_RESET_SERVICE_7688 = 'reboot'
url_check_connection = PREFIX + DOMAIN + API_CHECK_CONNECTION
params = {'gatewayId': CLIENT_ID}
timeout = 3
host = 'smartsite.mobifone.vn'
port = 443


# def call():
#     period = 120
#     while True:
#         try:
#             time.sleep(period)
#             LOGGER.info('Pinging to Google: %s', subprocess.check_output(['ping', '-c', '4', 'google.com']))
#             response = requests.get(url=url_check_connection, params=params)
#             if response.status_code == 200:
#                 LOGGER.info('Send check connection request to Smartsite successful!')
#                 active = json.loads(response.content)['result']
#                 if active:
#                     LOGGER.info('Gateway is online!')
#                 else:
#                     LOGGER.info('Gateway is offline!')
#                     CLIENT.disconnect()
#             else:
#                 LOGGER.info('Response from Smartsite is not 200')
#                 CLIENT.disconnect()
#         except Exception as ex:
#             LOGGER.info('Error when check connection with message: %s', ex.message)
#             CLIENT.disconnect()


def call():
    period = 10
    while True:
        try:
            time.sleep(period)
            LOGGER.info('Pinging to Google: %s', subprocess.check_output(['ping', '-c', '4', 'google.com']))
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            LOGGER.info('Gateway is online !!!')
        except Exception as ex:
            LOGGER.debug('Gateway is offline !!!')
            LOGGER.error('Error when check connection with message: %s', ex.message)
            CLIENT.disconnect()
