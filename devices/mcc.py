from config import BYTE_ORDER
from utility import bytes_to_int
from .utils import _read_attribute, _read_telemetry


def extract(byte_data):
    #telemetry
    mccSmokeState = bytes_to_int(byte_data[0])
    mccFireState = bytes_to_int(byte_data[1])
    mccMoveState = bytes_to_int(byte_data[2])
    mccDoorState = bytes_to_int(byte_data[3])
    mccFloodState = bytes_to_int(byte_data[4])
    mccDoorButton = bytes_to_int(byte_data[5])
    din6 = bytes_to_int(byte_data[6])
    din7 = bytes_to_int(byte_data[7])
    mccBellState = bytes_to_int(byte_data[8])
    mccDcIbat1 = bytes_to_int(byte_data[9:11], byteorder=BYTE_ORDER)
    mccDcVbat1 = bytes_to_int(byte_data[11:13], byteorder=BYTE_ORDER)
    mccDeviceTemp = bytes_to_int(byte_data[13:15], byteorder=BYTE_ORDER)
    mccRackTemp = bytes_to_int(byte_data[15:17], byteorder=BYTE_ORDER)
    mccDcBat1Temp = bytes_to_int(byte_data[17:19], byteorder=BYTE_ORDER)
    mccDcBat2Temp = bytes_to_int(byte_data[19:21], byteorder=BYTE_ORDER)
    mccDcAccumulatorSate = bytes_to_int(byte_data[21])
    mccDcVcabinet = bytes_to_int(byte_data[22:24], byteorder=BYTE_ORDER)
    mccDcIcabinet = bytes_to_int(byte_data[24:26], byteorder=BYTE_ORDER)
    mccDcPcabinet = bytes_to_int(byte_data[26:28], byteorder=BYTE_ORDER)
    mccDcPaccumulator = bytes_to_int(byte_data[28:30], byteorder=BYTE_ORDER)
    mccSystemClock = bytes_to_int(byte_data[30:32], byteorder=BYTE_ORDER)

    #client attributes
    mccRfidConnectState = bytes_to_int(byte_data[32])
    mccDcCabinetSate = bytes_to_int(byte_data[33])

    #telemetry
    _read_telemetry('mccSmokeState', mccSmokeState)
    _read_telemetry('mccFireState', mccFireState)
    _read_telemetry('mccMoveState', mccMoveState)
    _read_telemetry('mccDoorState', mccDoorState)
    _read_telemetry('mccBellState', mccBellState)
    _read_telemetry('mccFloodState', mccFloodState)
    _read_telemetry('mccDoorButton', mccDoorButton)
    _read_telemetry('din6', din6)
    _read_telemetry('din7', din7)
    _read_telemetry('mccDcIbat1', mccDcIbat1)
    _read_telemetry('mccDcVbat1', mccDcVbat1)
    _read_telemetry('mccDeviceTemp', mccDeviceTemp)
    _read_telemetry('mccRackTemp', mccRackTemp)
    _read_telemetry('mccDcBat1Temp', mccDcBat1Temp)
    _read_telemetry('mccDcBat2Temp', mccDcBat2Temp)
    _read_telemetry('mccDoorButton', mccDoorButton)
    _read_telemetry('mccDcAccumulatorSate', mccDcAccumulatorSate)
    _read_telemetry('mccDcVcabinet', mccDcVcabinet)
    _read_telemetry('mccDcIcabinet', mccDcIcabinet)
    _read_telemetry('mccDcPcabinet', mccDcPcabinet)
    _read_telemetry('mccDcPaccumulator', mccDcPaccumulator)
    _read_telemetry('mccSystemClock', mccSystemClock)

    #client attributes
    _read_attribute('mccRfidConnectState', mccRfidConnectState)
    _read_attribute('mccDcCabinetSate', mccDcCabinetSate)
