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
DEVICE_MCC_1 = 'device_MCC_1'
DEVICE_ATS_1 = 'device_ATS_1'
DEVICE_ACM_1 = 'device_ACM_1'

# rpc
AUTO = 'setAuto'
CONTROL = 'setControl'
GET_STATE = 'getState'
GET_VALUE = 'getValue'

# command
COMMAND_CONTROL = 'control'
# ATS
COMMAND_ATS_AUTO = 'auto'
COMMAND_ATS_MAIN = 'main'
COMMAND_ATS_GEN = 'gen'

# MCC
#module MCC
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

# ACM
#module acm
COMMAND_ACM_AUTO_ON = 'onAutoAcm'
COMMAND_ACM_AUTO_OFF = 'offAutoAcm'
# air conditioner 1
COMMAND_AIRC_1_ON = 'onAirc1'
COMMAND_AIRC_1_OFF = 'offAirc1'
# air conditioner 2
COMMAND_AIRC_2_ON = 'onAirc2'
COMMAND_AIRC_2_OFF = 'offAirc2'
# fan
COMMAND_FAN_ON = 'onFan'
COMMAND_FAN_OFF = 'offFan'

# method
# airc1
GET_SATE_AIRC_1 = 'getStateAirc1'
GET_VALUE_AIRC_1 = 'getValueAirc1'
SET_AIRC_CONTROL_1 = 'setControlAirc1'
SET_AIRC_AUTO_1 = 'setAutoAirc1'
# airc2
GET_STATE_AIRC_2 = 'getStateAirc2'
GET_VALUE_AIRC_2 = 'getValueAirc2'
SET_AIRC_CONTROL_2 = 'setControlAirc2'
SET_AIRC_AUTO_2 = 'setAutoAirc2'
# fan
GET_STATE_FAN = 'getStateFan'
GET_VALUE_FAN = 'getValueFan'
SET_FAN_CONTROL = 'setControlFan'
SET_FAN_AUTO = 'setAutoFan'
# ats
GET_STATE_ATS = 'getStateAts'
SET_ATS_CONTROL_MAIN = 'setControlAtsMain'
SET_ATS_CONTROL_GEN = 'setControlAtsGen'
SET_ATS_AUTO = 'setAutoAts'
# crmu
GET_STATE_CRMU = 'getStateControlCrmu'
SET_CRMU_CONTROL = 'setControlCrmu'
SET_CRMU_AUTO = 'setAutoCrmu'
