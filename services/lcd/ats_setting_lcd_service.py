# coding=utf-8
from config import *
from config.common import UPDATE_VALUE
from config.common_lcd_services import *

# from operate.lcd_thread import write_body_send_shared_attributes, send_shared_attributes

# Cấu trúc body gửi api lên service khi confirm ok
ats_body_setting = {"atsGenDeactivateMode": 0, "atsGenInactiveStartTime": 0, "atsGenInactiveEndTime": 0}
ats_body_setting_tmp = {"atsGenDeactivateMode": 0, "atsGenInactiveStartTime": 0, "atsGenInactiveEndTime": 0}

# Mặc định vào màn hình đầu tiên id = 0, con trỏ dòng đầu của selection
screen_idx = 0
pointer_idx = -1
time = [-1, -1]

# Thông tin tên id của từng màn hình
screens_info = {"ats_setting": 0, "atsGenDeactivateMode": 1, "atsGenInactiveStartTime": 2,
                "atsGenInactiveEndTime": 3, "confirmDeactivateMode": 4,
                "confirmInactiveStartTime": 5, "confirmInactiveEndTime": 6}


# Màn hình chính được call ở menu
def call_screen_ats_setting(p_idx):
    from control import process_cmd_lcd
    global pointer_idx
    try:
        pointer_idx = p_idx
        switcher = [
            {
                "row_2": '> Cam chay M.Phat',
                "row_3": 'T.gian cam 1',
                "row_4": 'T.gian cam 2'
            },
            {
                "row_2": 'Cam chay M.Phat',
                "row_3": '> T.gian cam 1',
                "row_4": 'T.gian cam 2'
            },
            {
                "row_2": 'Cam chay M.Phat',
                "row_3": 'T.gian cam 1',
                "row_4": '> T.gian cam 2'
            }
        ]
        LOGGER.info('Enter call_screen_ats_setting function: %s', str(switcher[p_idx]))
        # Update text
        process_cmd_lcd(ROW_1, UPDATE_VALUE, 'THIET BI ATS')
        process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[p_idx]['row_2'])
        process_cmd_lcd(ROW_3, UPDATE_VALUE, switcher[p_idx]['row_3'])
        process_cmd_lcd(ROW_4, UPDATE_VALUE, switcher[p_idx]['row_4'])
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)


# Màn hình chọn khi chọn cấm chạy máy phát
def call_screen_deactivate_mode(p_idx):
    global pointer_idx
    from control import process_cmd_lcd
    try:
        pointer_idx = p_idx
        switcher = [
            {
                "row_2": '> Cam chay',
                "row_3": 'Khong cam chay'
            },
            {
                "row_2": 'Cam chay',
                "row_3": '> Khong cam chay'
            }
        ]
        LOGGER.info('Enter call_screen_deactivate_mode function: %s', str(switcher[p_idx]))
        # Update text
        process_cmd_lcd(ROW_1, UPDATE_VALUE, 'THIET BI ATS')
        process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[p_idx]['row_2'])
        process_cmd_lcd(ROW_3, UPDATE_VALUE, switcher[p_idx]['row_3'])
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)


# Màn hình xác nhận
def call_screen_confirm(p_idx):
    global pointer_idx
    from control import process_cmd_lcd
    try:
        pointer_idx = p_idx
        switcher = [
            {
                "row_2": '> Co',
                "row_3": 'Khong'
            },
            {
                "row_2": 'Co',
                "row_3": '> Khong'
            }
        ]
        LOGGER.info('Enter call_screen_confirm function: %s', str(switcher[p_idx]))
        # Update text
        process_cmd_lcd(ROW_1, UPDATE_VALUE, 'XAC NHAN LUU')
        process_cmd_lcd(ROW_2, UPDATE_VALUE, switcher[p_idx]['row_2'])
        process_cmd_lcd(ROW_3, UPDATE_VALUE, switcher[p_idx]['row_3'])
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)


# Màn hình thiet lap thoi gian cam
def call_screen_inactivate_time(p_idx, isStart):
    global pointer_idx
    from control import process_cmd_lcd
    try:
        pointer_idx = p_idx
        if isStart == 1:
            time_idx = 1
        else:
            time_idx = 2

        hour = get_string_time()
        process_cmd_lcd(ROW_1, UPDATE_VALUE, 'THIET BI ATS')
        process_cmd_lcd(ROW_2, UPDATE_VALUE, "T.gian cam {0}".format(time_idx))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, hour)
        LOGGER.info('Enter call_screen_inactivate_time function')
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)


