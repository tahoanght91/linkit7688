from .utils import _read_attribute


def extract(byte_data):
    card_id = byte_data[0:12].encode('hex')
    _read_attribute('crmuCardId', card_id)
