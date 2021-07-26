import glob
import os
import shutil
import time
from datetime import datetime

import requests

from config import LOGGER, device_config
from config.common_api import API_SEND_LOG, PREFIX, DOMAIN

MIN_SIZE_FILE = 1468006.4
MAX_SIZE_FILE = 1572864
TIME_PERIOD = 30
LOG_PATH = './app.log.1'
DESTINATION = './log'
URL_SEND_LOG = PREFIX + DOMAIN + API_SEND_LOG


def call():
    period = TIME_PERIOD
    while True:
        resp_get_size = get_size_log(LOG_PATH)
        resp_copy_log = copy_log(resp_get_size[0], resp_get_size[2])
        if resp_copy_log[0] and resp_copy_log[1]:
            resp_write_body = write_body_send_log(resp_copy_log[2])
            if len(resp_write_body[0]) > 0 and len(resp_write_body[1]) > 0:
                resp_send_log = send_log_smartsite(resp_write_body[0], resp_write_body[1])
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
    copied = False
    renamed = False
    destination = ''
    try:
        now = datetime.now()
        new_name = now.strftime('%d-%m-%Y-%H-%M-%S') + '.txt'
        if result and os.path.exists(source):
            shutil.copy(source, DESTINATION)
            copied = True
            LOGGER.debug('Copy log successful!')
        if copied:
            files = glob.glob(DESTINATION + '/*.log.1')
            old_file = os.path.join(DESTINATION + '/' + os.path.basename(files[0]))
            destination = os.path.join(DESTINATION + '/' + new_name)
            os.rename(old_file, destination)
            renamed = True
        else:
            LOGGER.debug('Fail while copy log to log folder')
    except Exception as ex:
        LOGGER.warning('Error at copy_log function with message: %s', ex.message)
    return copied, renamed, destination


def write_body_send_log(path_file):
    params = {}
    files = {}
    try:
        gateway_id = device_config['device_id']
        files = {"uploadFile": open(path_file, 'rb')}
        params = {"gatewayId": gateway_id}
        LOGGER.info('Body send log to Smartsite: %s', params)
    except Exception as ex:
        LOGGER.warning('Error at write_body_send_log function with message: %s', ex.message)
    return params, files


def send_log_smartsite(params, files):
    result = False
    try:
        if isinstance(params, dict) and isinstance(files, dict):
            if len(params) > 0 and len(files) > 0:
                response = requests.post(URL_SEND_LOG, params=params, files=files)
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

