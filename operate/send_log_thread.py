import glob
import os
import shutil
import time
from datetime import datetime

import requests

from config import LOGGER, device_config
from config.common_api import API_SEND_LOG, PREFIX, DOMAIN
from control.utils import read_to_json

MIN_SIZE_FILE = 1468006.4
MAX_SIZE_FILE = 1572864
TIME_PERIOD = 30
LOG_PATH = './app.log.1'
DESTINATION = './log'
LAST_UPDATE_LOG_PATH = './last_update_log.json'
url_send_log = PREFIX + DOMAIN + API_SEND_LOG


def call():
    period = TIME_PERIOD
    while True:
        existence = check_log_exist(LAST_UPDATE_LOG_PATH, LOG_PATH)
        if existence:
            detected = detect_new_log(LAST_UPDATE_LOG_PATH, LOG_PATH)
            if detected:
                copied = copy_log(LOG_PATH)
                if copied[0] and copied[1]:
                    body = write_body_send_log(copied[2])
                    if len(body) > 0:
                        response = send_log_smartsite(body[0], body[-1])
        time.sleep(period)


def check_log_exist(last_update_log_path, path):
    result = False
    try:
        if os.path.exists(path):
            result = True
    except Exception as ex:
        LOGGER.warning('Error at check_log_exist function with message: %s', ex.message)
    return result


def detect_new_log(last_update_log_path, log_path):
    result = False
    try:
        last_update_file = read_to_json(last_update_log_path)
        last_updated_date = last_update_file['updateDate']
        updated_date = os.path.getmtime(log_path)
        if updated_date > last_updated_date:
            result = True
    except Exception as ex:
        LOGGER.warning('Error at detect_new_log function with message: %s', ex.message)
    return result


def copy_log(source):
    copied = False
    renamed = False
    destination = ''
    try:
        now = datetime.now()
        new_name = now.strftime('%d-%m-%Y-%H-%M-%S') + '.txt'
        if os.path.exists(source):
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
    files = {}
    data = {}
    try:
        gateway_id = device_config['device_id']
        data = {'idTram': gateway_id}
        files = {"file": open(path_file, 'rb')}
        LOGGER.info('Params send log to Smartsite: %s', files)
    except Exception as ex:
        LOGGER.warning('Error at write_body_send_log function with message: %s', ex.message)
    return data, files


def send_log_smartsite(data, files):
    result = False
    try:
        if isinstance(data, dict) and isinstance(files, dict):
            if len(data) > 0 and len(files) > 0:
                response = requests.post(url_send_log, data=data, files=files)
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

