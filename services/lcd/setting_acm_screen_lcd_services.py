"""---------------------------------------------------------------------------------------------------------------------
                                                    Include
   ------------------------------------------------------------------------------------------------------------------"""
from config import LOGGER
from config.common import UPDATE_VALUE
from config.common_lcd_services import *

"""---------------------------------------------------------------------------------------------------------------------
                                                    Define 
   ------------------------------------------------------------------------------------------------------------------"""
acm_setting_list_screen_l = [
    {
        'row_1': 'CAI DAT DIEU HOA',
        'row_2': '> Che do',
        'row_3': 'T1',
        'row_4': 'T2'
    },
    {
        'row_1': 'CAI DAT DIEU HOA',
        'row_2': 'Che do',
        'row_3': '> T1',
        'row_4': 'T2'
    },
    {
        'row_1': 'CAI DAT DIEU HOA',
        'row_2': 'Che do',
        'row_3': 'T1',
        'row_4': '> T2'
    },
    {
        'row_1': 'CAI DAT DIEU HOA',
        'row_2': '> T3',
        'row_3': 'T4',
        'row_4': ' '
    },
    {
        'row_1': 'CAI DAT DIEU HOA',
        'row_2': 'T3',
        'row_3': '> T4',
        'row_4': ' '
    },
]

acm_setting_mode_screen_l = [
    {
        'row_1': 'CAI DAT DIEU HOA',
        'row_2': '> Tu dong',
        'row_3': 'Thu cong',
        'row_4': ' '
    },
    {
        'row_1': 'CAI DAT DIEU HOA',
        'row_2': 'Tu dong',
        'row_3': '> Thu cong',
        'row_4': ' '
    }
]

acm_setting_temp_setting_screen_l = [
    {
        'row_1': 'CAI DAT DIEU HOA',
        'row_2': 'T1',
        'row_3': '__',
        'row_4': ' '
    },
    {
        'row_1': 'CAI DAT DIEU HOA',
        'row_2': 'T2',
        'row_3': '__',
        'row_4': ' '
    },
    {
        'row_1': 'CAI DAT DIEU HOA',
        'row_2': 'T3',
        'row_3': '__',
        'row_4': ' '
    },
    {
        'row_1': 'CAI DAT DIEU HOA',
        'row_2': 'T4',
        'row_3': '__',
        'row_4': ' '
    }
]

acm_setting_confirm_screen_l = [
    {
        'row_1': 'XAC NHAN LUU',
        'row_2': '> Co',
        'row_3': 'Khong',
        'row_4': ' '
    },
    {
        'row_1': 'XAC NHAN LUU',
        'row_2': 'Co',
        'row_3': '> Khong',
        'row_4': ' '
    }
]

acm_setting_screen_l = [acm_setting_list_screen_l,
                        acm_setting_mode_screen_l,
                        acm_setting_temp_setting_screen_l,
                        acm_setting_confirm_screen_l]

NOT_GO_CONFIRM = False
GO_CONFIRM = True


"""---------------------------------------------------------------------------------------------------------------------
                                                Global variable
   ------------------------------------------------------------------------------------------------------------------"""
first_access_flag = True
screen_level = 0
index_pointer = 0
confirm_ok = False
setting_level = 0
temp_value = [['_', '_'], ['_', '_'], ['_', '_'], ['_', '_']]
temp_value_count = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
temp_index = 0
temp_number_index = 0
set_temp = 0
goto_confirm_screen_flag = False


"""---------------------------------------------------------------------------------------------------------------------
                                                Internal function
   ------------------------------------------------------------------------------------------------------------------"""
def acm_setting_print_static_lcd(screen_level_type, screen_index):
    from control import process_cmd_lcd
    global temp_value, set_temp, screen_level, acm_setting_screen_l

    screen = acm_setting_screen_l[screen_level_type]
    process_cmd_lcd(ROW_1, UPDATE_VALUE, screen[screen_index]['row_1'])
    process_cmd_lcd(ROW_2, UPDATE_VALUE, screen[screen_index]['row_2'])
    if screen_level == 2:
        set_temp = ''.join(temp_value[screen_index])
        process_cmd_lcd(ROW_3, UPDATE_VALUE, set_temp)
    else:
        process_cmd_lcd(ROW_3, UPDATE_VALUE, screen[screen_index]['row_3'])
    process_cmd_lcd(ROW_4, UPDATE_VALUE, screen[screen_index]['row_4'])


