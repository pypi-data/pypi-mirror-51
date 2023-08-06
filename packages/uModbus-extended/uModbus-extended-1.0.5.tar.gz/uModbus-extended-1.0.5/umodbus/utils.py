import sys
import struct
import logging
from logging import StreamHandler, Formatter
from functools import wraps

from umodbus import log


def log_to_stream(stream=sys.stderr, level=logging.NOTSET,
                  fmt=logging.BASIC_FORMAT):
    """ Add :class:`logging.StreamHandler` to logger which logs to a stream.

    :param stream. Stream to log to, default STDERR.
    :param level: Log level, default NOTSET.
    :param fmt: String with log format, default is BASIC_FORMAT.
    """
    fmt = Formatter(fmt)
    handler = StreamHandler()
    handler.setFormatter(fmt)
    handler.setLevel(level)

    log.addHandler(handler)


def unpack_mbap(mbap):
    """ Parse MBAP of 7 bytes and return tuple with fields.

        >>> parse_mbap(b'\x00\x08\x00\x00\x00\x06\x01')
        (8, 0, 6, 1)

    :param mbap: Array of 7 bytes.
    :return: Tuple with 4 values: Transaction identifier,  Protocol identifier,
        Length and Unit identifier.
    """
    # '>' indicates data is big-endian. Modbus uses this alignment. 'H' and 'B'
    # are format characters. 'H' is unsigned short of 2 bytes. 'B' is an
    # unsigned char of 1 byte.  HHHB sums up to 2 + 2 + 2 + 1 = 7 bytes.

    # TODO What it right exception to raise? Error code 04, Server failure,
    # seems most appropriate.
    return struct.unpack('>HHHB', mbap)


def pack_mbap(transaction_id, protocol_id, length, unit_id):
    """ Create and return response MBAP.

    :param transaction_id: Transaction id.
    :param protocol_id: Protocol id.
    :param length: Length of following bytes in ADU.
    :param unit_id: Unit id.
    :return: Byte array of 7 bytes.
    """
    return struct.pack('>HHHB', transaction_id, protocol_id, length, unit_id)


def pack_exception_pdu(function_code, error_code):
    """ Return exception PDU of 2 bytes.

        "The exception response message has two fields that differentiate it
        from a nor mal response: Function Code Field: In a normal response, the
        server echoes the function code of the original request in the function
        code field of the response. All function codes have a most -
        significant bit (MSB) of 0 (their values are all below 80 hexadecimal).
        In an exception response, the server sets the MSB of the function code
        to 1.  This makes the function code value in an exception response
        exactly 80 hexadecimal higher than the value would be for a normal
        response.

        With the function code's MSB set, the client's application program can
        recognize the exception response and can examine the data field for the
        exception code.  Data Field: In a normal response, the server may
        return data or statistics in the data field (any information that was
        requested in the request). In an exception response, the server returns
        an exception code in the data field. This defines the server condition
        that caused the exception."

        -- MODBUS Application Protocol Specification V1.1b3, chapter 7

        ================ ===============
        Field            Length (bytes)
        ================ ===============
        Error code       1
        Function code    1
        ================ ===============

    :param error_code: Error code.
    :param function_code: Function code.
    :return: PDU of 2 bytes.
    """
    return struct.pack('>BB', function_code + 0x80, error_code)


def get_function_code_from_request_pdu(pdu):
    """ Return function code from request PDU.

    :return pdu: Array with bytes.
    :return: Function code.
    """
    return struct.unpack('>B', pdu[:1])[0]


def memoize(f):
    """ Decorator which caches function's return value each it is called.
    If called later with same arguments, the cached value is returned.
    """
    cache = {}

    @wraps(f)
    def inner(arg):
        if arg not in cache:
            cache[arg] = f(arg)
        return cache[arg]
    return inner


def recv_exactly(recv_fn, size):
    """ Use the function to read and return exactly number of bytes desired.

    https://docs.python.org/3/howto/sockets.html#socket-programming-howto for
    more information about why this is necessary.

    :param recv_fn: Function that can return up to given bytes
        (i.e. socket.recv, file.read)
    :param size: Number of bytes to read.
    :return: Byte string with length size.
    :raises ValueError: Could not receive enough data (usually timeout).
    """
    recv_bytes = 0
    chunks = []
    while recv_bytes < size:
        chunk = recv_fn(size - recv_bytes)
        if len(chunk) == 0:  # when closed or empty
            break
        recv_bytes += len(chunk)
        chunks.append(chunk)

    response = b''.join(chunks)

    if len(response) != size:
        raise ValueError

    return response




def _short_unpacker(packed_data):
    """
    Returns a tuple representing the packed data with the length
    of the format type of the given original packed data
    """
    short_bytes_count = 'H' * int(len(packed_data)/2)
    return struct.unpack('{bytes_count}'.format(bytes_count=short_bytes_count), packed_data)

def _short_packer(unpacked_data):
    """ Returns a list representing the unpacked data as int16, 2 bytes packed list """
    data = []
    for unpacked_int16 in unpacked_data:
        data.append(struct.pack('H', unpacked_int16))
    return data

def data_packer(value, indianess='=', data_type='H', byte_swap_type='abcd'):
    """ Returns the data packed, ready to be written """
    packed_data = struct.pack('{0}{1}'.format(indianess, data_type), value)
    unpacked_int16_data = _short_unpacker(packed_data)
    unpacked_int16_data = _byte_word_swap_manager(unpacked_int16_data, byte_swap_type=byte_swap_type)
    return unpacked_int16_data


def data_unpacker(data, indianess='=', data_type='H', byte_swap_type='abcd'):
    """ Returns the unpacked data, as the format specified """
    packed_bytes = _short_packer(data)

    packed_bytes = _byte_word_swap_manager(packed_bytes, byte_swap_type=byte_swap_type)

    return struct.unpack('{0}{1}'.format(indianess, data_type), b''.join(packed_bytes))


def _byte_word_swap_manager(packed_bytes, byte_swap_type=None):
    if len(packed_bytes) == 2:
        if byte_swap_type == 'cdab':
            packed_bytes[0], packed_bytes[1] = packed_bytes[1], packed_bytes[0]
        else:
            pass
    elif len(packed_bytes) == 4:
        if byte_swap_type == 'cdab':
            packed_bytes = [packed_bytes[2], packed_bytes[3], packed_bytes[0], packed_bytes[1]]
        elif byte_swap_type == 'dcba':
            packed_bytes = [packed_bytes[3], packed_bytes[2], packed_bytes[1], packed_bytes[0]]
        elif byte_swap_type == 'badc':
            packed_bytes = [packed_bytes[1], packed_bytes[0], packed_bytes[3], packed_bytes[2]]
        else:
            pass
    return packed_bytes


