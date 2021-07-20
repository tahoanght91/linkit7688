import time

from config import shared_attributes, default_data, CLIENT, telemetries, LOGGER
from operate.lcd_thread import write_body_send_shared_attributes, send_shared_attributes

PERIOD_UPDATE_T = 300


def call():
    period = PERIOD_UPDATE_T
    while True:
        try:
            time.sleep(period)
            if CLIENT.is_connected():
                dct_telemetry = get_four_t_telemetry(telemetries)
                dct_shared_attributes = get_four_t_shared_attributes(shared_attributes)
                if len(dct_telemetry) > 0 and len(dct_shared_attributes) > 0:
                    result = compare_dct(dct_telemetry, dct_shared_attributes)
                    if len(result) > 0:
                        for x in result:
                            body = write_body_send_shared_attributes(x[0], x[1])
                            response = send_shared_attributes(body)
                    elif len(result) == 0:
                        LOGGER.info('No change value from T1 -> T4 !!!')
                else:
                    LOGGER.info('T1 -> T4 in Telemetry or shared attributes is empty !!!')
        except Exception as ex:
            LOGGER.error('Error at call function in update_t_acm_thread with message: %s', ex.message)


def get_four_t_telemetry(dct_telemetry):
    dct_four_t_telemetry = {}
    try:
        dct_four_t_telemetry['acmT1Temp'] = dct_telemetry.get('acmT1Temp', default_data.acmT1Temp)
        dct_four_t_telemetry['acmT2Temp'] = dct_telemetry.get('acmT2Temp', default_data.acmT2Temp)
        dct_four_t_telemetry['acmT3Temp'] = dct_telemetry.get('acmT3Temp', default_data.acmT3Temp)
        dct_four_t_telemetry['acmT4Temp'] = dct_telemetry.get('acmT4Temp', default_data.acmT4Temp)
        LOGGER.info('Dictionary telemetry of 4 acmTxTemp: %s', dct_four_t_telemetry)
    except Exception as ex:
        LOGGER.error('Error at get_four_t_telemetry function with message: %s', ex.message)
    return dct_four_t_telemetry


def get_four_t_shared_attributes(dct_shared_attributes):
    dct_four_t_shared_attributes = {}
    try:
        dct_four_t_shared_attributes['acmT1Temp'] = dct_shared_attributes.get('acmT1Temp', default_data.acmT1Temp)
        dct_four_t_shared_attributes['acmT2Temp'] = dct_shared_attributes.get('acmT2Temp', default_data.acmT2Temp)
        dct_four_t_shared_attributes['acmT3Temp'] = dct_shared_attributes.get('acmT3Temp', default_data.acmT3Temp)
        dct_four_t_shared_attributes['acmT4Temp'] = dct_shared_attributes.get('acmT4Temp', default_data.acmT4Temp)
        LOGGER.info('Dictionary shared attributes of 4 acmTxTemp: %s', dct_four_t_shared_attributes)
    except Exception as ex:
        LOGGER.error('Error at get_four_t_telemetry function with message: %s', ex.message)
    return dct_four_t_shared_attributes


def compare_dct(dct_telemetry, dct_shared_attributes):
    dct_diff = {}
    try:
        dct_diff = set(dct_telemetry.items()) - set(dct_shared_attributes.items())
        LOGGER.info('Different values between dictionary: %s', dct_diff)
    except Exception as ex:
        LOGGER.error('Error at compare_dct function with message: %s', ex.message)
    return dct_diff

