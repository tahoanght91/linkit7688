# TRUONG
from config import *
from config.common import *
from config.common_lcd_services import *
from operate.lcd_thread import create_cmd_multi


def security_sensor_screen(_telemitries, _moving_screen):
    try:
        cmd_lcd[UPDATE_VALUE] = create_cmd_multi("CAM BIEN AN NINH", ROW_1)
        if not _moving_screen:
            if _telemitries.get("mccSmokeState") == 1:
                cmd_lcd[UPDATE_VALUE] = str("Khoi: 1") + SALT_DOLLAR_SIGN + str(ROW_2) + END_CMD
            if _telemitries.get("mccFireState") == 1:
                cmd_lcd[UPDATE_VALUE] = str("Chay: 1") + SALT_DOLLAR_SIGN + str(ROW_3) + END_CMD
            if _telemitries.get("mccFloodState") == 1:
                cmd_lcd[UPDATE_VALUE] = str("Ngap: 1") + SALT_DOLLAR_SIGN + str(ROW_4) + END_CMD
        else:
            if _telemitries.get("mccFloodState") == 1:
                cmd_lcd[UPDATE_VALUE] = str("Ngap: 1") + SALT_DOLLAR_SIGN + str(ROW_2) + END_CMD
            if _telemitries.get("mccDoorButton") == 1:
                cmd_lcd[UPDATE_VALUE] = str("Cua: 1") + SALT_DOLLAR_SIGN + str(ROW_3) + END_CMD
            if _telemitries.get("mccMoveState") == 1:
                cmd_lcd[UPDATE_VALUE] = str("Chuyen dong: 1") + SALT_DOLLAR_SIGN + str(ROW_4) + END_CMD
    except Exception as ex:
        LOGGER.error('operate > icd_thread > security_sensor_screen: %s', ex.message)


