redque
======

A distributed queue based on Redis

Installation
------------

.. code-block:: python

    pip install redque

Example
-------

.. code-block:: python

    import time
    import random
    import threading
    import redis
    import redque


    def productor(redis_conn):
        other_queue = redque.Queue(redis_conn, "__test", "bp__test")

        for _ in range(100):
            other_queue.push("e_{0}".format(random.randint(1, 100)))
            time.sleep(0.1)


    if __name__ == "__main__":
        pool = redis.ConnectionPool(
            host="127.0.0.1",
            port=6379,
            password="123456"
        )

        queue = redque.Queue(
            redis.Redis(connection_pool=pool),
            "__test",
            "bp__test"
        )
        queue.clear(True)

        # non-blocking
        for _ in range(100):
            queue.push(random.randint(1, 100))

        queue.process(lambda x: (print(x), True), False)

        # blocking
        t = threading.Thread(target=productor,
                            args=(redis.Redis(connection_pool=pool),))
        t.start()

        queue.process(lambda x: (print(x), True), timeout=3)

        t.join()
