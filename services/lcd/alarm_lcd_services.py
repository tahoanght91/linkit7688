from datetime import datetime
from config import *
from config.common import *
from config.common_lcd_services import *

BAN_TIN_CANH_BAO = 'BAN TIN CANH BAO'


def write_to_json(body, file_url):
    try:
        json_last_trace = json.dumps(body)
        with io.open(file_url, 'wb') as last_trace_file:
            last_trace_file.write(json_last_trace)
        LOGGER.info('Command information just send: %s', body)
    except Exception as ex:
        LOGGER.error('Error at write_to_json function with message: %s', ex.message)


def read_to_json(fileUrl):
    try:
        json_file = open(fileUrl, )
        json_info = json.load(json_file)
    except Exception as ex:
        LOGGER.error('Error at call function in read_to_json with message: %s', ex.message)
    return json_info


def check_alarm():
    try:
        tel_lcd = read_to_json('./latest_telemetry.json')
        all_row = read_to_json('./last_cmd_alarm.json')
        row1 = all_row['row1']
        row2 = all_row['row2']
        row3 = all_row['row3']
        if row1 != BAN_TIN_CANH_BAO:
            cmd_lcd[UPDATE_VALUE] = create_cmd_multi(BAN_TIN_CANH_BAO, ROW_1)
            row1 = BAN_TIN_CANH_BAO
            LOGGER.info('Log in row 1 success: %s', row1)
        row2 = get_alarm(row2, tel_lcd)
        row3 = get_time_alarm(row3)
        # max_tem = shared_attributes.get('acmExpectedTemp', default_data.acmExpectedTemp)
        # LOGGER.info('MAX TEMPERATURE: %s', str(max_tem))
        body = {"row1": row1, "row2": row2, "row3": row3}
        write_to_json(body, './last_cmd_alarm.json')
    except Exception as ex:
        LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)


def get_alarm(row2, tel_lcd):
    try:
        if tel_lcd:
            if (CB_CHAY in tel_lcd) and tel_lcd.get(CB_CHAY) == 1:
                row2 = create_for_each('CB Chay!', row2)
            elif (CB_KHOI in tel_lcd) and tel_lcd.get(CB_KHOI) == 1:
                row2 = create_for_each('CB Khoi!', row2)
            # elif tel_lcd.get('acmTempIndoor') > max_tem:
            #     row2_3 = self.create_for_each('CB Nhiet!', dt_string, row2_3)
            elif (CB_NGAP in tel_lcd) and tel_lcd.get(CB_NGAP) == 1:
                row2 = create_for_each('CB Ngap!', row2)
            elif (CB_CUA in tel_lcd) and tel_lcd.get(CB_CUA) == 1:
                row2 = create_for_each('CB Cua!', row2)
            else:
                row2 = create_for_each('An Toan!', row2)
    except Exception as ex:
        LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)
    return row2


def get_time_alarm(row):
    try:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M")
        show = str(dt_string) + SALT_DOLLAR_SIGN + str(ROW_2) + END_CMD
        if show != row:
            cmd_lcd[UPDATE_VALUE] = show
            LOGGER.info('TIME TO ALARM: %s', str(show))
            row = show
    except Exception as ex:
        LOGGER.error('Error at call function in check_key_code with message: %s', ex.message)
    return row


def create_for_each(string, row_str):
    try:
        el1 = create_cmd_multi(string, ROW_2)
        if el1 != row_str:
            cmd_lcd[UPDATE_VALUE] = el1
            LOGGER.info('ALarm in line 2 -3 in create_for_each : %s', el1)
            row_str = el1
        return row_str
    except Exception as ex:
        LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)


def create_cmd_multi(str_show, row):
    return str(str_show) + SALT_DOLLAR_SIGN + str(row) + END_CMD

# class alarm_lcd_service:
#
#     def __init__(self):
#         pass
#
#     def check_alarm(self, tel_lcd):
#         now = datetime.now()
#         dt_string = now.strftime("%d/%m/%Y %H:%M")
#         try:
#             json_file = open('./last_cmd_alarm.json', )
#             all_row = json.load(json_file)
#             row1 = all_row['row1']
#             row2_3 = all_row['row2_3']
#
#             if row1 != BAN_TIN_CANH_BAO:
#                 cmd_lcd[UPDATE_VALUE] = self.create_cmd_multi(BAN_TIN_CANH_BAO, ROW_1)
#                 row1 = BAN_TIN_CANH_BAO
#                 LOGGER.info('Log in row 1 success: %s', row1)
#
#             # max_tem = shared_attributes.get('acmExpectedTemp', default_data.acmExpectedTemp)
#             # LOGGER.info('MAX TEMPERATURE: %s', str(max_tem))
#             if tel_lcd:
#                 if tel_lcd.get('mccFireState') == 1:
#                     row2_3 = self.create_for_each('CB Chay!', dt_string, row2_3)
#                 elif tel_lcd.get('mccSmokeState') == 1:
#                     row2_3 = self.create_for_each('CB Khoi!', dt_string, row2_3)
#                 # elif tel_lcd.get('acmTempIndoor') > max_tem:
#                 #     row2_3 = self.create_for_each('CB Nhiet!', dt_string, row2_3)
#                 elif tel_lcd.get('mccFloodState') == 1:
#                     row2_3 = self.create_for_each('CB Ngap!', dt_string, row2_3)
#                 elif tel_lcd.get('mccDoorState') == 1:
#                     row2_3 = self.create_for_each('CB Cua!', dt_string, row2_3)
#                 else:
#                     row2_3 = self.create_for_each('An Toan!', '', row2_3)
#             body = {"row1": row1, "row2_3": row2_3}
#             write_to_json(body, './last_cmd_alarm.json')
#         except Exception as ex:
#             LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)
#
#     def create_for_each(self, string1, string2, row2_3):
#         try:
#             el1 = self.create_cmd_multi(string1, ROW_2)
#             el1 += self.create_cmd_multi(string2, ROW_3)
#             if el1 != row2_3:
#                 cmd_lcd[UPDATE_VALUE] = el1
#                 LOGGER.info('ALarm in line 2 -3 in create_for_each : %s', el1)
#                 row2_3 = el1
#             return row2_3
#         except Exception as ex:
#             LOGGER.error('Error at call function in menu_thread with message: %s', ex.message)
#
#     def create_cmd_multi(self, str_show, row):
#         return str(str_show) + SALT_DOLLAR_SIGN + str(row) + END_CMD
