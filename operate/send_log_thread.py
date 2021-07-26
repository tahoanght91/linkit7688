import os
import shutil
import time
from datetime import datetime

import requests

from config import LOGGER, device_config
from config.common_api import API_SEND_LOG

MIN_SIZE_FILE = 1468006.4
MAX_SIZE_FILE = 1572864
TIME_PERIOD = 30
LOG_PATH = './app.log.1'


def call():
    period = TIME_PERIOD
    while True:

        time.sleep(period)


def get_size_log(path):
    size = -1
    result = False
    try:
        size = os.path.getsize(path)
        if MIN_SIZE_FILE <= size <= MAX_SIZE_FILE:
            result = True
    except Exception as ex:
        LOGGER.warning('Error at get_size_log function with message: %s', ex.message)
    return result, size, path


def copy_log(result, source):
    flag = False
    destination = ''
    try:
        now = datetime.now()
        file_name = now.strftime('%d/%m/%Y-%H:%M:%S') + '.txt'
        destination = './log/' + file_name
        if result and os.path.exists(source) and destination != '':
            shutil.copyfile(source, destination)
            flag = True
    except Exception as ex:
        LOGGER.warning('Error at copy_log function with message: %s', ex.message)
    return flag, destination


def write_body_send_log(flag, path_file):
    body = {}
    try:
        if flag:
            now = time.time()
            gateway_id = device_config['device_id']
            access_token = device_config['access_token']
            body = {"gatewayId": gateway_id, "accessToken": access_token, "uploadFile": open(path_file, 'rb'), "createdDate": now}
            LOGGER.info('Body send log to Smartsite: %s', body)
    except Exception as ex:
        LOGGER.warning('Error at write_body_send_log function with message: %s', ex.message)
    return body


def send_log_smartsite(body):
    result = False
    try:
        if isinstance(body, dict):
            if len(body) > 0:
                response = requests.post(API_SEND_LOG, json=body)
                if response.status_code == 200:
                    result = True
                    LOGGER.info('Send log to Smartsite successful!')
                else:
                    LOGGER.debug('Fail while send log to Smartsite. Status code is: %s', str(response.status_code))
        else:
            LOGGER.debug('Body is not dictionary!')
    except Exception as ex:
        LOGGER.warning('Error at send_log_smartsite function with message: %s', ex.message)
    return result


def delete_log(path_file):
    result = False
    try:
        if os.path.exists(path_file):
            os.remove(path_file)
            result = True
            LOGGER.debug('Remove file log successful!')
    except Exception as ex:
        LOGGER.warning('Error at delete_log function with message: %s', ex.message)
    return result

