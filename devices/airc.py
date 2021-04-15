import utility
from . import utils
from config import BYTE_ORDER


def extract(byte_data):
    '''
    Extract the data from an AIRC message sent from the IO
    '''
    temp = float(utility.bytes_to_int(byte_data[0:2], byteorder=BYTE_ORDER) / 10)
    humid = utility.bytes_to_int(byte_data[2:4], byteorder=BYTE_ORDER)
    airc1_temp = float(utility.bytes_to_int(byte_data[4:6], byteorder=BYTE_ORDER) / 10)
    airc2_temp = float(utility.bytes_to_int(byte_data[6:8], byteorder=BYTE_ORDER) / 10)
    outdoor_temp = float(utility.bytes_to_int(byte_data[8:10], byteorder=BYTE_ORDER) / 10)
    airc1_run_state = utility.bytes_to_int(byte_data[10])
    airc1_error = utility.bytes_to_int(byte_data[11])
    airc2_run_state = utility.bytes_to_int(byte_data[12])
    airc2_error = utility.bytes_to_int(byte_data[13])

    airc1_run_threshold = utility.bytes_to_int(byte_data[14:16], byteorder=BYTE_ORDER)
    airc2_run_threshold = utility.bytes_to_int(byte_data[16:18], byteorder=BYTE_ORDER)

    airc1_command = utility.bytes_to_int(byte_data[18])
    airc2_command = utility.bytes_to_int(byte_data[19])
    ir_status = utility.bytes_to_int(byte_data[20])
    learn_cmd_id = utility.bytes_to_int(byte_data[21])

    online_status = utility.bytes_to_int(byte_data[22])

    utils._read_telemetry('aircTemp', temp)
    utils._read_telemetry('aircHumid', humid)
    utils._read_telemetry('aircAirc1Temp', airc1_temp)
    utils._read_telemetry('aircAirc2Temp', airc2_temp)
    utils._read_telemetry('aircOutdoorTemp', outdoor_temp)
    utils._read_attribute('aircAirc1RunState', airc1_run_state)
    utils._read_attribute('aircAirc1Error', airc1_error)
    utils._read_attribute('aircAirc2RunState', airc2_run_state)
    utils._read_attribute('aircAirc2Error', airc2_error)
    utils._read_attribute('aircAirc1RunThreshold', airc1_run_threshold)
    utils._read_attribute('aircAirc2RunThreshold', airc2_run_threshold)
    utils._read_attribute('aircAirc1Command', airc1_command)
    utils._read_attribute('aircAirc2Command', airc2_command)
    utils._read_attribute('aircIrStatus', ir_status)
    utils._read_attribute('aircLearnCmdId', learn_cmd_id)
    utils._read_attribute('aircOnlineStatus', online_status)