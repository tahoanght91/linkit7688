# TRUONG
from config import *
from config.common import UPDATE_VALUE
from config.common_lcd_services import *

last_cmd_lcd = './last_cmd_screen.json'


# man hinh mac dinh
def security_sensor_screen_1(_telemitries):
    from control import process_cmd_lcd
    from control.utils import read_to_json, write_to_json

    try:
        LOGGER.debug('List telemetries in sensor_screen: %s', _telemitries)
        mcc_smoke_tate = ''
        mcc_fire_state = ''
        mcc_flood_state = ''

        all_row = read_to_json(last_cmd_lcd)
        # thay doi cac state neu co trong telemetries, neu khong se dung mac dinh la ''
        if "mccSmokeState" in _telemitries.keys():
            mcc_smoke_tate = _telemitries.get("mccSmokeState")
        else:
            LOGGER.warning(
                "operate > icd_thread > security_sensor_screen_1: key 'mccSmokeState' is not in Telemetries")

        if "mccFireState" in _telemitries.keys():
            mcc_fire_state = _telemitries.get("mccFireState")
        else:
            LOGGER.warning(
                "operate > icd_thread > security_sensor_screen_1: key 'mccFireState' is not in Telemetries")

        if "mccFloodState" in _telemitries.keys():
            mcc_flood_state = _telemitries.get("mccFloodState")
        else:
            LOGGER.warning(
                "operate > icd_thread > security_sensor_screen_1: key 'mccFloodState' is not in Telemetries")

        # In ra man hinh
        row1 = "CAM BIEN AN NINH"
        row2 = "Khoi: " + str(mcc_smoke_tate)
        row3 = "Chay: " + str(mcc_fire_state)
        row4 = "Ngap nuoc: " + str(mcc_flood_state)
        if all_row['row1'] != row1:
            process_cmd_lcd(ROW_1, UPDATE_VALUE, row1)
            all_row['row1'] = row1
        if all_row['row2'] != row2:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, row2)
            all_row['row2'] = row2
        if all_row['row3'] != row3:
            process_cmd_lcd(ROW_3, UPDATE_VALUE, row3)
            all_row['row3'] = row3
        if all_row['row4'] != row4:
            process_cmd_lcd(ROW_4, UPDATE_VALUE, row4)
            all_row['row4'] = row4

        # save to file
        write_to_json(all_row, last_cmd_lcd)
    except Exception as ex:
        LOGGER.warning('operate > icd_thread > default_security_sensor_screen: %s', ex.message)


def security_sensor_screen_2(_telemitries):
    from control import process_cmd_lcd
    from control.utils import read_to_json, write_to_json

    try:
        mcc_flood_state = ''
        mcc_door_button = ''
        mcc_move_state = ''
        all_row = read_to_json(last_cmd_lcd)

        # tao String mac dinh in ra man hinh
        if "mccFloodState" in _telemitries.keys():
            mcc_flood_state = _telemitries.get("mccFloodState")
        else:
            LOGGER.warning(
                "operate > icd_thread > security_sensor_screen_2: key 'mccFloodState' is not in Telemetries")

        if "mccDoorButton" in _telemitries.keys():
            mcc_door_button = _telemitries.get("mccDoorButton")
        else:
            LOGGER.warning(
                "operate > icd_thread > security_sensor_screen_2: key 'mccDoorButton' is not in Telemetries")

        if "mccMoveState" in _telemitries.keys():
            mcc_move_state = _telemitries.get("mccMoveState")
        else:
            LOGGER.warning(
                "operate > icd_thread > security_sensor_screen_2: key 'mccMoveState' is not in Telemetries")

        # In ra man hinh
        row1 = "CAM BIEN AN NINH"
        row2 = "Ngap nuoc: " + str(mcc_flood_state)
        row3 = "Cua: " + str(mcc_door_button)
        row4 = "Chuyen dong: " + str(mcc_move_state)
        if all_row['row1'] != row1:
            process_cmd_lcd(ROW_1, UPDATE_VALUE, row1)
            all_row['row1'] = row1
        if all_row['row2'] != row2:
            process_cmd_lcd(ROW_2, UPDATE_VALUE, row2)
            all_row['row2'] = row2
        if all_row['row3'] != row3:
            process_cmd_lcd(ROW_3, UPDATE_VALUE, row3)
            all_row['row3'] = row3
        if all_row['row4'] != row4:
            process_cmd_lcd(ROW_4, UPDATE_VALUE, row4)
            all_row['row4'] = row4

        # save to file
        write_to_json(all_row, last_cmd_lcd)
    except Exception as ex:
        LOGGER.warning('operate > icd_thread > chance_security_sensor_screen: %s', ex.message)
