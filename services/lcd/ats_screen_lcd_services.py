from config import *
from config.common import UPDATE_VALUE
from config.common_lcd_services import *


def get_title_ats():
    from control import process_cmd_lcd
    try:
        show = 'THONG TIN ATS'
        process_cmd_lcd(ROW_1, UPDATE_VALUE, show)
    except Exception as ex:
        LOGGER.error('Error at get_title_ats function with message: %s', ex.message)


def get_info_ats():
    from control import process_cmd_lcd
    try:
        infor_ats = client_attributes
        status = 'Ket noi' if infor_ats.get('atsConnect') > 0 else 'Mat ket noi'
        resource = 'May phat' if infor_ats.get('atsContactorGenState') > 0 else 'Dien luoi'
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(status))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, 'Nguon: ' + str(resource))
    except Exception as ex:
        LOGGER.error('Error at get_info_ats function with message: %s', ex.message)


def get_detail_ats():
    row2 = ''
    row3 = ''
    row4 = ''
    from control import process_cmd_lcd
    try:
        detail = telemetries
        status = client_attributes
        row2 = 'Mat ket noi'
        row3 = 'Mat ket noi'
        row4 = 'Mat ket noi'
        if status.get('atsConnect') == 1:
            if status.get('atsContactorGenState') == 1:
                row2 = str(detail.get('atsVgenP1')) + str(detail.get('atsVgenP2')) + str(detail.get('atsVgenP3'))
            else:
                row2 = str(detail.get('atsVacP1')) + str(detail.get('atsVacP2')) + str(detail.get('atsVacP3'))
            row3 = str(detail.get('atsVloadP1')) + str(detail.get('atsVloadP2')) + str(detail.get('atsVloadP3'))
            row4 = str(detail.get('atsIloadP1')) + str(detail.get('atsIloadP2')) + str(detail.get('atsIloadP3'))
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
    except Exception as ex:
        LOGGER.error('Error at get_detail_ats function with message: %s', ex.message)


def get_screen_ats():
    try:
        get_title_ats()
        get_info_ats()
    except Exception as ex:
        LOGGER.error('Error at get_screen_ats function with message: %s', ex.message)
