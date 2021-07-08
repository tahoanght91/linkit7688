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
    row2 = ''
    row3 = ''
    row4 = ''
    from control import process_cmd_lcd
    try:
        infor_ats = client_attributes
        row2 = 'Ket noi' if infor_ats.get('atsConnect') > 0 else 'Mat ket noi'
        row3 = 'Nguon: May phat' if infor_ats.get('atsContactorGenState') > 0 else 'Nguon: Dien luoi'
        if telemetries.get('atsState') is not None and telemetries.get('atsState') != '':
            row4 = 'Che do: ' + str(telemetries.get('atsState'))
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
    except Exception as ex:
        LOGGER.error('Error at get_info_ats function with message: %s', ex.message)


def get_detail_screen1_ats():
    row2 = ''
    row3 = ''
    row4 = ''
    from control import process_cmd_lcd
    try:
        if telemetries.get('atsAcState') is not None and telemetries.get('atsAcState') != '':
            row2 = 'Dien luoi: ' + str(telemetries.get('atsAcState'))
        if telemetries.get('atsGenState') is not None and telemetries.get('atsGenState') != '':
            row3 = 'May phat: ' + str(telemetries.get('atsGenState'))
        if telemetries.get('atsState') is not None and telemetries.get('atsState') != '':
            row4 = 'Che do M.Phat: ' + str(telemetries.get('atsState'))
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
    except Exception as ex:
        LOGGER.error('Error at get_detail_ats function with message: %s', ex.message)


def get_detail_screen2_ats():
    row2 = ''
    row3 = ''
    row4 = ''
    atsVacP1 = ''
    atsVacP2 = ''
    atsVacP3 = ''
    atsVgenP1 = ''
    atsVgenP2 = ''
    atsVgenP3 = ''
    atsVloadP1 = ''
    atsVloadP2 = ''
    atsVloadP3 = ''
    from control import process_cmd_lcd
    try:
        if telemetries.get('atsVacP1') is not None and telemetries.get('atsVacP1') != '':
            atsVacP1 = str(telemetries.get('atsVacP1')) + 'V '
        if telemetries.get('atsVacP2') is not None and telemetries.get('atsVacP2') != '':
            atsVacP2 = str(telemetries.get('atsVacP2')) + 'V '
        if telemetries.get('atsVacP3') is not None and telemetries.get('atsVacP3') != '':
            atsVacP3 = str(telemetries.get('atsVacP3')) + 'V'
        row2 = atsVacP1 + atsVacP2 + atsVacP3
        if telemetries.get('atsVgenP1') is not None and telemetries.get('atsVgenP1') != '':
            atsVgenP1 = str(telemetries.get('atsVgenP1')) + 'V '
        if telemetries.get('atsVgenP2') is not None and telemetries.get('atsVgenP2') != '':
            atsVgenP2 = str(telemetries.get('atsVgenP2')) + 'V '
        if telemetries.get('atsVgenP3') is not None and telemetries.get('atsVgenP3') != '':
            atsVgenP3 = str(telemetries.get('atsVgenP3')) + 'V'
        row3 = atsVgenP1 + atsVgenP2 + atsVgenP3
        if telemetries.get('atsVloadP1') is not None and telemetries.get('atsVloadP1') != '':
            atsVloadP1 = str(telemetries.get('atsVloadP1')) + 'V '
        if telemetries.get('atsVloadP2') is not None and telemetries.get('atsVloadP2') != '':
            atsVloadP2 = str(telemetries.get('atsVloadP2')) + 'V '
        if telemetries.get('atsVloadP3') is not None and telemetries.get('atsVloadP3') != '':
            atsVloadP3 = str(telemetries.get('atsVloadP3')) + 'V'
        row4 = atsVloadP1 + atsVloadP2 + atsVloadP3
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
    except Exception as ex:
        LOGGER.error('Error at get_detail_ats function with message: %s', ex.message)


def get_detail_screen3_ats():
    row2 = ''
    row3 = ''
    row4 = ''
    atsIloadP1 = ''
    atsIloadP2 = ''
    atsIloadP3 = ''
    atsPac1 = ''
    atsPac2 = ''
    atsPac3 = ''
    atsVacFreq = ''
    atsVgenFreq = ''
    atsVloadFreq = ''
    from control import process_cmd_lcd
    try:
        if telemetries.get('atsIloadP1') is not None and telemetries.get('atsIloadP1') != '':
            atsIloadP1 = str(telemetries.get('atsIloadP1')) + 'A '
        if telemetries.get('atsIloadP2') is not None and telemetries.get('atsIloadP2') != '':
            atsIloadP2 = str(telemetries.get('atsIloadP2')) + 'A '
        if telemetries.get('atsIloadP3') is not None and telemetries.get('atsIloadP3') != '':
            atsIloadP3 = str(telemetries.get('atsIloadP3')) + 'A'
        row2 = atsIloadP1 + atsIloadP2 + atsIloadP3
        if telemetries.get('atsPac1') is not None and telemetries.get('atsPac1') != '':
            atsPac1 = str(telemetries.get('atsPac1')) + 'W, '
        if telemetries.get('atsPac2') is not None and telemetries.get('atsPac2') != '':
            atsPac2 = str(telemetries.get('atsPac2')) + 'W, '
        if telemetries.get('atsPac3') is not None and telemetries.get('atsPac3') != '':
            atsPac3 = str(telemetries.get('atsPac3')) + 'W'
        row3 = atsPac1 + atsPac2 + atsPac3
        if telemetries.get('atsVacFreq') is not None and telemetries.get('atsVacFreq') != '':
            atsVacFreq = str(telemetries.get('atsVacFreq')) + 'Hz '
        if telemetries.get('atsVgenFreq') is not None and telemetries.get('atsVgenFreq') != '':
            atsVgenFreq = str(telemetries.get('atsVgenFreq')) + 'Hz '
        if telemetries.get('atsVloadFreq') is not None and telemetries.get('atsVloadFreq') != '':
            atsVloadFreq = str(telemetries.get('atsVloadFreq')) + 'Hz'
        row4 = atsVacFreq + atsVgenFreq + atsVloadFreq
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
    except Exception as ex:
        LOGGER.error('Error at get_detail_ats function with message: %s', ex.message)


