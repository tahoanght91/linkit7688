import time

from config import *
from config.common_led import *


def call():
    period = 2
    while True:
        dct_led_value = get_led_value()
        if len(dct_led_value) > 0:
            for key, value in dct_led_value.items():
                compose_led_command(key, value)
        time.sleep(period)


def get_led_value():
    print('telemetry')
    print(telemetries)
    dct_led = {}
    try:
        dct_led[LED_SERVER] = 0  # TODO: need function check
        dct_led[LED_ATS] = 0  # TODO: check key
        dct_led[LED_DC] = client_attributes['mccDcCabinetSate']
        dct_led[LED_ACM] = client_attributes['acmIState']
        dct_led[LED_ATU] = 0
        dct_led[LED_1] = 0
        dct_led[LED_2] = 0
        dct_led[LED_NONE] = 0
        dct_led[LED_ALARM] = telemetries['mccSmokeState']   # TODO: need function check
        dct_led[LED_3G] = 0  # TODO: need function check
        dct_led[LED_ETHERNET] = 0   # TODO: need function check
        dct_led[LED_CRMU] = client_attributes['mccRfidConnectState']
        dct_led[LED_4] = 0
    except Exception as ex:
        LOGGER.error('Error at get_led_value function with message: %s', ex.message)
    return dct_led


def compose_led_command(key, value):
    try:
        led_id = key
        led_color = validate_value(value)
        commands_lock.acquire()
        commands[led_id] = led_color
        commands_lock.release()
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
