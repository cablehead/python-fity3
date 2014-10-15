import fity3


def test_generator():

    class Now(object):
        def __init__(self, now):
            self.now = now
            self.log = []

        def __call__(self):
            return self.now

        def sleep(self, n):
            self.log.append(n)
            self.now += n
            return self

        def clear(self):
            self.log = []

    now = Now(1413401558001)

    f3 = fity3.generator(1, sleep=now.sleep, now=now)

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
    now.sleep(1).clear()

    for i in range(256):
        _id1 = next(f3)

    _id2 = next(f3)

    assert now.log == [1]
    now.clear()

    assert _id1 & fity3.sequence_mask == 255
    assert _id2 & fity3.sequence_mask == 0
    assert _id2 & fity3.timestamp_mask > _id1 & fity3.timestamp_mask


def test_to_timestamp():
    f3 = fity3.generator(1, now=lambda: 1413401558001)
    _id = next(f3)
    assert int(fity3.to_timestamp(_id)) == 1413401558
