import utility
from config import BYTE_ORDER
from . import utils


def extract(byte_data):
    # client attributes
    acmOnlineState = utility.bytes_to_int(byte_data[0])
    acmAutoMode = utility.bytes_to_int(byte_data[1])
    acmTempError = utility.bytes_to_int(byte_data[2])
    acmHumidError = utility.bytes_to_int(byte_data[3])
    acmIState = utility.bytes_to_int(byte_data[4])
    acmAirc1RunState = utility.bytes_to_int(byte_data[5])
    acmAirc2RunState = utility.bytes_to_int(byte_data[6])
    acmAirc1Error = utility.bytes_to_int(byte_data[7])
    acmAirc2Error = utility.bytes_to_int(byte_data[8])
    acmFanRunState = utility.bytes_to_int(byte_data[9])
    acmFanError = utility.bytes_to_int(byte_data[10])
    acmRunTimeAirc1 = utility.bytes_to_int(byte_data[25])
    acmRunTimeAirc2 = utility.bytes_to_int(byte_data[26])
    acmRunTimeFan = utility.bytes_to_int(byte_data[27])

    # telemetry
    acmTempIndoor = utility.bytes_to_int(byte_data[11:13], byteorder=BYTE_ORDER)
    acmTempOutdoor = utility.bytes_to_int(byte_data[13:15], byteorder=BYTE_ORDER)
    acmHumidIndoor = utility.bytes_to_int(byte_data[15:17], byteorder=BYTE_ORDER)
    acmT1Temp = utility.bytes_to_int(byte_data[17:19], byteorder=BYTE_ORDER)
    acmT2Temp = utility.bytes_to_int(byte_data[19:21], byteorder=BYTE_ORDER)
    acmT3Temp = utility.bytes_to_int(byte_data[21:23], byteorder=BYTE_ORDER)
    acmT4Temp = utility.bytes_to_int(byte_data[23:25], byteorder=BYTE_ORDER)

    # telemetry
    utils._read_telemetry('acmTempIndoor', acmTempIndoor)
    utils._read_telemetry('acmTempOutdoor', acmTempOutdoor)
    utils._read_telemetry('acmHumidIndoor', acmHumidIndoor)
    utils._read_telemetry('acmT1Temp', acmT1Temp)
    utils._read_telemetry('acmT2Temp', acmT2Temp)
    utils._read_telemetry('acmT3Temp', acmT3Temp)
    utils._read_telemetry('acmT4Temp', acmT4Temp)
    utils._read_telemetry('acmAirc1RunState', acmAirc1RunState)
    utils._read_telemetry('acmAirc2RunState', acmAirc2RunState)
    utils._read_telemetry('acmFanRunState', acmFanRunState)
    utils._read_telemetry('acmAutoMode', acmAutoMode)
    utils._read_telemetry('acmOnlineState', acmOnlineState)
    utils._read_telemetry('acmRunTimeAirc1', acmRunTimeAirc1)
    utils._read_telemetry('acmRunTimeAirc2', acmRunTimeAirc2)
    utils._read_telemetry('acmRunTimeFan', acmRunTimeFan)

    # client attributes
    utils._read_telemetry('acmTempError', acmTempError)
    utils._read_telemetry('acmHumidError', acmHumidError)
    utils._read_attribute('acmIState', acmIState)
    utils._read_attribute('acmAirc1Error', acmAirc1Error)
    utils._read_attribute('acmAirc2Error', acmAirc2Error)
    utils._read_attribute('acmFanError', acmFanError)

