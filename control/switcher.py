from config.common_command import *


# Command MCC
def parse_mcc_command_to_number(command):
    switcher_mcc_command = {
        COMMAND_MCC_OPEN_DOOR: 0,
        COMMAND_MCC_CLOSE_DOOR: 1,
        COMMAND_MCC_OFF_BELL: 0,
        COMMAND_MCC_ON_BELL: 1,
        COMMAND_MCC_OFF_VMB: 0,
        COMMAND_MCC_ON_VMB: 1,
        COMMAND_MCC_OFF_VSENS: 0,
        COMMAND_MCC_ON_VSENS: 1,
        COMMAND_MCC_OFF_LAMP: 0,
        COMMAND_MCC_ON_LAMP: 1,
        COMMAND_MCC_OFF_CAM: 0,
        COMMAND_MCC_ON_CAM: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_1: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_1: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_2: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_2: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_3: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_3: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_4: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_4: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_5: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_5: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_6: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_6: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_7: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_7: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_8: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_8: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_9: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_9: 1,
        COMMAND_MCC_OFF_DOUT_REVERSED_10: 0,
        COMMAND_MCC_ON_DOUT_REVERSED_10: 1
    }
    return switcher_mcc_command.get(command, "Out of range!")


# Command ACM
def parse_acm_command_to_number(command):
    switcher_acm_command = {
        COMMAND_ACM_AUTO_OFF: 0,
        COMMAND_ACM_AUTO_ON: 1,
        COMMAND_ACM_AIRC_1_OFF: 0,
        COMMAND_ACM_AIRC_1_ON: 1,
        COMMAND_ACM_AIRC_2_OFF: 0,
        COMMAND_ACM_AIRC_2_ON: 1,
        COMMAND_ACM_FAN_OFF: 0,
        COMMAND_ACM_FAN_ON: 1,
        COMMAND_ACM_SELF_PROPELLED_OFF: 0,
        COMMAND_ACM_SELF_PROPELLED_ON: 1
    }
    return switcher_acm_command.get(command, "Out of range!")


# Command ATS
def parse_ats_command_to_number(command):
    switcher_ats_command = {
        COMMAND_ATS_MAIN_ON: 0,
        COMMAND_ATS_GEN_ON: 1,
        COMMAND_ATS_AUTO_ON: 2,
        COMMAND_ATS_OFF: 3,
        COMMAND_ATS_STOP_GEN: 0,
        COMMAND_ATS_START_GEN: 1
    }
    return switcher_ats_command.get(command, "Out of range!")


# shared attributes ATS
def parse_ats_shared_attributes_to_number(key):
    switcher_ats = {
        'atsGenInactiveStartTime': 1,
        'atsVacMaxThreshold': 2,
        'atsGenAutoResetTimeout': 3,
        'atsVgenMinThreshold': 4,
        'atsVacMinThreshold': 5,
        'atsGenAutoResetMode': 6,
        'atsGenInactiveEndTime': 7,
        'atsGenAutoResetMax': 8,
        'atsGenDeactivateMode': 9,
        'atsVgenMaxThreshold': 10,
        'atsVgenIdleCoolingTimeout': 11,
        'atsVgenIdleWarmUpTimeout': 12,
        'atsVacStabilizeTimeout': 13,
        'atsGenActiveDuration': 14
    }
    return switcher_ats.get(key, -1)


# shared attributes MCC
def parse_mcc_shared_attributes_to_number(key):
    switcher_mcc = {
        'mccPeriodReadDataIO': 1,
        'mccPeriodSendTelemetry': 2,
        'mccPeriodUpdate': 3,
        'mccDcMinThreshold': 4
    }
    return switcher_mcc.get(key, -1)


# shared attributes ACM
def parse_acm_shared_attributes_to_number(key):
    switcher_acm = {
        'acmControlAuto': 1,
        'acmAlternativeTime': 2,
        'acmRunTime': 3,
        'acmRestTime': 4,
        'acmGenAllow': 5,
        'acmVacThreshold': 6,
        'acmMinTemp': 7,
        'acmMaxTemp': 8,
        'acmMinHumid': 9,
        'acmMaxHumid': 10,
        'acmExpectedTemp': 11,
        'acmExpectedHumid': 12,
        'acmT1Temp': 13,
        'acmT2Temp': 14,
        'acmT3Temp': 15,
        'acmT4Temp': 16
    }
    return switcher_acm.get(key, -1)

