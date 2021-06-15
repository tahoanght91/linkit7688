from config import *
import control
from config.common import *
from control.utils import check_state_device, get_value_device


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
        if GET_STATE in method:
            params = {'device': device, 'command': GET_STATE}
        elif GET_VALUE in method:
            params = {'device': device, 'command': GET_VALUE}

    if AUTO in method:
        if control.process_set_auto(params):
            commands_lock.acquire()
            commands[params['device']] = params['command']
            commands_lock.release()
            LOGGER.info('Command AUTO receive success')
        else:
            LOGGER.info('Command AUTO fail')
    elif CONTROL in method:
        if control.check_command_send_rpc(params):
            commands_lock.acquire()
            commands[params['device']] = params['command']
            commands_lock.release()
            LOGGER.info('Command CONTROL receive success')
        else:
            LOGGER.info('Command CONTROL malformed message or manual mode not activated')
    elif GET_STATE in method:
        if control.check_command(params):
            state = check_state_device(device, method)
            CLIENT.gw_send_rpc_reply(device, request_id, state, 1)
            LOGGER.info('Command GET_SATE receive success: %s', state)
        else:
            LOGGER.info('Command GET_SATE fail')
    elif GET_VALUE in method:
        if control.check_command(params):
            value_of_device = get_value_device(device, method)
            CLIENT.gw_send_rpc_reply(device, request_id, value_of_device, 1)
            LOGGER.info('Command GET_VALUE receive success: %s', value_of_device)
        else:
            LOGGER.info('Command GET_VALUE fail')

# body: {"method": "rpcCall", "params": {"device": "airc", "command": "on"}}
# gateway-set : {'device': 'device_airc', 'data': {'params': False, 'id': 4, 'method': 'setAircValue'}}
# gateway-get : {'device': 'device_airc', 'data': {'id': 4, 'method': 'getAircValue'}}