def call_screen_with_screen_id(screen_id):
    global screen_idx, pointer_idx ,time
    try:
        LOGGER.info('Enter call_screen_with_screen_id function, screen_id: %s', str(screen_id))
        screen_idx = screen_id
        if screen_id == screens_info["ats_setting"]:
            call_screen_ats_setting(p_idx=0)
        if screen_id == screens_info["atsGenDeactivateMode"]:
            call_screen_deactivate_mode(p_idx=0)
        elif screen_id == screens_info["atsGenInactiveStartTime"]:
            time = [-1, -1]
            call_screen_inactivate_time(p_idx=0, isStart=1)
        elif screen_id == screens_info["atsGenInactiveEndTime"]:
            time = [-1, -1]
            call_screen_inactivate_time(p_idx=0, isStart=0)
        elif screen_id == screens_info["confirmDeactivateMode"] or screen_id == screens_info[
            "confirmInactiveStartTime"] or screen_id == screens_info["confirmInactiveEndTime"]:
            call_screen_confirm(p_idx=0)
    except Exception as ex:
        LOGGER.error('Error at call function in screen_assign_ip_address with message: %s', ex.message)


# Register func nay
def listen_key_code(keycode):
    global screen_idx
    try:
        LOGGER.info('Enter listen_key_code function, screen_idx: %s, keycode: %s', str(screen_idx), str(keycode))
        if screen_idx == screens_info["ats_setting"]:
            ats_setting_listen_key(keycode)
        elif screen_idx == screens_info["atsGenDeactivateMode"]:
            ats_deactivate_mode_listen_key(keycode)
        elif screen_idx == screens_info["atsGenInactiveStartTime"]:
            ats_inactive_time_listen_key(keycode, isStart=1)
        elif screen_idx == screens_info["atsGenInactiveEndTime"]:
            ats_inactive_time_listen_key(keycode, isStart=0)
        elif screen_idx == screens_info["confirmInactiveStartTime"] or screen_idx == screens_info[
            "confirmInactiveEndTime"] or screen_idx == screens_info["confirmDeactivateMode"]:
            confirm_listen_key(keycode)
        else:
            return
    except Exception as ex:
        LOGGER.error('Error at call function listen_key_code with message: %s', ex.message)


def ats_setting_listen_key(keycode):
    global screen_idx, pointer_idx
    try:
        LOGGER.info('Enter ats_setting_listen_key function, keycode: %s', str(keycode))
        if keycode == BUTTON_34_EVENT_UP:
            # down
            if pointer_idx == 2:
                pointer_idx = 2
            else:
                pointer_idx = pointer_idx + 1
            call_screen_ats_setting(pointer_idx)

        elif keycode == BUTTON_14_EVENT_UP:
            # up
            if pointer_idx < 0:
                pointer_idx = 0
            else:
                pointer_idx = pointer_idx - 1
            call_screen_ats_setting(pointer_idx)

        elif keycode == BUTTON_24_EVENT_UP:
            # ok
            if pointer_idx == -1:
                call_screen_with_screen_id(pointer_idx + 1)
                pointer_idx = 0
            else:
                call_screen_with_screen_id(pointer_idx + 1)
        else:
            pass
    except Exception as ex:
        LOGGER.error('Error at call function ats_setting_listen_key with message: %s', ex.message)


def ats_deactivate_mode_listen_key(keycode):
    global screen_idx, pointer_idx
    try:
        LOGGER.info('Enter ats_deactivate_mode_listen_key function, keycode: %s', str(keycode))
        if keycode == BUTTON_34_EVENT_UP:
            # down
            if pointer_idx == 1:
                pointer_idx = 1
            else:
                pointer_idx = pointer_idx + 1
            call_screen_deactivate_mode(pointer_idx)

        elif keycode == BUTTON_14_EVENT_UP:
            # up
            if pointer_idx == 0:
                pointer_idx = 0
            else:
                pointer_idx = pointer_idx - 1
            call_screen_deactivate_mode(pointer_idx)

        elif keycode == BUTTON_24_EVENT_UP:
            # ok
            if pointer_idx == 0:
                ats_body_setting_tmp["atsGenDeactivateMode"] = 1
                call_screen_with_screen_id(screens_info["confirmDeactivateMode"])
            else:
                ats_body_setting_tmp["atsGenDeactivateMode"] = 0
                call_screen_with_screen_id(screens_info["confirmDeactivateMode"])

        else:
            pass
    except Exception as ex:
        LOGGER.error('Error at call function ats_deactivate_mode_listen_key with message: %s', ex.message)


