# device_name
from config.common_command import *

DEVICE_AIRC = 'device_airc'
DEVICE_AIRC_1 = 'device_airc1'
DEVICE_AIRC_2 = 'device_airc2'
DEVICE_MISC = 'device_misc'
DEVICE_CRMU = 'device_crmu'
DEVICE_ATU = 'device_atu'
DEVICE_DC = 'device_dc'
DEVICE_ATS = 'device_ats'
DEVICE_FIRE_SENSOR = 'device_fire_sensor'
DEVICE_FLOOD_SENSOR = 'device_flood_sensor'
DEVICE_MOVE_SENSOR = 'device_move_sensor'
DEVICE_SMOKE_SENSOR = 'device_smoke_sensor'

DEVICE_MDC_1 = 'device_MDC_1'
DEVICE_MCC_1 = 'GW005_MCC_1'
DEVICE_ATS_1 = 'GW005_ATS_1'
DEVICE_ACM_1 = 'GW005_ACM_1'

# ID DEVICE
ID_MCC = 97
ID_ACM = 99
ID_ATS = 98

# FORMAT RPC
CHAR_B = 'B'
FORMAT_RPC = 'BBBBBB'
FORMAT_RFID = 'BBBBB'
FORMAT_LCD = 'BBBBBB'

# BYTES SHARED ATTRIBUTES
BYTES_SA_MCC = 8
BYTES_SA_ACM = 18
BYTES_SA_ATS = 28

# SHARED ATTRIBUTES
TYPE = 'type'
ID_SHARED_ATTRIBUTES = 'idSharedAttributes'
VALUE = 'value'
MCC = 'mcc'
ACM = 'acm'
ATS = 'ats'
KEY_MCC = 'sharedMcc'
KEY_ATS = 'sharedAts'
KEY_ACM = 'sharedAcm'

# rpc
AUTO = 'setAuto'
CONTROL = 'setControl'
GET_STATE = 'getState'
GET_VALUE = 'getValue'

# compare rfid card
SHARED_ATTRIBUTES_RFID_CARD = 'mccRespCardId'

# lcd service
LCD_SERVICE = 'lcdService'

# list command
list_command = [COMMAND_MCC_OPEN_DOOR, COMMAND_MCC_CLOSE_DOOR, COMMAND_MCC_ON_BELL, COMMAND_MCC_OFF_BELL,
                COMMAND_MCC_ON_LAMP, COMMAND_MCC_OFF_LAMP, COMMAND_MCC_OFF_DOUT_REVERSED_1,
                COMMAND_MCC_ON_DOUT_REVERSED_1,
                COMMAND_MCC_OFF_DOUT_REVERSED_2, COMMAND_MCC_ON_DOUT_REVERSED_2, COMMAND_MCC_OFF_DOUT_REVERSED_3,
                COMMAND_MCC_ON_DOUT_REVERSED_3,
                COMMAND_MCC_OFF_DOUT_REVERSED_4, COMMAND_MCC_ON_DOUT_REVERSED_4, COMMAND_MCC_OFF_DOUT_REVERSED_5,
                COMMAND_MCC_ON_DOUT_REVERSED_5,
                COMMAND_MCC_OFF_DOUT_REVERSED_6, COMMAND_MCC_ON_DOUT_REVERSED_6, COMMAND_MCC_OFF_DOUT_REVERSED_7,
                COMMAND_MCC_ON_DOUT_REVERSED_7,
                COMMAND_MCC_OFF_DOUT_REVERSED_8, COMMAND_MCC_ON_DOUT_REVERSED_8, COMMAND_MCC_OFF_DOUT_REVERSED_9,
                COMMAND_MCC_ON_DOUT_REVERSED_9,
                COMMAND_MCC_OFF_DOUT_REVERSED_10, COMMAND_MCC_ON_DOUT_REVERSED_10, COMMAND_MCC_OFF_DOUT_REVERSED_11,
                COMMAND_MCC_ON_DOUT_REVERSED_11,
                COMMAND_MCC_OFF_DOUT_REVERSED_12, COMMAND_MCC_ON_DOUT_REVERSED_12, COMMAND_MCC_OFF_DOUT_REVERSED_13,
                COMMAND_MCC_ON_DOUT_REVERSED_13,
                COMMAND_ACM_AUTO_OFF, COMMAND_ACM_AUTO_ON, COMMAND_ACM_AIRC_1_OFF, COMMAND_ACM_AIRC_1_ON,
                COMMAND_ACM_AIRC_2_ON, COMMAND_ACM_AIRC_2_OFF, COMMAND_ACM_FAN_OFF,
                COMMAND_ACM_FAN_ON, COMMAND_ACM_SELF_PROPELLED_OFF, COMMAND_ACM_SELF_PROPELLED_ON,
                COMMAND_ATS_ELECTRICITY_SUPPLY_OFF,
                COMMAND_ATS_ELECTRICITY_SUPPLY_ON, COMMAND_ATS_GENERATOR_SUPPLY_OFF, COMMAND_ATS_GENERATOR_SUPPLY_ON,
                COMMAND_ATS_GENERATOR_OFF,
                COMMAND_ATS_GENERATOR_ON, COMMAND_ATS_START_OFF, COMMAND_ATS_START_ON, COMMAND_ATS_SELF_PROPELLED_OFF,
                COMMAND_ATS_SELF_PROPELLED_ON]
