import time

from config import *
from config.common import *

CONTINUOUS_RUN = 180 * 60  # time run
acm_period_start = 0
acm_air_alter_state = True
acm_air_alter_time = 0
acm_fan_only_cycle = 0


def _send_command(command):
    commands_lock.acquire()
    commands[DEVICE_ACM] = command
    commands_lock.release()
    return DEVICE_ACM + ':' + command


# This method is called every loop if the device is in Auto mode
def check_status():
    LOGGER.info('Enter monitor:acm:check_status')
    LOGGER.info('Shared attributes: %s', shared_attributes)
    global acm_period_start
    global acm_air_alter_state
    global acm_air_alter_time
    global acm_fan_only_cycle

    # Time to run in alternative mode (not used), convert from hour to second
    acmAlternativeTime = 3600 * shared_attributes.get('acmAlternativeTime', default_data.acmAlternativeTime)
    # Time to run/rest air-conditioner if T is lower than T2, , convert from hour to second
    acmRunTime = 3600 * shared_attributes.get('acmRunTime', default_data.acmRunTime)
    acmRestTime = 3600 * shared_attributes.get('acmRestTime', default_data.acmRestTime)
    acmGenAllow = shared_attributes.get('acmGenAllow', default_data.acmGenAllow)
    acmVacThreshold = shared_attributes.get('acmVacThreshold', default_data.acmVacThreshold)
    acmMaxHumid = shared_attributes.get('acmMaxHumid', default_data.acmMaxHumid)
    acmT1Temp = shared_attributes.get('acmT1Temp', default_data.acmT1Temp)
    acmT2Temp = shared_attributes.get('acmT2Temp', default_data.acmT2Temp)
    acmT3Temp = shared_attributes.get('acmT3Temp', default_data.acmT3Temp)
    acmT4Temp = shared_attributes.get('acmT4Temp', default_data.acmT4Temp)

    # Client
    acmOnlineState = client_attributes.get('acmOnlineState', default_data.acmOnlineState)
    acmAirc1RunState = telemetries.get('acmAirc1RunState', default_data.acmAirc1RunState)
    acmAirc2RunState = telemetries.get('acmAirc2RunState', default_data.acmAirc2RunState)
    acmFanRunState = telemetries.get('acmFanRunState', default_data.acmFanRunState)

    # acmOnlineState = client_attributes['acmOnlineState']
    # acmAirc1RunState = telemetries['acmAirc1RunState']
    # acmAirc2RunState = telemetries['acmAirc2RunState']
    # acmFanRunState = telemetries['acmFanRunState']
    # acmAutoMode = client_attributes.get('acmAutoMode', default_data.acmAutoMode)
    # acmTempError = client_attributes.get('acmTempError', default_data.acmTempError)
    # acmHumidError = client_attributes.get('acmHumidError', default_data.acmHumidError)
    # acmIState = client_attributes.get('acmIState', default_data.acmIState)
    # acmAirc1Error = client_attributes.get('acmAirc1Error', default_data.acmAirc1Error)
    # acmAirc2Error = client_attributes.get('acmAirc2Error', default_data.acmAirc2Error)
    # acmFanError = client_attributes.get('acmFanError', default_data.acmFanError)

    # Telemetry
    acmTempIndoor = telemetries.get('acmTempIndoor', default_data.acmTempIndoor)
    acmTempOutdoor = telemetries.get('acmTempOutdoor', default_data.acmTempOutdoor)
    acmHumidIndoor = telemetries.get('acmHumidIndoor', default_data.acmHumidIndoor)
    # acmTempIndoor = telemetries['acmTempIndoor']
    # acmTempOutdoor = telemetries['acmTempOutdoor']
    # acmHumidIndoor = telemetries['acmHumidIndoor']
    # acmT1TempUser = telemetries.get('acmT1Temp', default_data.acmT1Temp)
    # acmT2TempUser = telemetries.get('acmT2Temp', default_data.acmT2Temp)
    # acmT3TempUser = telemetries.get('acmT3Temp', default_data.acmT3Temp)
    # acmT4TempUser = telemetries.get('acmT4Temp', default_data.acmT4Temp)

    mccSmokeState = telemetries.get('mccSmokeState', default_data.mccSmokeState)
    mccFireState = telemetries.get('mccFireState', default_data.mccFireState)

    atsAcState = telemetries.get('atsAcState', default_data.atsAcState)

    atsVacP1 = telemetries.get('atsVacP1', default_data.atsVacP1)
    atsVacP2 = telemetries.get('atsVacP2', default_data.atsVacP2)
    atsVacP3 = telemetries.get('atsVacP3', default_data.atsVacP3)
    atsVgenP1 = telemetries.get('atsVgenP1', default_data.atsVgenP1)
    atsVgenP2 = telemetries.get('atsVgenP2', default_data.atsVgenP2)
    atsVgenP3 = telemetries.get('atsVgenP3', default_data.atsVgenP3)

    atsContactorElecState = telemetries.get('atsContactorElecState', default_data.atsContactorElecState)
    atsContactorGenState = telemetries.get('atsContactorGenState', default_data.atsContactorGenState)

    # Get current time
    timestamp = time.time()
    if acm_air_alter_time == 0:
        acm_air_alter_time = timestamp

    TempDelta = 1  # Delta temperature (in Celcius degree)

    # Decide whether to run air or fan
    air_enabled = True

    acmAirc1NextState = acmAirc1CurrentState = (acmAirc1RunState == 1)
    acmAirc2NextState = acmAirc2CurrentState = (acmAirc2RunState == 1)
    acmFanCurrentState = acmFanNextState = (acmFanRunState == 1)

    '''
    Running Permission
    '''
    # Run air-conditioner with power-generator
    # atsAcState: Lost AC Grid
    if acmGenAllow == 0 and atsAcState == 0:
        LOGGER.debug('# On power-generator, don\'t run AIRC')
        air_enabled = False

    # Don't run air-conditioner if low AC
    # TODO: make sure all BTS have 3-phase AC
    # if atsContactorElecState == 1 and (atsVacP1 < acmVacThreshold
    #                                    or atsVacP2 < acmVacThreshold
    #                                    or atsVacP3 < acmVacThreshold) \
    #         or atsContactorGenState == 1 and (atsVgenP1 < acmVacThreshold
    #                                           or atsVgenP2 < acmVacThreshold
    #                                           or atsVgenP3 < acmVacThreshold):
    #     LOGGER.debug('# Low AC, don\'t run AIRC')
    #     air_enabled = False

    '''
    Auto procedure, High -> Low priority:
    '''
    if mccSmokeState == 1 or mccFireState == 1:
        # Force turn off air-conditioner & fan when in fire
        LOGGER.debug('# Smoke or fire detected, turn off AIRC & FAN')
        acmAirc1NextState = False
        acmAirc2NextState = False
        acmFanNextState = False
        acm_fan_only_cycle = 0
        acm_period_start = 0  # Reset period timer
        acm_air_alter_time = timestamp  # Reset alternative timer
    elif acmHumidIndoor > acmMaxHumid:
        # When too humid, must turn on air-conditioner, turn off fan, don't care for temperature
        LOGGER.debug('# Humidity too high, turn on AIRC, turn off FAN')
        # But it won't run if power is too low or on Gen or Batt
        acmAirc1NextState = air_enabled
        acmAirc2NextState = air_enabled
        acmFanNextState = False
        acm_fan_only_cycle = 0
        acm_period_start = 0  # Reset period timer
        acm_air_alter_time = timestamp  # Reset alternative timer
    elif acmTempIndoor > acmT1Temp:
        # Temperature driven: T > T1 ~ run both Air if enabled
        LOGGER.debug('# Temperature driven: T > T1 ~ run both Air if enabled')
        acmAirc1NextState = air_enabled
        acmAirc2NextState = air_enabled
        acmFanNextState = False
        acm_fan_only_cycle = 0
        acm_period_start = 0  # Reset period timer
        acm_air_alter_time = timestamp  # Reset alternative timer
    elif acmT2Temp < acmTempIndoor < acmT1Temp - TempDelta:
        # Temperature driven: T1 - TempDelta > T > T2 ~ run only one Air if enabled
        LOGGER.debug('# Temperature driven: T1 - TempDelta > T > T2'
                     ' => run only one Air if enabled')
        acmAirc1NextState = air_enabled and acm_air_alter_state
        acmAirc2NextState = air_enabled and not acm_air_alter_state
        acmFanNextState = False
        acm_fan_only_cycle = 0
        acm_period_start = 0  # Reset period timer
        # Don't reset alternative timer
    elif acmTempIndoor < acmT2Temp - TempDelta:
        # Fan should already be enabled
        if acmTempOutdoor > acmT4Temp + TempDelta:
            # If temp_outdoor > T4 + delta => always one Air
            LOGGER.debug('# Temperature driven: temp_outdoor > T4 + delta => always one Air')
            acmAirc1NextState = air_enabled and acm_air_alter_state
            acmAirc2NextState = air_enabled and not acm_air_alter_state
            acmFanNextState = False
            acm_fan_only_cycle = 0
            acm_period_start = 0  # Reset period timer
            # Don't reset alternative timer
        elif acmTempOutdoor < acmT4Temp:
            # If temp_outdoor < T4 => Air off for t1 (Fan only), after t1 if temp_indoor > T3 => Air in t2 time
            LOGGER.debug('# Cycling: temp_outdoor < T4 => Air off for t1 (Fan only), after t1 if temp_indoor > T3'
                         ' => Air in t2 time')
            # t1 = acmRestTime
            # t2 = acmRunTime
            period_elapsed = timestamp - acm_period_start  # time since start of current period (either Running or Resting)
            LOGGER.debug('# ACM cycling time is: ' + str(period_elapsed))
            if acm_fan_only_cycle == 0:
                # acm_period_start == 0: First time running t1/t2 cycle (acm_period_start is reset before)
                # period_elapsed > acmRunTime: Was running for t2 already, check acmT3Temp again
                if acm_period_start == 0 or \
                        period_elapsed > acmRunTime:
                    if acmAirc1CurrentState or acmAirc2CurrentState or not acmFanCurrentState:
                        LOGGER.debug('# Running => Stop Air, run only fan in t1 time (start a new period)')
                        acmAirc1NextState = False
                        acmAirc2NextState = False
                        acmFanNextState = True
                    else:
                        # Start counting t1 (acmRestTime) after both Air1-Air2 are off and Fan is on
                        acm_fan_only_cycle = 1
                        acm_period_start = timestamp  # Start period timer
                        acm_air_alter_time = timestamp  # Reset alternative timer
            elif period_elapsed > acmRestTime:
                if acmTempIndoor >= acmT3Temp:
                    # We are resting
                    # After resting for t1, check if acmTempIndoor > acmT3Temp then start Air
                    # => Run arc1 in t2 time (start a new period)
                    LOGGER.debug('# Resting => Run arc1 in t2 time (start a new period)')
                    acmAirc1NextState = air_enabled and acm_air_alter_state
                    acmAirc2NextState = air_enabled and not acm_air_alter_state
                    acmFanNextState = False
                    # After both Air1-Air2 and Fan state are set successfully
                    if acmAirc1NextState == acmAirc1CurrentState and \
                            acmAirc2NextState == acmAirc2CurrentState and \
                            acmFanNextState == acmFanCurrentState:
                        # Start counting t2 (acmRunTime)
                        acm_fan_only_cycle = 0
                        acm_period_start = timestamp  # Start period timer
                        # Don't reset alternative timer
                else:
                    # Already acmTempIndoor < acmT3Temp, restart fan-only cycle
                    # Remove this part if want to start Air right after acmTempIndoor >= acmT3Temp
                    # without waiting for a complete t1 (acmRestTime) cycle again
                    acm_fan_only_cycle = 0
                    acm_period_start = 0            # Reset period timer
                    acm_air_alter_time = timestamp  # Reset alternative timer
    elif not acmAirc1CurrentState and not acmAirc2CurrentState:
        # Prevent case when both air is off and temperature falls between the delta
        acmAirc1NextState = air_enabled and acm_air_alter_state
        acmAirc2NextState = air_enabled and not acm_air_alter_state
        acmFanNextState = False
        acm_fan_only_cycle = 0
        acm_period_start = 0  # Reset period timer
        # Don't reset alternative timer

    # Counting alternative time, only if 1 airc is running:
    if (acmAirc1NextState and not acmAirc2NextState) or (not acmAirc1NextState and acmAirc2NextState):
        # Set acmAlternativeTime to = to disable alternative mode
        if timestamp - acm_air_alter_time > acmAlternativeTime > 0:
            acm_air_alter_time = timestamp
            acm_air_alter_state = not acm_air_alter_state

    if not acmOnlineState:
        LOGGER.debug("ACM not online, won't send command")
        return ''

    '''
    Checking next state and issue command. Send 1 command at a time.
    '''
    rtn = ''
    if acmAirc1CurrentState and not acmAirc1NextState:
        rtn += _send_command(COMMAND_ACM_AIRC_1_OFF)
    elif not acmAirc1CurrentState and acmAirc1NextState:
        rtn += _send_command(COMMAND_ACM_AIRC_1_ON)
    elif acmAirc2CurrentState and not acmAirc2NextState:
        rtn += _send_command(COMMAND_ACM_AIRC_2_OFF)
    elif not acmAirc2CurrentState and acmAirc2NextState:
        rtn += _send_command(COMMAND_ACM_AIRC_2_ON)
    elif acmFanCurrentState and not acmFanNextState:
        rtn += _send_command(COMMAND_ACM_FAN_OFF)
    elif not acmFanCurrentState and acmFanNextState:
        rtn += _send_command(COMMAND_ACM_FAN_ON)

    LOGGER.info('Exit monitor:acm:check_status - ' + rtn)
    return rtn
