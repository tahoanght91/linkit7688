from config import *
from config.common_lcd_services import *
from services import lcd_cmd


class AtsDisplay:
    def __init__(self):
        self.is_connect = 0
        self.ats_generator_stt = 0
        self.ats_power_network_stt = 0

        self.ats_vac = [0, 0, 0]
        self.ats_vgen = [0, 0, 0]
        self.ats_vload = [0, 0, 0]
        self.ats_iload = [0, 0, 0]

        # self.is_connect_previous = 0
        # self.electricity_supply_previous = 0
        #
        # self.ats_vac_previous = [0, 0, 0]
        # self.ats_vgen_previous = [0, 0, 0]
        # self.ats_vload_previous = [0, 0, 0]
        # self.ats_iload_previous = [0, 0, 0]

    def header(self):
        lcd_cmd.print_lcd('THONG TIN ATS', ROW_1)

    def disconnect_display(self):
        if self.is_connect == 0:
            lcd_cmd.print_lcd('Mat ket noi', ROW_2)

    def display1(self):
        try:
            if self.get_state():
                self.header()
                if self.is_connect:
                    lcd_cmd.print_lcd('Ket noi', ROW_2)
                    if self.ats_generator_stt:
                        lcd_cmd.print_lcd('Nguon: Dien luoi', ROW_3)
                        LOGGER.info('ATS is connecting, power supply: Electric network')
                    elif self.ats_power_network_stt:
                        lcd_cmd.print_lcd('Nguon: May phat', ROW_3)
                        LOGGER.info('ATS is connecting, power supply: Power generator')
                else:
                    self.header()
                    lcd_cmd.clear_display()
                    self.disconnect_display()
                    LOGGER.info('ATS disconnected')
        except Exception as ex:
            LOGGER.info('display1 function error: %s', ex.message)

    def display2(self):
        try:
            if self.get_values_ats() and self.get_state():
                if self.is_connect:
                    if self.ats_power_network_stt:
                        string_row2 = '{p1}V {p2}V {p3}V'.format(p1=self.ats_vac[0], p2=self.ats_vac[1],
                                                                 p3=self.ats_vac[2])
                    else:
                        string_row2 = '{p1}V {p2}V {p3}V'.format(p1=self.ats_vgen[0], p2=self.ats_vgen[1],
                                                                 p3=self.ats_vgen[2])
                    lcd_cmd.print_lcd(string_row2, ROW_2)
                else:
                    self.header()
                    lcd_cmd.clear_display()
                    self.disconnect_display()
                lcd_cmd.print_lcd('Ket noi', ROW_2)
                string_row3 = '{p1}V {p2}V {p3}V'.format(p1=self.ats_vload[0], p2=self.ats_vload[1],
                                                         p3=self.ats_vload[2])

                string_row4 = '{p1}A {p2}A {p3}A'.format(p1=self.ats_iload[0], p2=self.ats_iload[1],
                                                         p3=self.ats_iload[2])
                lcd_cmd.print_lcd(string_row3, ROW_3)
                lcd_cmd.print_lcd(string_row4, ROW_4)
        except Exception as ex:
            LOGGER.info('display2 function error: %s', ex.message)

    def get_state(self):
        try:
            if update_attributes:
                # read status ats
                self.is_connect = update_attributes['atsConnect']
                self.ats_generator_stt = update_attributes['atsContactorGenState']
                self.ats_power_network_stt = update_attributes['atsContactorElecState']
                LOGGER.info('Get information form ats: state')
                return True
            else:
                return False
        except Exception as ex:
            LOGGER.info('get_state function error: %s', ex.message)

    def get_values_ats(self):
        try:
            if telemetries:
                # read vol ampe
                self.ats_vac = [telemetries['atsVacP1'], telemetries['atsVacP2'], telemetries['atsVacP3']]
                self.ats_vgen = [telemetries['atsVgenP1'], telemetries['atsVgenP2'], telemetries['atsVgenP3']]
                self.ats_vload = [telemetries['atsVloadP1'], telemetries['atsVloadP2'], telemetries['atsVloadP3']]
                self.ats_iload = [telemetries['atsIloadP1'], telemetries['atsIloadP2'], telemetries['atsIloadP3']]
                LOGGER.info('Get information form ats: vol ampe value')
                return True
            else:
                return False
        except Exception as ex:
            LOGGER.info('get_values_ats function error: %s', ex.message)
