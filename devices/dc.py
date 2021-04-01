from utility import bytes_to_int
from .utils import _read_attribute, _read_telemetry
from config import BYTE_ORDER

def extract(byte_data):
    rect_state = bytes_to_int(byte_data[0])
    vdc = bytes_to_int(byte_data[1:3], byteorder = BYTE_ORDER)
    ibat1 = bytes_to_int(byte_data[3:5], byteorder = BYTE_ORDER)
    bat1_temp = bytes_to_int(byte_data[5:7], byteorder = BYTE_ORDER)
    vbat1_div2 = bytes_to_int(byte_data[7:9], byteorder = BYTE_ORDER)
    ibat2 = bytes_to_int(byte_data[9:11], byteorder = BYTE_ORDER)
    bat2_temp = bytes_to_int(byte_data[11:13], byteorder = BYTE_ORDER)
    vbat2_div2 = bytes_to_int(byte_data[13:15], byteorder = BYTE_ORDER)
    ibat3 = bytes_to_int(byte_data[15:17], byteorder = BYTE_ORDER)
    bat3_temp = bytes_to_int(byte_data[17:19], byteorder = BYTE_ORDER)
    vbat3_div2 = bytes_to_int(byte_data[19:21], byteorder = BYTE_ORDER)
    ibat4 = bytes_to_int(byte_data[21:23], byteorder = BYTE_ORDER)
    bat4_temp = bytes_to_int(byte_data[23:25], byteorder = BYTE_ORDER)
    vbat4_div2 = bytes_to_int(byte_data[25:27], byteorder = BYTE_ORDER)

    online_status = bytes_to_int(byte_data[27])

    _read_attribute('dcRectState', rect_state)
    _read_attribute('dcVdc', vdc)
    _read_telemetry('dcIbat1', ibat1)
    _read_telemetry('dcBat1Temp', bat1_temp)
    _read_telemetry('dcVbat1Div2', vbat1_div2)
    _read_telemetry('dcIbat2', ibat2)
    _read_telemetry('dcBat2Temp', bat2_temp)
    _read_telemetry('dcVbat2Div2', vbat2_div2)
    _read_telemetry('dcIbat3', ibat3)
    _read_telemetry('dcBat3Temp', bat3_temp)
    _read_telemetry('dcVbat3Div2', vbat3_div2)
    _read_telemetry('dcIbat4', ibat4)
    _read_telemetry('dcBat4Temp', bat4_temp)
    _read_telemetry('dcVbat4Div2', vbat4_div2)

    _read_attribute('dcOnlineStatus', online_status)