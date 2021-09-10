from config import LOGGER
from config.common import UPDATE_VALUE
from config.common_lcd_services import *

last_cmd_lcd = './last_cmd_screen.json'


def show_temp_condition(_telemetries):
    from control import process_cmd_lcd
    from control.utils import read_to_json, write_to_json

    try:
        all_row = read_to_json(last_cmd_lcd)
        title = 'BAN TIN DIEU HOA'
        if all_row['row1'] != title:
            process_cmd_lcd(ROW_1, UPDATE_VALUE, title)
            all_row['row1'] = title

        if 'acmAirc1RunState' and 'acmAirc2RunState' in _telemetries:
            temp1 = _telemetries['acmAirc1RunState']
            temp2 = _telemetries['acmAirc2RunState']
            cond1 = 'DH1:Tat DH2:Tat'
            cond2 = 'DH1:Bat DH2: Bat'
            cond3 = 'DH1:Bat DH2: Tat'
            cond4 = 'DH1:Tat DH2: Bat'
            if temp1 == 0 and temp2 == 0:
                if all_row['row2'] != cond1:
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, cond1)
                    all_row['row2'] = cond1
            elif temp1 == 1 and temp2 == 1:
                if all_row['row2'] != cond2:
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, cond2)
                    all_row['row2'] = cond2
            elif temp1 == 1 and temp2 == 0:
                if all_row['row2'] != cond3:
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, cond3)
                    all_row['row2'] = cond3
            elif temp1 == 0 and temp2 == 1:
                if all_row['row2'] != cond4:
                    process_cmd_lcd(ROW_2, UPDATE_VALUE, cond4)
                    all_row['row2'] = cond4
        else:
            LOGGER.warning("services > lcd > air_screen_lcd_services ")

        fan1 = 'Quat: Bat'
        fan2 = 'Quat: Tat'
        if 'acmFanRunState' in _telemetries:
            mode_fan = _telemetries['acmFanRunState']
            if mode_fan == 1:
                if all_row['row3'] != fan1:
                    process_cmd_lcd(ROW_3, UPDATE_VALUE, fan1)
                    all_row['row3'] = fan1
            elif mode_fan == 0:
                if all_row['row3'] != fan2:
                    process_cmd_lcd(ROW_3, UPDATE_VALUE, fan2)
                    all_row['row3'] = fan2

        auto = 'Che do: Auto'
        manual = 'Che do: Manual'
        if 'acmAutoMode' in _telemetries:
            mode_auto = _telemetries['acmAutoMode']
            if mode_auto != 0:
                if all_row['row4'] != auto:
                    process_cmd_lcd(ROW_4, UPDATE_VALUE, auto)
                    all_row['row4'] = auto
            else:
                if all_row['row4'] != manual:
                    process_cmd_lcd(ROW_4, UPDATE_VALUE, manual)
                    all_row['row4'] = manual

        # save to file
        write_to_json(all_row, last_cmd_lcd)

    except Exception as ex:
        LOGGER.warning('Error at call function in menu_thread with message: %s', ex.message)


def show_time_condition(_telemetries):
    from control import process_cmd_lcd
    from control.utils import read_to_json, write_to_json

    try:
        all_row = read_to_json(last_cmd_lcd)
        if 'acmRunTimeAirc1' in _telemetries:
            time1 = _telemetries['acmRunTimeAirc1']
            cond1 = 'T.gian DH1: ' + str(time1) + 'h'
            if all_row['row2'] != cond1:
                process_cmd_lcd(ROW_2, UPDATE_VALUE, cond1)
                all_row['row2'] = cond1
        else:
            LOGGER.warning("Time condition 1 is not exist in telemetries")

        if 'acmRunTimeAirc2' in _telemetries:
            time2 = _telemetries['acmRunTimeAirc2']
            cond2 = 'T.gian DH2: ' + str(time2) + 'h'
            if all_row['row3'] != cond2:
                process_cmd_lcd(ROW_3, UPDATE_VALUE, cond2)
                all_row['row3'] = cond2
        else:
            LOGGER.warning("Time condition 2 is not exist in telemetries")

        if 'acmRunTimeFan' in _telemetries:
            time3 = _telemetries['acmRunTimeFan']
            fan = 'T.gian Quat: ' + str(time3) + 'h'
            if all_row['row4'] != fan:
                process_cmd_lcd(ROW_4, UPDATE_VALUE, fan)
                all_row['row4'] = fan
        else:
            LOGGER.warning("Time fan is not exist in telemetries")
        # save to file
        write_to_json(all_row, last_cmd_lcd)

    except Exception as ex:
        LOGGER.warning('Error at call function in menu_thread with message: %s', ex.message)
