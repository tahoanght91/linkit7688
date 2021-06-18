import time

from config import *
from config.common_led import *


dct_last_trace_led_alarm = {}


def call():
    period = 20
    while True:
        dct_led_value = get_led_value()
        if len(dct_led_value) > 0:
            for key, value in dct_led_value.items():
                compose_led_command(key, value)
        time.sleep(period)


def get_led_value():
    dct_led = {}
    try:
        dct_led[LED_SERVER] = get_state_led_server()
        dct_led[LED_ATS] = client_attributes['atsErrorState']
        dct_led[LED_DC] = client_attributes['mccDcCabinetSate']
        dct_led[LED_ACM] = client_attributes['acmIState']
        dct_led[LED_ATU] = 1
        dct_led[LED_1] = 1
        dct_led[LED_2] = 1
        dct_led[LED_NONE] = 1
        dct_led[LED_ALARM] = get_sate_led_alarm(telemetries, dct_last_trace_led_alarm)   # TODO: need function check
        dct_led[LED_3G] = 1  # TODO: need function check
        dct_led[LED_ETHERNET] = 0   # TODO: need function check
        dct_led[LED_CRMU] = client_attributes['mccRfidConnectState']
        dct_led[LED_4] = 1
    except Exception as ex:
        LOGGER.error('Error at get_led_value function with message: %s', ex.message)
    return dct_led


def compose_led_command(key, value):
    try:
        led_id = key
        led_color = validate_value(value)
        cmd_led_lock.acquire()
        cmd_led[led_id] = led_color
        cmd_led_lock.release()
    except Exception as ex:
        LOGGER.error('Error at compose_led_command with message: %s', ex.message)


def validate_value(value):
    result = RED
    try:
        if value == 0:
            result = GREEN
        return result
    except Exception as ex:
        LOGGER.error('Error at validate_value function with message: %s', ex.message)
    return result


def set_last_trace_led_alarm(key, value):
    dct_last_trace_led_alarm[key] = value


def get_sate_led_alarm(dct_telemetry, dct_last_trace):
    result = -1
    try:
        if len(dct_telemetry) == 0:
            if len(dct_last_trace) == 0:
                result = client_attributes.get('mccSmokeState', default_data.mccSmokeState)
            else:
                result = dct_last_trace['mccSmokeState']
        elif len(dct_telemetry) > 0:
            if 'mccSmokeState' in dct_telemetry:
                result = dct_telemetry['mccSmokeState']
            else:
                result = dct_last_trace['mccSmokeState']
        set_last_trace_led_alarm('mccSmokeState', result)
    except Exception as ex:
        LOGGER.error('Error at get_sate_led_alarm function with message: %s', ex.message)
    return result


def get_state_led_server():
    try:
        if CLIENT.is_connected():
            return 0
        else:
            return 1
    except Exception as ex:
        LOGGER.error('Error at get_state_led_server function with message: %s', ex.message)
