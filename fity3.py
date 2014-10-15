"""
Fity3 is a Twitter snowflake like scheme generator that fits in 53 bits (for
JavaScript)

Its scheme is:

    timestamp | worker_id | sequence
     41 bits  |  4 bits   |  8 bits

Timestamp is in milliseconds since the epoch allowing for 69 years of ids.

Each id generated per millisecond receives a unique auto incrementing sequence
number. Each worker can produce 256 ids per millisecond.

The scheme allows for 16 unique workers, so at most 4 million ids (16*256*1000)
can be produced per second with this scheme.
"""

import time
import logging


log = logging.getLogger(__name__)


__version__ = '0.6'


# Wed, 15 Oct 2014 11:00:00.000 GMT
fitepoch = 1413370800000

worker_id_bits = 4
max_worker_id = -1 ^ (-1 << worker_id_bits)
sequence_bits = 8
worker_id_shift = sequence_bits
timestamp_left_shift = sequence_bits + worker_id_bits
sequence_mask = -1 ^ (-1 << sequence_bits)
timestamp_mask = -1 >> timestamp_left_shift << timestamp_left_shift


def to_timestamp(_id):
    _id = _id >> timestamp_left_shift  # strip the lower bits
    _id += fitepoch                    # adjust for epoch
    _id = _id / 1000                   # convert from milliseconds to seconds
    return _id


def generator(worker_id, sleep=lambda x: time.sleep(x/1000.0)):
    assert worker_id >= 0 and worker_id <= max_worker_id

    last_timestamp = -1
    sequence = 0

    while True:
        timestamp = int(time.time() * 1000)

        if last_timestamp > timestamp:
            log.warning(
                "clock is moving backwards. waiting until %i" % last_timestamp)
            sleep(last_timestamp-timestamp)
            continue

        if last_timestamp == timestamp:
            sequence = (sequence + 1) & sequence_mask
            if sequence == 0:
                log.warning("sequence overrun")
                sequence = -1 & sequence_mask
                sleep(1)
                continue
        else:
            sequence = 0

        last_timestamp = timestamp

        yield (
            ((timestamp-fitepoch) << timestamp_left_shift) |
            (worker_id << worker_id_shift) |
            sequence)
