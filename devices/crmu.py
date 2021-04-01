from utility import bytes_to_int
from .utils import _read_attribute
 
 # fixed crmu to 13 byte
def extract(byte_data):
    card_id = byte_data[0:12].encode('hex')
    door_state = bytes_to_int(byte_data[12])

    online_status = bytes_to_int(byte_data[13])

    _read_attribute('crmuCardId', card_id)
    _read_attribute('crmuDoorState', door_state)

    _read_attribute('crmuOnlineStatus', online_status)