from utility import bytes_to_int
from .utils import _read_attribute, _read_telemetry
from config import BYTE_ORDER


def extract(byte_data):
    '''
    Extract the data from an ATU message sent from the IO
    '''
    atu_1x = bytes_to_int(byte_data[0:4], byteorder=BYTE_ORDER)
    atu_1y = bytes_to_int(byte_data[4:8], byteorder=BYTE_ORDER)
    atu_1z = bytes_to_int(byte_data[8:12], byteorder=BYTE_ORDER)
    atu_2x = bytes_to_int(byte_data[12:16], byteorder=BYTE_ORDER)
    atu_2y = bytes_to_int(byte_data[16:20], byteorder=BYTE_ORDER)
    atu_2z = bytes_to_int(byte_data[20:24], byteorder=BYTE_ORDER)
    atu_3x = bytes_to_int(byte_data[24:28], byteorder=BYTE_ORDER)
    atu_3y = bytes_to_int(byte_data[28:32], byteorder=BYTE_ORDER)
    atu_3z = bytes_to_int(byte_data[32:36], byteorder=BYTE_ORDER)
    online_status = bytes_to_int(byte_data[36])

    _read_telemetry('atuAtu1X', atu_1x)
    _read_telemetry('atuAtu1Y', atu_1y)
    _read_telemetry('atuAtu1Z', atu_1z)
    _read_telemetry('atuAtu2X', atu_2x)
    _read_telemetry('atuAtu2Y', atu_2y)
    _read_telemetry('atuAtu2Z', atu_2z)
    _read_telemetry('atuAtu3X', atu_3x)
    _read_telemetry('atuAtu3Y', atu_3y)
    _read_telemetry('atuAtu3Z', atu_3z)

    _read_attribute('atuOnlineStatus', online_status)
