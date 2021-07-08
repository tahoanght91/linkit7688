OP_CODE_SEND_LCD = 0X31

EVENT_NONE = 0
EVENT_DOWN = 1
EVENT_UP = 2
EVENT_HOLD = 3
EVENT_POWER = 4

MAX_INDEX_MENU = 2
MIN_INDEX_MENU = 0

MENU_LEVEL_1 = 1
MENU_LEVEL_2 = 2
MENU_LEVEL_3 = 3

SALT_DOLLAR_SIGN = '$$'
LCD_ACK = b'\xa0\x02\x11\x00'

ROW_1 = 1
ROW_2 = 2
ROW_3 = 3
ROW_4 = 4

KEYCODE_11 = 257
KEYCODE_12 = 513
KEYCODE_13 = 1025
KEYCODE_14 = 2049
KEYCODE_15 = 4097
KEYCODE_16 = 8193
KEYCODE_21 = 258
KEYCODE_22 = 514
KEYCODE_23 = 1026
KEYCODE_24 = 2050
KEYCODE_25 = 4098
KEYCODE_26 = 8194
KEYCODE_31 = 260
KEYCODE_32 = 516
KEYCODE_33 = 1028
KEYCODE_34 = 2052
KEYCODE_35 = 4100
KEYCODE_36 = 8196


BUTTON_11_EVENT_UP = 0  # exit to main display
BUTTON_12_EVENT_UP = 1  # warning display
BUTTON_13_EVENT_UP = 2  # air condition
BUTTON_14_EVENT_UP = 3  # up
BUTTON_15_EVENT_UP = 4  # rfid
BUTTON_16_EVENT_UP = 5
BUTTON_21_EVENT_UP = 6
BUTTON_22_EVENT_UP = 7
BUTTON_23_EVENT_UP = 8  # left
BUTTON_24_EVENT_UP = 9  # ok
BUTTON_25_EVENT_UP = 10  # right
BUTTON_26_EVENT_UP = 11 # security sensor
BUTTON_31_EVENT_UP = 12
BUTTON_32_EVENT_UP = 13
BUTTON_33_EVENT_UP = 14  # setting
BUTTON_34_EVENT_UP = 15  # down
BUTTON_35_EVENT_UP = 16  # ATS
BUTTON_36_EVENT_UP = 17
BUTTON_11_EVENT_HOLD = 18
BUTTON_12_EVENT_HOLD = 19
BUTTON_13_EVENT_HOLD = 20
BUTTON_14_EVENT_HOLD = 21
BUTTON_15_EVENT_HOLD = 22
BUTTON_16_EVENT_HOLD = 23
BUTTON_21_EVENT_HOLD = 24
BUTTON_22_EVENT_HOLD = 25
BUTTON_23_EVENT_HOLD = 26
BUTTON_24_EVENT_HOLD = 27
BUTTON_25_EVENT_HOLD = 28
BUTTON_26_EVENT_HOLD = 29
BUTTON_31_EVENT_HOLD = 30
BUTTON_32_EVENT_HOLD = 31
BUTTON_33_EVENT_HOLD = 32
BUTTON_34_EVENT_HOLD = 33
BUTTON_35_EVENT_HOLD = 34
BUTTON_36_EVENT_HOLD = 35
LIST_KEYCODE = [KEYCODE_11, KEYCODE_12, KEYCODE_13, KEYCODE_14, KEYCODE_15, KEYCODE_16,
                KEYCODE_21, KEYCODE_22, KEYCODE_23, KEYCODE_24, KEYCODE_25, KEYCODE_26,
                KEYCODE_31, KEYCODE_32, KEYCODE_33, KEYCODE_34, KEYCODE_35, KEYCODE_36]
EVENT_NONE_BT = 0
EVENT_UP_BT = 1
EVENT_HOLD_BT = 2
LIST_EVENT_BT = [EVENT_NONE_BT, EVENT_UP_BT, EVENT_HOLD_BT]