def ats_inactive_time_listen_key(keycode, isStart):
    global time, pointer_idx
    try:
        LOGGER.info('Enter ats_inactive_time_listen_key function, isStart: %s', str(isStart))

        if keycode == BUTTON_34_EVENT_UP:
            # down
            if time[pointer_idx] < 0:
                time[pointer_idx] = 0
            else:
                time[pointer_idx] = time[pointer_idx] - 1

            call_screen_inactivate_time(pointer_idx, isStart)

        elif keycode == BUTTON_14_EVENT_UP:
            # up
            if time[pointer_idx] == 9:
                time[pointer_idx] = 9
            else:
                time[pointer_idx] = time[pointer_idx] + 1
            call_screen_inactivate_time(pointer_idx, isStart)
        elif keycode == BUTTON_23_EVENT_UP:
            # key left
            if pointer_idx == 0:
                pointer_idx = 0
            else:
                pointer_idx = pointer_idx - 1

            time[pointer_idx] = -1
            call_screen_inactivate_time(pointer_idx, isStart)
        elif keycode == BUTTON_25_EVENT_UP:
            # key right
            if pointer_idx == 1:
                pointer_idx = 1
            else:
                pointer_idx = pointer_idx + 1
            #
            time[pointer_idx] = -1
            call_screen_inactivate_time(pointer_idx, isStart)
        elif keycode == BUTTON_24_EVENT_UP:
            # ok
            if isStart:
                call_screen_with_screen_id(screens_info["confirmInactiveStartTime"])
                if "_" not in get_string_time():
                    ats_body_setting_tmp["atsGenInactiveStartTime"] = get_string_time()
            else:
                call_screen_with_screen_id(screens_info["confirmInactiveEndTime"])
                if "_" not in get_string_time():
                    ats_body_setting_tmp["confirmInactiveEndTime"] = get_string_time()
                return
    except Exception as ex:
        LOGGER.error('Error at call function ats_inactive_time_listen_key with message: %s', ex.message)


def confirm_listen_key(keycode):
    global pointer_idx, ats_body_setting
    try:
        LOGGER.info('Enter confirm_listen_key function, keycode: %s', str(keycode))
        if keycode == BUTTON_34_EVENT_UP:
            # down
            if pointer_idx == 1:
                pointer_idx = 1
            else:
                pointer_idx = pointer_idx + 1
            call_screen_confirm(pointer_idx)

        elif keycode == BUTTON_14_EVENT_UP:
            # up
            if pointer_idx == 0:
                pointer_idx = 0
            else:
                pointer_idx = pointer_idx - 1
            call_screen_confirm(pointer_idx)

        elif keycode == BUTTON_24_EVENT_UP:
            if pointer_idx == 0:
                ats_body_setting = ats_body_setting_tmp

                #     Call api method post to server
                call_api_to_smart_site(ats_body_setting)

            if pointer_idx == 1:
                call_back_ats_setting()
        else:
            pass
    except Exception as ex:
        LOGGER.error('Error at call function in confirm_listen_key with message: %s', ex.message)


def get_string_time():
    global time
    if time[0] == -1:
        hour_idx1 = "_"
    else:
        hour_idx1 = "{0}".format(time[0])

    if time[1] == -1:
        hour_idx2 = "_"
    else:
        hour_idx2 = "{0}".format(time[1])

    hour = "{0}{1}".format(hour_idx1, hour_idx2)
    return hour


def reset_params():
    global ats_body_setting, time, screen_idx, pointer_idx
    try:
        ats_body_setting = {"atsGenDeactivateMode": 0, "atsGenInactiveStartTime": 0, "atsGenInactiveEndTime": 0}
        screen_idx = 0
        pointer_idx = -1
        time = [-1, -1]
    except Exception as ex:
        LOGGER.error('Error at call function in confirm_listen_key with message: %s', ex.message)


# ats_body_setting = {"atsGenDeactivateMode": 0, "atsGenInactiveStartTime": 0, "atsGenInactiveEndTime": 0}
def call_api_to_smart_site(body):
    from operate.lcd_thread import write_body_send_shared_attributes, send_shared_attributes
    try:
        LOGGER.info('Enter confirm_listen_key function')
        if screen_idx == screens_info["confirmDeactivateMode"]:
            json_body = write_body_send_shared_attributes("atsGenDeactivateMode", body["atsGenDeactivateMode"])
        elif screen_idx == screens_info["confirmInactiveStartTime"]:
            json_body = write_body_send_shared_attributes("atsGenInactiveStartTime", body["atsGenInactiveStartTime"])
        elif screen_idx == screens_info["confirmInactiveEndTime"]:
            json_body = write_body_send_shared_attributes("atsGenInactiveEndTime", body["atsGenInactiveEndTime"])

        if len(json_body) > 0:
            send_shared_attributes(json_body)
            call_back_ats_setting()
    except Exception as ex:
        LOGGER.error('Error at call function in confirm_listen_key with message: %s', ex.message)


def call_back_ats_setting():
    global screen_idx
    try:
        screen_idx = screens_info["ats_setting"]
        if screen_idx == screens_info["confirmDeactivateMode"]:
            ats_body_setting["atsGenDeactivateMode"] = 0
            call_screen_ats_setting(p_idx=0)
        elif screen_idx == screens_info["confirmInactiveStartTime"]:
            ats_body_setting["atsGenInactiveStartTime"] = 0
            call_screen_ats_setting(p_idx=1)
        elif screen_idx == screens_info["confirmInactiveEndTime"]:
            ats_body_setting["atsGenInactiveEndTime"] = 0
            call_screen_ats_setting(p_idx=2)

    except Exception as ex:
        LOGGER.error('Error at call function in call_back_ats_setting with message: %s', ex.message)
