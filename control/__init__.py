from . import utils


def process_set_auto(command):
    """
    Check the eligibility of a rpc call that set auto mode of components
    """
    return utils._process_set_auto(command.get('device', None), command.get('command', None))


def check_command(command):
    """
    Check the eligibility of a rpc call from the server
    """
    return utils._check_command(command.get('device', None), command.get('command', None))


def check_command_send_rpc(command):
    return utils._check_command_send_rpc(command.get('device', None), command.get('command', None))


def process_command(command):
    """
    Take a command and create a bytes respective to that command, without the check sum
    """
    return utils._process_command(command['device'], command['command'])
