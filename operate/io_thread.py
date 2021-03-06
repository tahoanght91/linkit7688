import time

import serial

import control
from config import *
from devices import airc, ats, atu, crmu, dc, misc
from utility import *

def call():
    ser = serial.Serial(port = IO_PORT, baudrate = BAUDRATE)
    data_ack = b'\xa0\x02\x11\x00'
    control_ack = b'\xa0\x01\x21'
    message_break = shared_attributes.get('periodReadDataIO', default_data.periodReadDataIO) # time read data from IO
    flip = READ_PER_WRITE

    while True:
        # Read data
        byte_stream = blocking_read(ser, message_break)
        if byte_stream and _read_data(byte_stream):
            ser.write(with_check_sum(data_ack, BYTE_ORDER))        

        # Write command
        if commands:
            commands_snap = []
            commands_lock.acquire()
            for item in commands.items():
                commands_snap.append(item)
            commands_lock.release()
            for device, command in commands_snap:
                command_formatted = {'device': device, 'command': command}             
                write_stream = with_check_sum(control.process_command(command_formatted), BYTE_ORDER)
                tries = 0
                LOGGER.info('Send command to IO, device %s, command %s', device, command)
                while True:
                    if flip == 0:
                        flip = READ_PER_WRITE
                        ser.write(write_stream)
                    else:
                        flip -= 1
                    byte_stream = blocking_read(ser, message_break)
                    if byte_stream:
                        if byte_stream == with_check_sum(control_ack, BYTE_ORDER):
                            commands_lock.acquire()
                            if commands[device] == command:
                                del commands[device]
                            commands_lock.release()
                            LOGGER.debug("Receive ACK message")
                            break
                        if _read_data(byte_stream):
                            ser.write(with_check_sum(data_ack, BYTE_ORDER))
                    if flip == 0:
                        tries += 1
                        if tries > 3:
                            LOGGER.info('Time out')
                            break
                        LOGGER.debug('Try sending again')

def _read_data(byte_stream):
    LOGGER.info('Receive data message')
    if len(byte_stream) < 3:
        LOGGER.debug('Message too short, length %d', len(byte_stream))
        return False
    if byte_stream[0] != b'\xa0':
        LOGGER.debug('Mark byte not right, expected mark byte A0, received mark byte %s', byte_stream[0].encode('hex'))
        return False
    if not check_check_sum(byte_stream, BYTE_ORDER):
        LOGGER.debug('Check sum not right, expected check sum %s, received check sum %s',
                with_check_sum(byte_stream[:-2], BYTE_ORDER)[-2:].encode('hex'),
                byte_stream[-2:].encode('hex'))
        return False
    frame_length = bytes_to_int(byte_stream[1])
    op_code = byte_stream[2]
    LOGGER.debug('Opcode %s', op_code.encode('hex'))
    data = byte_stream[3:-2]
    if op_code == _OpData.IO_STATUS_MISC: # MISC
        LOGGER.info('MISC message, declared length: %d, real length: %d, expected length: %d', frame_length - 1, len(data), _OpData.MISC_SIZE)
        if _check_data(frame_length, data, _OpData.MISC_SIZE):
            misc.extract(data)
            return True
    elif op_code == _OpData.IO_STATUS_DC: # DC
        LOGGER.info('DC message, declared length: %d, real length: %d, expected length: %d', frame_length - 1, len(data), _OpData.DC_SIZE)
        if _check_data(frame_length, data, _OpData.DC_SIZE):
            dc.extract(data[1:])
            return True
    elif op_code == _OpData.IO_STATUS_ATS: # ATS
        LOGGER.info('ATS message, declared length: %d, real length: %d, expected length: %d', frame_length - 1, len(data), _OpData.ATS_SIZE)
        if _check_data(frame_length, data, _OpData.ATS_SIZE):
            ats.extract(data[1:])
            return True
    elif op_code == _OpData.IO_STATUS_AIRC: # AIRC
        LOGGER.info('AIRC message, declared length: %d, real length: %d, expected length: %d', frame_length - 1, len(data), _OpData.AIRC_SIZE)
        if _check_data(frame_length, data, _OpData.AIRC_SIZE):
            airc.extract(data[1:])
            return True
    elif op_code == _OpData.IO_STATUS_ATU: # ATU
        LOGGER.info('ATU message, declared length: %d, real length: %d, expected length: %d', frame_length - 1, len(data), _OpData.ATU_SIZE)
        if _check_data(frame_length, data, _OpData.ATU_SIZE):
            atu.extract(data[1:])
            return True
    elif op_code == _OpData.IO_STATUS_CRMU: # CRMU
        LOGGER.info('CRMU message, declared length: %d, real length: %d, expected length: %d', frame_length - 1, len(data), _OpData.CRMU_SIZE)
        if _check_data(frame_length, data, _OpData.CRMU_SIZE):
            crmu.extract(data[1:])
            return True
    return False


class _OpData:
    MISC_SIZE = 16
    AIRC_SIZE = 24
    ATS_SIZE = 92
    ATU_SIZE = 38
    CRMU_SIZE = 15
    DC_SIZE = 29
    KEY_SIZE = 3

    IO_STATUS_MISC = b'\x11'
    IO_STATUS_DC = b'\x12'
    IO_STATUS_ATS = b'\x13'
    IO_STATUS_AIRC = b'\x14'
    IO_STATUS_ATU = b'\x15'
    IO_STATUS_CRMU = b'\x16'

def _check_data(frame_length, data, expected_data_length):
    if frame_length != len(data) + 1 or frame_length != expected_data_length + 1:
        return False
    else:
        return True
