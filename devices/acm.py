import utility
from . import utils
from config import BYTE_ORDER


def extract(byte_data):
    #telemetry
    acmTempIndoor = utility.bytes_to_int(byte_data[0:2], byteorder=BYTE_ORDER)
    acmTempOutdoor = utility.bytes_to_int(byte_data[2:4], byteorder=BYTE_ORDER)
    acmHumidIndoor = utility.bytes_to_int(byte_data[4:6], byteorder=BYTE_ORDER)

    #client attributes
    acmTempError = utility.bytes_to_int(byte_data[7])
    acmHumidError = utility.bytes_to_int(byte_data[8])
    acmAutoMode = utility.bytes_to_int(byte_data[9])
    acmOnlineState = utility.bytes_to_int(byte_data[10])
    acmIState = utility.bytes_to_int(byte_data[11])
    acmAirc1RunState = utility.bytes_to_int(byte_data[12])
    acmAirc2RunState = utility.bytes_to_int(byte_data[13])
    acmAirc1Error = utility.bytes_to_int(byte_data[14])
    acmAirc2Error = utility.bytes_to_int(byte_data[15])
    acmFanRunState = utility.bytes_to_int(byte_data[16])
    acmFanError = utility.bytes_to_int(byte_data[17])

    #telemetry
    utils._read_telemetry('acmTempIndoor', acmTempIndoor)
    utils._read_telemetry('acmTempOutdoor', acmTempOutdoor)
    utils._read_telemetry('acmHumidIndoor', acmHumidIndoor)

    #client attributes
    utils._read_telemetry('acmTempError', acmTempError)
    utils._read_telemetry('acmHumidError', acmHumidError)
    utils._read_attribute('acmAutoMode', acmAutoMode)
    utils._read_attribute('acmOnlineState', acmOnlineState)
    utils._read_attribute('acmIState', acmIState)
    utils._read_attribute('acmAirc1RunState', acmAirc1RunState)
    utils._read_attribute('acmAirc2RunState', acmAirc2RunState)
    utils._read_attribute('acmAirc1Error', acmAirc1Error)
    utils._read_attribute('acmAirc2Error', acmAirc2Error)
    utils._read_attribute('acmFanRunState', acmFanRunState)
    utils._read_attribute('acmFanError', acmFanError)
