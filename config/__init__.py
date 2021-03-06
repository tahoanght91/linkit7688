import io
import json
import logging
import threading

from . import default_data
import mqtt

with io.open('./config/devices.json', encoding = 'utf8') as f:
    device_config = json.load(f)
LOGGER = logging.getLogger('App')
BYTE_ORDER = 'little'
HOST = device_config['host']
ACCESS_TOKEN = device_config['access_token']
CLIENT_ID = device_config['device_id']
CLIENT = mqtt.TBDeviceMqttClient(host = HOST, token = ACCESS_TOKEN, client_id = CLIENT_ID)
IO_PORT = '/dev/ttyS0'
BAUDRATE = 115200
UPDATE_PERIOD = 7 * 24 * 60 * 60
READ_PER_WRITE = 20

shared_attributes = {}
client_attributes = {}
update_attributes = {}
telemetries = {}
commands = {}

update_attributes_lock = threading.Lock()
telemetries_lock = threading.Lock()
commands_lock = threading.Lock()