import utility
from . import utils
from config import BYTE_ORDER


def extract(byte_data):
    '''
    Extract the data from an AIRC message sent from the IO
    '''

    #telemetry
    temp_indoor = utility.bytes_to_int(byte_data[0:2], byteorder=BYTE_ORDER)
    temp_outdoor = utility.bytes_to_int(byte_data[2:4], byteorder=BYTE_ORDER)
    humid_indoor = utility.bytes_to_int(byte_data[4:6], byteorder=BYTE_ORDER)

    #clien attributes
    airc1_command = utility.bytes_to_int(byte_data[7])
    airc2_command = utility.bytes_to_int(byte_data[8])
    fan_command = utility.bytes_to_int(byte_data[9])
    thr_temp_1 = utility.bytes_to_int(byte_data[10])
    thr_temp_2 = utility.bytes_to_int(byte_data[11])
    thr_temp_3 = utility.bytes_to_int(byte_data[12])
    thr_temp_4 = utility.bytes_to_int(byte_data[13])
    airc_count = utility.bytes_to_int(byte_data[14])
    mode_auto_en = utility.bytes_to_int(byte_data[15])

    #telemetry
    utils._read_telemetry('temp_indoor', temp_indoor)
    utils._read_telemetry('temp_outdoor', temp_outdoor)
    utils._read_telemetry('humid_indoor', humid_indoor)

    #clien attributes
    utils._read_attribute('airc1_command', airc1_command)
    utils._read_attribute('airc2_command', airc2_command)
    utils._read_attribute('fan_command', fan_command)
    utils._read_attribute('thr_temp_1', thr_temp_1)
    utils._read_attribute('thr_temp_2', thr_temp_2)
    utils._read_attribute('thr_temp_3', thr_temp_3)
    utils._read_attribute('thr_temp_4', thr_temp_4)
    utils._read_attribute('airc_count', airc_count)
    utils._read_attribute('mode_auto_en', mode_auto_en)
