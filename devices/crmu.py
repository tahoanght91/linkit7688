from config import LOGGER
from .utils import _read_attribute


def extract(byte_data):
    mccRfidCard = byte_data[0:17].encode('hex')
    LOGGER.info('Card is: %s', mccRfidCard)
    _read_attribute('mccRfidCard', str(mccRfidCard))
