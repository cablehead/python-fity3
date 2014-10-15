Fity3 is a Twitter snowflake like scheme generator that fits in 53 bits (for
JavaScript)

Its scheme is::

    timestamp | worker_id | sequence
     41 bits  |  4 bits   |  8 bits

Timestamp is in milliseconds since the epoch allowing for 69 years of ids.

Each id generated per millisecond receives a unique auto incrementing sequence
number. Each worker can produce 256 ids per millisecond.

The scheme allows for 16 unique workers, so at most 4 million ids (16*256*1000)
can be produced per second with this scheme.

.. code:: python

    >>> import fity3
    >>> f3 = fity3.generator(1)
    >>> f3.next()
    14127739136
    >>> f3.next()
    14132125952
    >>> f3.next()
    14135079168

    # convenience to convert to a unix timestamp
    >>> fity3.to_timestamp(14135079168)
    1413374250
