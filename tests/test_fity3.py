import time
import sys

import fity3


def rerun(n):
    def decorate(f):
        def wrap(*a, **kw):
            while True:
                try:
                    return f(*a, **kw)
                except AssertionError:
                    decorate.n = decorate.n - 1
                    if decorate.n <= 0:
                        raise
        return wrap
    decorate.n = n
    return decorate


def sleep_till_ms_start():
    t = time.time()*1000
    time.sleep((1 - (t - int(t)))/1000.0)


@rerun(getattr(sys, 'subversion', ['CPython'])[0] == 'PyPy' and 5 or 3)
def test_generator():
    f3 = fity3.generator(1)

    sleep_till_ms_start()

    _id1 = next(f3)
    _id2 = next(f3)
    _id3 = next(f3)

    assert _id1 & fity3.sequence_mask == 0
    assert _id2 & fity3.sequence_mask == 1
    assert _id3 & fity3.sequence_mask == 2
    assert _id1 & fity3.timestamp_mask == \
        _id2 & fity3.timestamp_mask == _id3 & fity3.timestamp_mask

    # test that we sleep and then wrap to the next millisecond once the
    # sequence is exhausted
    sleep_till_ms_start()

    for i in range(256):
        _id1 = next(f3)

    _id2 = next(f3)

    assert _id1 & fity3.sequence_mask == 255
    assert _id2 & fity3.sequence_mask == 0
    assert _id2 & fity3.timestamp_mask > _id1 & fity3.timestamp_mask


def test_to_timestamp():
    f3 = fity3.generator(1)
    sleep_till_ms_start()
    _id = next(f3)
    t = time.time()
    assert int(t) == int(fity3.to_timestamp(_id))
