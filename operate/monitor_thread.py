import time

from config import *
from monitor import *

def call():
    period = shared_attributes.get('periodUpdate', default_data.periodUpdate)
    while True:
        bell.apply()
        if shared_attributes.get('atsControlAuto', default_data.atsControlAuto):
            ats.apply()
        if shared_attributes.get('miscFanControlAuto', default_data.miscFanControlAuto):
            fan.apply()
        if shared_attributes.get('aircControlAuto', default_data.aircControlAuto):
            airc.apply()
        if shared_attributes.get('crmuControlAuto', default_data.crmuControlAuto):
            crmu.apply()
        time.sleep(period)