def get_detail_screen4_ats():
    row2 = ''
    row3 = ''
    row4 = ''
    mccDcBat1Temp = ''
    mccDcBat2Temp = ''
    mccDcBat3Temp = ''
    mccDcV1 = ''
    mccDcI1 = ''
    mccDcP1 = ''
    mccDcV2 = ''
    mccDcI2 = ''
    mccDcP2 = ''
    from control import process_cmd_lcd
    try:
        if telemetries.get('mccDcBat1Temp') is not None and telemetries.get('mccDcBat1Temp') != '':
            mccDcBat1Temp = str(telemetries.get('mccDcBat1Temp')) + 'C '
        if telemetries.get('mccDcBat2Temp') is not None and telemetries.get('mccDcBat2Temp') != '':
            mccDcBat2Temp = str(telemetries.get('mccDcBat2Temp')) + 'C '
        if telemetries.get('mccDcBat3Temp') is not None and telemetries.get('mccDcBat3Temp') != '':
            mccDcBat3Temp = str(telemetries.get('mccDcBat3Temp')) + 'C'
        row2 = mccDcBat1Temp + mccDcBat2Temp + mccDcBat3Temp
        if telemetries.get('mccDcV1') is not None and telemetries.get('mccDcV1') != '':
            mccDcV1 = str(telemetries.get('mccDcV1')) + 'V '
        if telemetries.get('mccDcI1') is not None and telemetries.get('mccDcI1') != '':
            mccDcI1 = str(telemetries.get('mccDcI1')) + 'A '
        if telemetries.get('mccDcP1') is not None and telemetries.get('mccDcP1') != '':
            mccDcP1 = str(telemetries.get('mccDcP1')) + 'W'
        row3 = mccDcV1 + mccDcI1 + mccDcP1
        if telemetries.get('mccDcV2') is not None and telemetries.get('mccDcV2') != '':
            mccDcV2 = str(telemetries.get('mccDcV2')) + 'V '
        if telemetries.get('mccDcI2') is not None and telemetries.get('mccDcI2') != '':
            mccDcI2 = str(telemetries.get('mccDcI2')) + 'A '
        if telemetries.get('mccDcP2') is not None and telemetries.get('mccDcP2') != '':
            mccDcP2 = str(telemetries.get('mccDcP2')) + 'W'
        row4 = mccDcV2 + mccDcI2 + mccDcP2
        process_cmd_lcd(ROW_2, UPDATE_VALUE, str(row2))
        process_cmd_lcd(ROW_3, UPDATE_VALUE, str(row3))
        process_cmd_lcd(ROW_4, UPDATE_VALUE, str(row4))
    except Exception as ex:
        LOGGER.error('Error at get_detail_ats function with message: %s', ex.message)


def get_detail_screen5_ats():
    row2 = ''
    row3 = ''
    row4 = ''
    mccDcV3 = ''
    mccDcI3 = ''
    mccDcP3 = ''
    mccDcV4 = ''
    mccDcI4 = ''
    mccDcP4 = ''
    mccDcV5 = ''
    mccDcI5 = ''
    mccDcP5 = ''
    from control import process_cmd_lcd
    try:
        if telemetries.get('mccDcV3') is not None and telemetries.get('mccDcV3') != '':
            mccDcV3 = str(telemetries.get('mccDcV3')) + 'V '
        if telemetries.get('mccDcI3') is not None and telemetries.get('mccDcI3') != '':
            mccDcI3 = str(telemetries.get('mccDcI3')) + 'A '
        if telemetries.get('mccDcP3') is not None and telemetries.get('mccDcP3') != '':
            mccDcP3 = str(telemetries.get('mccDcP3')) + 'W'
        row2 = mccDcV3 + mccDcI3 + mccDcP3
        if telemetries.get('mccDcV4') is not None and telemetries.get('mccDcV4') != '':
            mccDcV4 = str(telemetries.get('mccDcV4')) + 'V '
        if telemetries.get('mccDcI4') is not None and telemetries.get('mccDcI4') != '':
            mccDcI4 = str(telemetries.get('mccDcI4')) + 'A '
        if telemetries.get('mccDcP4') is not None and telemetries.get('mccDcP4') != '':
            mccDcP4 = str(telemetries.get('mccDcP4')) + 'W'
        row3 = mccDcV4 + mccDcI4 + mccDcP4
        if telemetries.get('mccDcV5') is not None and telemetries.get('mccDcV5') != '':
            mccDcV5 = str(telemetries.get('mccDcV5')) + 'V '
        if telemetries.get('mccDcI5') is not None and telemetries.get('mccDcI5') != '':
            mccDcI5 = str(telemetries.get('mccDcI5')) + 'A '
        if telemetries.get('mccDcP5') is not None and telemetries.get('mccDcP5') != '':
            mccDcP5 = str(telemetries.get('mccDcP5')) + 'W'
        row4 = mccDcV5 + mccDcI5 + mccDcP5
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
