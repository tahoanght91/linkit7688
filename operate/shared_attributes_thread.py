import struct
import time

from operator import itemgetter
from config import LOGGER, shared_attributes, default_data, CLIENT, commands_lock, commands


# def call():
#     period = shared_attributes.get('mccPeriodUpdate', default_data.mccPeriodUpdate)
#     while True:
#         if CLIENT.is_connected():
#             for key, value in shared_attributes.items():
#                 commands_lock.acquire()
#                 commands[key] = value
#                 commands_lock.release()
#                 LOGGER.debug('Process command send shared attributes to stm32: device name: %s, value: %s', key, value)
#         time.sleep(period)


list_dict_ats = []
list_dict_acm = []
list_dict_mcc = []


def call():
    try:
        period = shared_attributes.get('mccPeriodUpdate', default_data.mccPeriodUpdate)
        while True:
            if CLIENT.is_connected():
                for key, value in shared_attributes.items():
                    response_classify_sa = classify_shared_attributes(key, value)
                    if response_classify_sa is not None:
                        classify_dict(response_classify_sa)
                        LOGGER.info('Successful list classification')
                    else:
                        LOGGER.info('Failed list classification')
                response_sorted = sort_list_dict(list_dict_mcc, list_dict_acm, list_dict_ats)
                if len(response_sorted) > 0:
                    LOGGER.info('Sort the list successful')
                    array_value = get_array_value(response_sorted)
                    if len(array_value) > 0:
                        LOGGER.info('Get value of array successful')
                        commands_lock.acquire()
                        commands['allSharedAttributes'] = array_value
                        commands_lock.release()
                        response_clear_list = clear_all_list(list_dict_mcc, list_dict_acm, list_dict_ats)
                        if response_clear_list:
                            LOGGER.info('Clear all array successful')
                        else:
                            LOGGER.info('Clear all array failed')
                    else:
                        LOGGER.info('Get value of array failed')
                else:
                    LOGGER.info('Sort the list failed')
            time.sleep(period)
    except Exception as ex:
        LOGGER.error('Error at call function in thread shared_attributes_thread with message: %s', ex.message)


def classify_shared_attributes(key, value):
    number = 0
    formatted = {}
    try:
        if 'ats' in key:
            number = parse_ats_shared_attributes_to_number(key)
            formatted = {'type': 'ats', 'idSharedAttributes': number, 'value': value}
        elif 'mcc' in key:
            number = parse_mcc_shared_attributes_to_number(key)
            formatted = {'type': 'mcc', 'idSharedAttributes': number, 'value': value}
        elif 'acm' in key:
            number = parse_acm_shared_attributes_to_number(key)
            formatted = {'type': 'acm', 'idSharedAttributes': number, 'value': value}
    except Exception as ex:
        LOGGER.error('Error at classify_shared_attributes function with message: %s', ex.message)
    return formatted


def parse_ats_shared_attributes_to_number(key):
    switcher_ats = {
        'atsVacMaxThreshold': 1,
        'atsVdcThreshold': 2,
        'atsVacMinThreshold': 3,
        'atsVgenMaxThreshold': 4,
        'atsVgenMinThreshold': 5,
        'atsVacStabilizeTimeout': 6,
        'atsVgenIdleCoolingTimeout': 7,
        'atsVgenIdleWarmUpTimeout': 8,
        'atsGenInactiveStartTime': 9,
        'atsGenInactiveEndTime': 10,
        'atsGenActiveDuration': 11
    }
    return switcher_ats.get(key, "Out of range!")


def parse_mcc_shared_attributes_to_number(key):
    switcher_mcc = {
        'mccPeriodReadDataIO': 1,
        'mccPeriodSendTelemetry': 2,
        'mccPeriodUpdate': 3,
        'mccDcMinThreshold': 4
    }
    return switcher_mcc.get(key, "Out of range!")


def parse_acm_shared_attributes_to_number(key):
    switcher_acm = {
        'acmAlternativeState': 1,
        'acmAlternativeTime': 2,
        'acmRunTime': 3,
        'acmRestTime': 4,
        'acmGenAllow': 5,
        'acmVacThreshold': 6,
        'acmMinTemp': 7,
        'acmMaxTemp': 8,
        'acmMinHumid': 9,
        'acmMaxHumid': 10,
        'acmExpectedTemp': 11,
        'acmExpectedHumid': 12,
        'acmT1Temp': 13,
        'acmT2Temp': 14,
        'acmT3Temp': 15,
        'acmT4Temp': 16
    }
    return switcher_acm.get(key, "Out of range!")


def sort_list_dict(list_dict_mcc, list_dict_acm, list_dict_ats):
    new_list_mcc = []
    new_list_acm = []
    new_list_ats = []
    try:
        new_list_mcc = sorted(list_dict_mcc, key=itemgetter('idSharedAttributes'))
        new_list_acm = sorted(list_dict_acm, key=itemgetter('idSharedAttributes'))
        new_list_ats = sorted(list_dict_ats, key=itemgetter('idSharedAttributes'))
    except Exception as ex:
        LOGGER.error('Error at sort_list_dict function with message: %s', ex.message)
    return new_list_mcc, new_list_acm, new_list_ats


def classify_dict(response_classify):
    response = False
    try:
        if response_classify['type'] is 'mcc':
            list_dict_mcc.append(response_classify.copy())
            response = True
        elif response_classify['type'] is 'ats':
            list_dict_ats.append(response_classify.copy())
            response = True
        elif response_classify['type'] is 'acm':
            list_dict_acm.append(response_classify.copy())
            response = True
    except Exception as ex:
        LOGGER.error('Error at classify_dict function with message: %s', ex.message)
    return response


def get_array_value(tuple_sorted):
    array_value = []
    try:
        for x in tuple_sorted:
            for y in x:
                array_value.append(y['value'])
    except Exception as ex:
        LOGGER.error('Error at get_array_value function with message: %s', ex.message)
    return array_value


def clear_all_list(list_dict_mcc, list_dict_acm, list_dict_ats):
    flag = False
    try:
        del list_dict_mcc[:]
        del list_dict_acm[:]
        del list_dict_ats[:]
        if len(list_dict_mcc) == 0 and len(list_dict_acm) == 0 and len(list_dict_ats) == 0:
            flag = True
    except Exception as ex:
        LOGGER.error('Error at clear_all_list function with message: %s', ex.message)
    return flag

