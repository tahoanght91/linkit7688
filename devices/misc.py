from config import BYTE_ORDER
from utility import bytes_to_int
from .utils import _read_attribute, _read_telemetry

def extract(byte_data):
    fireState = bytes_to_int(byte_data[0])
    offOnFire = bytes_to_int(byte_data[1])
    smokeState = bytes_to_int(byte_data[2])
    floodState = bytes_to_int(byte_data[3])
    moveSensor = bytes_to_int(byte_data[4])
    din5 = bytes_to_int(byte_data[5])
    din6 = bytes_to_int(byte_data[6])
    din7 = bytes_to_int(byte_data[7])
    temp = bytes_to_int(byte_data[8:10], BYTE_ORDER)
    humid = bytes_to_int(byte_data[10:12], BYTE_ORDER)
    bell_state = bytes_to_int(byte_data[12])
    fan_state = bytes_to_int(byte_data[13])
    v12 = bytes_to_int(byte_data[14])
    vbus = bytes_to_int(byte_data[15])

    _read_attribute('fireState', fireState)
    _read_attribute('offOnFire', offOnFire)
    _read_attribute('smokeState', smokeState)
    _read_attribute('floodState', floodState)
    _read_attribute('moveSensor', moveSensor)
    _read_attribute('miscDin5', din5)
    _read_attribute('miscDin6', din6)
    _read_attribute('miscDin7', din7)
    _read_telemetry('miscTemp', temp)
    _read_telemetry('miscHumid', humid)
    _read_attribute('miscBellState', bell_state)
    _read_attribute('miscFanState', fan_state)
    _read_attribute('miscV12', v12)
    _read_attribute('miscVbus', vbus)