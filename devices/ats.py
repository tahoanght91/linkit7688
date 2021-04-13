from utility import bytes_to_int
from .utils import _read_attribute, _read_telemetry
from config import BYTE_ORDER

# fixed ATS to 90 byte
def extract(byte_data):
    '''
    Extract the data from an ATS message sent from the IO
    '''
    comm_state = bytes_to_int(byte_data[0])
    mode = bytes_to_int(byte_data[1])
    type = bytes_to_int(byte_data[2])
    contactor_state = bytes_to_int(byte_data[3])

    vac_p1 = bytes_to_int(byte_data[4:6], byteorder = BYTE_ORDER)
    vac_p2 = bytes_to_int(byte_data[6:8], byteorder = BYTE_ORDER)
    vac_p3 = bytes_to_int(byte_data[8:10], byteorder = BYTE_ORDER)
    vac_freq = bytes_to_int(byte_data[10:12], byteorder = BYTE_ORDER)
    vgen_p1 = bytes_to_int(byte_data[12:14], byteorder = BYTE_ORDER)
    vgen_p2 = bytes_to_int(byte_data[14:16], byteorder = BYTE_ORDER)
    vgen_p3 = bytes_to_int(byte_data[16:18], byteorder = BYTE_ORDER)
    vgen_freq = bytes_to_int(byte_data[18:20], byteorder = BYTE_ORDER)
    vload_p1 = bytes_to_int(byte_data[20:22], byteorder = BYTE_ORDER)
    vload_p2 = bytes_to_int(byte_data[22:24], byteorder = BYTE_ORDER)
    vload_p3 = bytes_to_int(byte_data[24:26], byteorder = BYTE_ORDER)
    vload_freq = bytes_to_int(byte_data[26:28], byteorder = BYTE_ORDER)
    iload_p1 = bytes_to_int(byte_data[28:30], byteorder = BYTE_ORDER)
    iload_p2 = bytes_to_int(byte_data[30:32], byteorder = BYTE_ORDER)
    iload_p3 = bytes_to_int(byte_data[32:34], byteorder = BYTE_ORDER)

    _read_attribute('atsCommState', comm_state)
    _read_attribute('atsMode', mode)
    _read_attribute('atsType', type)
    _read_attribute('atsContactorState', contactor_state)

    _read_telemetry('atsVacP1', vac_p1)
    _read_telemetry('atsVacP2', vac_p2)
    _read_telemetry('atsVacP3', vac_p3)
    _read_telemetry('atsVacFreq', vac_freq)
    _read_telemetry('atsVgenP1', vgen_p1)
    _read_telemetry('atsVgenP2', vgen_p2)
    _read_telemetry('atsVgenP3', vgen_p3)
    _read_telemetry('atsVgenFreq', vgen_freq)
    _read_telemetry('atsVloadP1', vload_p1)
    _read_telemetry('atsVloadP2', vload_p2)
    _read_telemetry('atsVloadP3', vload_p3)
    _read_telemetry('atsVloadFreq', vload_freq)
    _read_telemetry('atsIloadP1', iload_p1)
    _read_telemetry('atsIloadP2', iload_p2)
    _read_telemetry('atsIloadP3', iload_p3)