def acm_setting_button(button):
    global screen_level, index_pointer, confirm_ok, setting_level, temp_number_index, temp_value, temp_index, \
        first_access_flag, goto_confirm_screen_flag

    if first_access_flag is True and button == OK:
        first_access_flag = False
        return
    screen_level_internal = screen_level
    if screen_level_internal == 0:
        if button == UP:
            index_pointer -= 1
            if index_pointer > 4:
                index_pointer = 4
        elif button == DOWN:
            index_pointer += 1
            if index_pointer > 4:
                index_pointer = 4
        elif button == RIGHT:
            if index_pointer < 3:
                index_pointer = 3
        elif button == LEFT:
            if index_pointer >= 3:
                index_pointer = 0
        elif button == OK:
            setting_level = index_pointer
            if index_pointer == 0:
                screen_level = 1
            else:
                screen_level = 2
                index_pointer = index_pointer - 1
                temp_index = index_pointer
    elif screen_level_internal == 1:
        if button == UP:
            index_pointer = 0
        elif button == DOWN:
            index_pointer = 1
        elif button == OK:
            screen_level = 3
            index_pointer = 0
    elif screen_level_internal == 2:
        if button == UP:
            temp_value_count[temp_index][temp_number_index] += 1
            if temp_value_count[temp_index][temp_number_index] > 9:
                temp_value_count[temp_index][temp_number_index] = 0
            temp_value[temp_index][temp_number_index] = str(temp_value_count[temp_index][temp_number_index])
        elif button == DOWN:
            temp_value_count[temp_index][temp_number_index] -= 1
            if temp_value_count[temp_index][temp_number_index] < 0:
                temp_value_count[temp_index][temp_number_index] = 9
            temp_value[temp_index][temp_number_index] = str(temp_value_count[temp_index][temp_number_index])
        elif button == LEFT:
            temp_number_index = 0
        elif button == RIGHT and temp_value[temp_index][0] != '_':
            temp_number_index = 1
        elif button == OK and temp_value[temp_index][1] != '_':
            screen_level = 3
            index_pointer = 0
    elif screen_level_internal == 3:
        if button == UP:
            index_pointer = 0
        elif button == DOWN:
            index_pointer = 1
        elif button == OK:
            goto_confirm_screen_flag = True
            if index_pointer == 0:
                confirm_ok = True


def acm_setting_mode_control(mode):
    from operate.lcd_thread import write_body_send_shared_attributes, send_shared_attributes
    body = write_body_send_shared_attributes("acmControlAuto", mode)
    send_shared_attributes(body)


def acm_setting_temp(key_index, value):
    from operate.lcd_thread import write_body_send_shared_attributes, send_shared_attributes

    key = ["acmT1Temp", "acmT2Temp", "acmT3Temp", "acmT4Temp"]
    body = write_body_send_shared_attributes(key[key_index], value)
    send_shared_attributes(body)


def acm_setting_set_default_value():
    global first_access_flag, screen_level, index_pointer, confirm_ok, setting_level, temp_value, \
        temp_number_index, temp_index, set_temp, temp_value_count, goto_confirm_screen_flag

    first_access_flag = True
    screen_level = 0
    index_pointer = 0
    confirm_ok = False
    setting_level = 0
    temp_value = [['_', '_'], ['_', '_'], ['_', '_'], ['_', '_']]
    temp_value_count = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
    temp_index = 0
    temp_number_index = 0
    set_temp = 0
    goto_confirm_screen_flag = False


"""---------------------------------------------------------------------------------------------------------------------
                                                 External function
   ------------------------------------------------------------------------------------------------------------------"""
def acm_setting(button):
    global screen_level, index_pointer, confirm_ok, setting_level, set_temp, goto_confirm_screen_flag

    try:
        ret = NOT_GO_CONFIRM
        acm_setting_button(button)
        if confirm_ok is False:
            acm_setting_print_static_lcd(screen_level, index_pointer)
        else:
            if setting_level == 0:
                acm_setting_mode_control(index_pointer ^ 1)
            else:
                acm_setting_temp(setting_level - 1, int(set_temp))
        if goto_confirm_screen_flag is True:
            ret = GO_CONFIRM

        return ret
    except Exception as ex:
        LOGGER.error('Error at call function in acm_setting with message: %s', ex.message)
