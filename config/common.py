# device_name
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

# rpc
AUTO = 'setAuto'
CONTROL = 'setControl'
GET_STATE = 'getState'
GET_VALUE = 'getValue'

# COMMAND
COMMAND_CONTROL = 'control'

# ATS
COMMAND_ATS_AUTO = 'auto'
COMMAND_ATS_MAIN = 'main'
COMMAND_ATS_GEN = 'gen'

# MCC
# module MCC
COMMAND_MCC_AUTO_ON = 'onAutoMcc'
COMMAND_MCC_AUTO_OFF = 'offAutoMcc'
# door
COMMAND_MCC_OPEN_DOOR = 'openDoor'
COMMAND_MCC_CLOSE_DOOR = 'closeDoor'
# bell
COMMAND_MCC_ON_BELL = 'onBell'
COMMAND_MCC_OFF_BELL = 'offBell'
# lamp
COMMAND_MCC_ON_LAMP = 'onLamp'
COMMAND_MCC_OFF_LAMP = 'offLamp'
# device error
COMMAND_MCC_ON_ERROR = 'onError'
COMMAND_MCC_OFF_ERROR = 'offError'
# compare rfid card
SHARED_ATTRIBUTES_RFID_CARD = 'mccRespCardId'

# ACM
# module acm
COMMAND_ACM_AUTO_ON = 'onAutoAcm'
COMMAND_ACM_AUTO_OFF = 'offAutoAcm'
# air conditioner 1
COMMAND_ACM_AIRC_1_ON = 'onAcmAirc1'
COMMAND_ACM_AIRC_1_OFF = 'offAcmAirc1'
# air conditioner 2
COMMAND_ACM_AIRC_2_ON = 'onAcmAirc2'
COMMAND_ACM_AIRC_2_OFF = 'offAcmAirc2'
# fan
COMMAND_ACM_FAN_ON = 'onAcmFan'
COMMAND_ACM_FAN_OFF = 'offAcmFan'

# METHOD
# module ACM
# auto acm
SET_ACM_AUTO = 'setAutoAcm'
# manual airc1
GET_SATE_ACM_AIRC_1 = 'getStateAcmAirc1'
GET_VALUE_ACM_AIRC_1 = 'getValueAcmAirc1'
SET_ACM_AIRC_CONTROL_1 = 'setControlAcmAirc1'
# manual airc2
GET_STATE_ACM_AIRC_2 = 'getStateAcmAirc2'
GET_VALUE_ACM_AIRC_2 = 'getValueAcmAirc2'
SET_ACM_AIRC_CONTROL_2 = 'setControlAcmAirc2'
# fan
GET_STATE_ACM_FAN = 'getStateAcmFan'
GET_VALUE_ACM_FAN = 'getValueAcmFan'

# ATS
GET_STATE_ATS = 'getStateAts'
SET_ATS_CONTROL_MAIN = 'setControlAtsMain'
SET_ATS_CONTROL_GEN = 'setControlAtsGen'
SET_ATS_AUTO = 'setAutoAts'

# MCC
GET_STATE_MCC_DOOR = 'getStateMccDoor'
SET_CRMU_CONTROL = 'setControlCrmu'
SET_CRMU_AUTO = 'setAutoCrmu'