LOG_BUTTON = {BUTTON_11_EVENT_UP: 'BUTTON_11_EVENT_UP', BUTTON_12_EVENT_UP: 'BUTTON_12_EVENT_UP', BUTTON_13_EVENT_UP: 'BUTTON_13_EVENT_UP', BUTTON_14_EVENT_UP: 'BUTTON_14_EVENT_UP', BUTTON_15_EVENT_UP: 'BUTTON_15_EVENT_UP', BUTTON_16_EVENT_UP: 'BUTTON_16_EVENT_UP',
              BUTTON_21_EVENT_UP: 'BUTTON_21_EVENT_UP', BUTTON_22_EVENT_UP: 'BUTTON_22_EVENT_UP', BUTTON_23_EVENT_UP: 'BUTTON_23_EVENT_UP', BUTTON_24_EVENT_UP: 'BUTTON_24_EVENT_UP', BUTTON_25_EVENT_UP: 'BUTTON_25_EVENT_UP', BUTTON_26_EVENT_UP: 'BUTTON_26_EVENT_UP',
              BUTTON_31_EVENT_UP: 'BUTTON_31_EVENT_UP', BUTTON_32_EVENT_UP: 'BUTTON_32_EVENT_UP', BUTTON_33_EVENT_UP: 'BUTTON_33_EVENT_UP', BUTTON_34_EVENT_UP: 'BUTTON_34_EVENT_UP', BUTTON_35_EVENT_UP: 'BUTTON_35_EVENT_UP', BUTTON_36_EVENT_UP: 'BUTTON_36_EVENT_UP',
              BUTTON_11_EVENT_HOLD: 'BUTTON_11_EVENT_HOLD', BUTTON_12_EVENT_HOLD: 'BUTTON_12_EVENT_HOLD', BUTTON_13_EVENT_HOLD: 'BUTTON_13_EVENT_HOLD', BUTTON_14_EVENT_HOLD: 'BUTTON_14_EVENT_HOLD', BUTTON_15_EVENT_HOLD: 'BUTTON_15_EVENT_HOLD', BUTTON_16_EVENT_HOLD: 'BUTTON_16_EVENT_HOLD',
              BUTTON_21_EVENT_HOLD: 'BUTTON_21_EVENT_HOLD', BUTTON_22_EVENT_HOLD: 'BUTTON_22_EVENT_HOLD', BUTTON_23_EVENT_HOLD: 'BUTTON_23_EVENT_HOLD', BUTTON_24_EVENT_HOLD: 'BUTTON_24_EVENT_HOLD', BUTTON_25_EVENT_HOLD: 'BUTTON_25_EVENT_HOLD', BUTTON_26_EVENT_HOLD: 'BUTTON_26_EVENT_HOLD',
              BUTTON_31_EVENT_HOLD: 'BUTTON_31_EVENT_HOLD', BUTTON_32_EVENT_HOLD: 'BUTTON_32_EVENT_HOLD', BUTTON_33_EVENT_HOLD: 'BUTTON_33_EVENT_HOLD', BUTTON_34_EVENT_HOLD: 'BUTTON_34_EVENT_HOLD', BUTTON_35_EVENT_HOLD: 'BUTTON_35_EVENT_HOLD', BUTTON_36_EVENT_HOLD: 'BUTTON_36_EVENT_HOLD'}

ESC = BUTTON_11_EVENT_UP
CANH_BAO = BUTTON_12_EVENT_UP
CAM_BIEN = BUTTON_26_EVENT_UP
DIEU_HOA = BUTTON_13_EVENT_UP
ATS = BUTTON_35_EVENT_UP
SETTING = BUTTON_33_EVENT_UP
RFID = BUTTON_15_EVENT_UP

UP = BUTTON_14_EVENT_UP
DOWN = BUTTON_34_EVENT_UP
LEFT = BUTTON_23_EVENT_UP
RIGHT = BUTTON_25_EVENT_UP
OK = BUTTON_24_EVENT_UP

MENU_LV_1 = [ESC, CANH_BAO, CAM_BIEN, DIEU_HOA, ATS, SETTING, RFID]

# CANH BAO
CB_CHAY = 'mccFireState'
CB_KHOI = 'mccSmokeState'
CB_NGAP = 'mccFloodState'
CB_CUA = 'mccDoorState'
CB_NHIET = 'acmTempAlarm'
CB_DOAM = 'acmHumidAlarm'
CB_DIENAPLUOI = 'atsVacThresholdState'
CB_DIENMAYPHAT = 'atsVgenThresholdState'
CB_RFID = 'mccListRfid'
CB_DCLow = 'mccDcLowState'

