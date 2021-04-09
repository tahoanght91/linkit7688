import io
import json
import logging
import threading

from . import default_data
import mqtt

with io.open('./config/devices.json', encoding='utf8') as f:
    device_config = json.load(f)
LOGGER = logging.getLogger('App')
BYTE_ORDER = 'little'
HOST = device_config['host']
ACCESS_TOKEN = device_config['access_token']
CLIENT_ID = device_config['device_id']
# CLIENT = mqtt.TBDeviceMqttClient(host=HOST, token=ACCESS_TOKEN, client_id=CLIENT_ID)
CLIENT = mqtt.TBGatewayMqttClient(host=HOST, port=1883, token=ACCESS_TOKEN, gateway="gateway_python_001")
IO_PORT = '/dev/ttyS0'
BAUDRATE = 115200
UPDATE_PERIOD = 7 * 24 * 60 * 60
READ_PER_WRITE = 20

shared_attributes = {}
client_attributes = {}
update_attributes = {}
telemetries = {}
commands = {}

telemetries['miscTemp'] = 0
telemetries['miscHumid'] = 0
telemetries['aircTemp'] = 0
telemetries['aircHumid'] = 0
telemetries['aircAirc1Temp'] = 0
telemetries['aircAirc2Temp'] = 0
telemetries['aircOutdoorTemp'] = 0
telemetries['atsVacP1'] = 0
telemetries['atsVacP2'] = 0
telemetries['atsVacP3'] = 0
telemetries['atsVacFreq'] = 0
telemetries['atsVgenP1'] = 0
telemetries['atsVgenP2'] = 0
telemetries['atsVgenP3'] = 0
telemetries['atsVgenFreq'] = 0
telemetries['atsVloadP1'] = 0
telemetries['atsVloadP2'] = 0
telemetries['atsVloadP3'] = 0
telemetries['atsVloadFreq'] = 0
telemetries['atsIloadP1'] = 0
telemetries['atsIloadP2'] = 0
telemetries['atsIloadP3'] = 0
telemetries['atsGscOil'] = 0
telemetries['atsGscCoolantTemp'] = 0
telemetries['atsGscFuel'] = 0
telemetries['atsGscVbat'] = 0
telemetries['atsGscSpeed'] = 0
telemetries['atsGscPowerTotal'] = 0
telemetries['atsGscPower1'] = 0
telemetries['atsGscPower2'] = 0
telemetries['atsGscPower3'] = 0
telemetries['atsGscKvaTotal'] = 0
telemetries['atsGscKva1'] = 0
telemetries['atsGscKva2'] = 0
telemetries['atsGscKva3'] = 0
telemetries['atsGscRunHoursCounter'] = 0
telemetries['atsGscCrankCounter'] = 0
telemetries['atuAtu1X'] = 0
telemetries['atuAtu1Y'] = 0
telemetries['atuAtu1Z'] = 0
telemetries['atuAtu2X'] = 0
telemetries['atuAtu2Y'] = 0
telemetries['atuAtu2Z'] = 0
telemetries['atuAtu3X'] = 0
telemetries['atuAtu3Y'] = 0
telemetries['atuAtu3Z'] = 0
telemetries['dcVdc'] = 0
telemetries['dcIbat1'] = 0
telemetries['dcBat1Temp'] = 0
telemetries['dcVbat1Div2'] = 0
telemetries['dcIbat2'] = 0
telemetries['dcBat2Temp'] = 0
telemetries['dcVbat2Div2'] = 0
telemetries['dcIbat3'] = 0
telemetries['dcBat3Temp'] = 0
telemetries['dcVbat3Div2'] = 0
telemetries['dcIbat4'] = 0
telemetries['dcBat4Temp'] = 0
telemetries['dcVbat4Div2'] = 0

update_attributes_lock = threading.Lock()
telemetries_lock = threading.Lock()
commands_lock = threading.Lock()
