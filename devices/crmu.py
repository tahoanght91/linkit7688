from .utils import _read_attribute


def extract(byte_data):
    mccRfidCard = byte_data[0:12].encode('hex')
    _read_attribute('mccRfidCard', mccRfidCard)
