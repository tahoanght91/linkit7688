from config import *
import control


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
    method = content['data']['method']
    device = content['device']
    value = content['data']['params']
    params = {'device': device, 'command': value}
    if 'auto' in method:
        if control.process_set_auto(params):
            LOGGER.info('    Success')
        else:
            LOGGER.info('    Malformed message')
    elif method == 'setAircValue':
        if control.check_command(params):
            commands_lock.acquire()
            commands[params['device']] = params['command']
            commands_lock.release()
            LOGGER.info('    Success')
        else:
            LOGGER.info('    Malformed message or manual mode not activated')

# body: {"method": "rpcCall", "params": {"device": "airc", "command": "on"}}
