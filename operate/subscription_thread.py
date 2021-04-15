import time
import json

from config import *
import mqtt
import control
from monitor import bell, crmu


def _attribute_change_callback(result, exception):
    LOGGER.info(
        'Received attribution changed message, exception: ' + str(exception))
    if exception is None:
        log_info = []
        for key, value in result.items():
            log_info.append('\t{:>20s}: {:>20s}'.format(str(key), str(value)))
            shared_attributes[key] = value
        LOGGER.info('\n'.join(log_info))

def _rpc_callback(request_id, request_body):
    LOGGER.info('Received rpc message\n    Id: %s\n    Body: %s',
                request_id, request_body)
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


#body: {"method": "rpcCall", "params": {"device": "airc", "command": "on"}}