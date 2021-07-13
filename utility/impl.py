import time
import struct
from config import _OpData, BYTE_ORDER
from config import LOGGER


# from numba import jit

def bytes_to_int(data, byteorder=None):
    if len(data) == 1:
        return struct.unpack('B', data)[0]
    if byteorder == 'little':
        fmt = '<'
    elif byteorder == 'big':
        fmt = '>'
    else:
        raise ValueError()
    if len(data) == 2:
        return struct.unpack(fmt + 'H', data)[0]
    elif len(data) == 4:
        return struct.unpack(fmt + 'I', data)[0]


def with_check_sum(byte_stream, byteorder):
    return byte_stream + _check_sum(byte_stream, byteorder)


def check_check_sum(byte_stream, byteorder):
    return _check_sum(byte_stream[:-2], byteorder) == byte_stream[-2:]


def blocking_read_number_of_byte(ser, number_of_byte):
    ser.read(number_of_byte)


def blocking_read_datablock(ser, message_break):
    initial_break = message_break / 10
    start = time.time()
    read_buffer = b''
    while True:
        read_buffer = b''

        # quit if no telemetry packet in duration
        duration = time.time() - start
        if duration > initial_break:
            LOGGER.info('Not found any data packet in: %s ms', str(duration))
            break

        read_buffer = ser.read(1)

        if read_buffer[0] == b'\xa0':
            read_buffer += ser.read(2)
            read_buffer_decode = ':'.join(x.encode('hex') for x in read_buffer)
            LOGGER.info('Found header. Checking next 2 byte for len+opcode in read_buffer: %s', str(read_buffer_decode))
            data_len = bytes_to_int(read_buffer[1])
            op_code = read_buffer[2]
            if data_len > 0 and (op_code == _OpData.IO_STATUS_ACM or
                    op_code == _OpData.IO_STATUS_ATS or
                    op_code == _OpData.IO_STATUS_CRMU or
                    op_code == _OpData.IO_STATUS_LCD or
                    op_code == _OpData.IO_STATUS_MCC or
                    op_code == _OpData.IO_STATUS_RPC or
                    op_code == _OpData.IO_STATUS_ACK_LED or
                    op_code == _OpData.IO_STATUS_ACK_LCD or
                    op_code == _OpData.IO_STATUS_ACK_SHARED_ATT_LED or
                    op_code == _OpData.IO_STATUS_CLOCK_SET or
                    op_code == _OpData.IO_STATUS_CLOCK_EXTRACT):
                LOGGER.info('Found packet header, data with with len %s, opcode %s', data_len, op_code)
                # datalen + 2 byte checksum, - 1 byte op_code
                read_buffer += ser.read(data_len + 2 - 3)
                read_buffer_decode = ':'.join(x.encode('hex') for x in read_buffer)
                LOGGER.info('Received packet: %s', str(read_buffer_decode))
                # crc = read_buffer[-2] << 8 | read_buffer[-1]
                # if check_check_sum(read_buffer, BYTE_ORDER):
                #     LOGGER.info('Check sum successfully')
                #     break
                # else:
                #     LOGGER.info('Drop frame')
                if not check_check_sum(read_buffer, BYTE_ORDER):
                    LOGGER.debug('Check sum not right, expected check sum %s, received check sum %s',
                                 with_check_sum(read_buffer[:-2], BYTE_ORDER)[-2:].encode('hex'),
                                 read_buffer[-2:].encode('hex'))
                else:
                    break
            else:
                LOGGER.info('Not found header+len+opcode in 3 byte %s', str(read_buffer_decode))
                read_buffer = b''
        else:
            LOGGER.debug('Mark byte not right, expected mark byte A0, received mark byte %s',
                         str(read_buffer[0].encode('hex')))
            read_buffer = b''

    return read_buffer


def _check_sum(byte_stream, byteorder):
    '''
    The function use the crc16 checksum algorithm as follow:
    
        static uint16_t mb_crc16(uint8_t buf[], uint16_t len)
        {
            uint16_t crc16 = 0xFFFF;
            uint16_t i, j, tmp;

            for (i = 0; i < len; ++i) {
                crc16 ^= buf[i];
                for (j = 8; j > 0; --j) {
                    tmp = crc16 & 0x0001;
                    crc16 >>= 1;
                    if (tmp == 1) {
                        crc16 ^= 0xA001;
                    }
                }
            }
            return crc16;
        }
    '''

    length = len(byte_stream)
    crc16 = 0xFFFF
    for i in range(length):
        crc16 ^= bytes_to_int(byte_stream[i])
        for _ in range(8, 0, -1):
            tmp = crc16 & 0x0001
            crc16 >>= 1
            if tmp:
                crc16 ^= 0xA001
    if byteorder == 'little':
        fmt = '<H'
    elif byteorder == 'big':
        fmt = '>H'
    else:
        raise ValueError()
    return struct.pack(fmt, crc16)

# def check_sum_frame(frame):
#     crc16 = 0xFFFF
#     for i in frame:
#         crc16 ^= i
#         for index in range(8, 0, -1):
#             tmp = crc16 & 0x0001
#             crc16 >>= 1
#             if tmp == 1:
#                 crc16 ^= 0xA001
#     return crc16

