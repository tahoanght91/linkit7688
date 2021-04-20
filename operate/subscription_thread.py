from config import *
import control
from config.common import *


def _attribute_change_callback(result):
    LOGGER.info(result)
    if result is not None:
        log_info = []
        for key, value in result['data'].items():
            shared_attributes[key] = value
        LOGGER.info('\n'.join(log_info))


def _rpc_callback(request_id, request_body):
    LOGGER.info('Received rpc message\n    Id: %s\n    Body: %s', request_id, request_body)
    try:
        params = request_body.get('params')
        method = request_body.get('method')

        if method == 'setAuto':
            if control.process_set_auto(params):
                CLIENT.send_rpc_reply(request_id, 'success')
                LOGGER.info('    Success')
            else:
                CLIENT.send_rpc_reply(request_id, 'failed')
                LOGGER.info('    Malformed message')
        elif method == 'rpcCall':
            if control.check_command(params):
                commands_lock.acquire()
                commands[params['device']] = params['command']
                commands_lock.release()
                CLIENT.send_rpc_reply(request_id, 'success')
                LOGGER.info('    Success')
            else:
                CLIENT.send_rpc_reply(request_id, 'failed')
                LOGGER.info('    Malformed message or manual mode not activated')
        else:
            CLIENT.send_rpc_reply(request_id, 'failed')
            LOGGER.info('    Malformed message')
    except Exception as e:
        CLIENT.send_rpc_reply(request_id, 'failed')
        LOGGER.info('    Unexpected error: %s', str(e))


def _gw_rpc_callback(self, content):
    LOGGER.info('Received rpc message\n    Content: %s\n', content)
    value = ''
    params = ''
    method = content['data']['method']
    device = content['device']
    request_id = content['data']['id']

    if len(content['data']) == 3:
        value = content['data']['params']
        params = {'device': device, 'command': value}
    elif len(content['data']) == 2:
        params = {'device': device, 'command': GET_STATE}

    if AUTO in method:
        if control.process_set_auto(params):
            LOGGER.info('    Success')
        else:
            LOGGER.info('    Malformed message')
    elif CONTROL in method:
        if 'Airc1' in method:
            params = {'device': DEVICE_AIRC_1, 'command': value}
        elif 'Airc2' in method:
            params = {'device': DEVICE_AIRC_2, 'command': value}
        if control.check_command_send_rpc(params):
            commands_lock.acquire()
            commands[params['device']] = params['command']
            commands_lock.release()
            LOGGER.info('    Success')
        else:
            LOGGER.info('    Malformed message or manual mode not activated')
    elif GET_STATE in method:
        if control.check_command(params):
            value = check_state_device(device, method)
            CLIENT.gw_send_rpc_reply(device, request_id, value, 1)
            LOGGER.info('    Success')
        else:
            LOGGER.info('    Malformed message or manual mode not activated')


def check_state_device(device_name, method):
    value = ''
    if device_name == DEVICE_AIRC and method == GET_AIRC_CONTROL_1:
        value = bool(client_attributes.get('aircIrStatus', default_data.aircIrStatus))
    elif device_name == DEVICE_AIRC and method == GET_AIRC_AUTO_1:
        value = bool(client_attributes.get('aircIrStatus', default_data.aircIrStatus))
    elif device_name == DEVICE_AIRC and method == GET_AIRC_CONTROL_2:
        value = bool(client_attributes.get('aircIrStatus', default_data.aircIrStatus))
    elif device_name == DEVICE_AIRC and method == GET_AIRC_AUTO_2:
        value = bool(client_attributes.get('aircIrStatus', default_data.aircIrStatus))
    elif device_name == DEVICE_MISC and method == GET_FAN_CONTROL:
        value = bool(client_attributes.get('miscDin0', default_data.miscDin0))
    elif device_name == DEVICE_MISC and method == GET_FAN_AUTO:
        value = bool(client_attributes.get('miscDin0', default_data.miscDin0))
    elif device_name == DEVICE_ATS and method == GET_ATS_CONTROL_MAIN:
        value = bool(client_attributes.get('atsMode', default_data.atsMode))
    elif device_name == DEVICE_ATS and method == GET_ATS_CONTROL_GEN:
        value = bool(client_attributes.get('atsMode', default_data.atsMode))
    elif device_name == DEVICE_ATS and method == GET_ATS_AUTO:
        value = bool(client_attributes.get('atsMode', default_data.atsMode))
    elif device_name == DEVICE_CRMU and method == GET_CRMU_CONTROL:
        value = bool(client_attributes.get('crmuOnlineStatus', default_data.crmuOnlineStatus))
    elif device_name == DEVICE_CRMU and method == GET_CRMU_AUTO:
        value = bool(client_attributes.get('crmuOnlineStatus', default_data.crmuOnlineStatus))
    return value

# body: {"method": "rpcCall", "params": {"device": "airc", "command": "on"}}
# gateway-set : {'device': 'device_airc', 'data': {'params': False, 'id': 4, 'method': 'setAircValue'}}
# gateway-get : {'device': 'device_airc', 'data': {'id': 4, 'method': 'getAircValue'}}
