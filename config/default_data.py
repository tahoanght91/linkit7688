import io
import os
import json

if not os.path.exists('./config/data.json'):
    os.system('cp ./config/factory_data.json ./config/data.json')

with io.open('./config/data.json', encoding='utf8') as f:
    data_dict = json.load(f)
    globals().update(data_dict['shared'])
    globals().update(data_dict['client'])
    globals().update(data_dict['telemetry'])
    shared_keys = [x for x in data_dict['shared']]
    client_keys = [x for x in data_dict['client']]
    telemetry_keys = [x for x in data_dict['telemetry']]
