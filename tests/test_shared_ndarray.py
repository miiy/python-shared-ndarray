import time
import queue
import unittest
import numpy as np
import multiprocessing as mp
import shared_ndarray as sn


def produce(q: mp.Queue, shared: bool = False):
    data = np.ones((1920, 1080, 3), dtype=np.uint8)
    t1 = time.time()

    total = 25
    for i in range(total):
        if shared:
            arr = sn.from_numpy(data)
        else:
            arr = data
        q.put(arr)
    t2 = time.time() - t1
    avg_time = t2 / total
    print(f"put time: {t2}, avg: {avg_time}")


def wait_queue(q: mp.Queue):
    try:
        while q.qsize() == 0:
            time.sleep(0.001)
    except NotImplementedError:
        while q.empty():
            time.sleep(0.001)


def consumer(q: mp.Queue, shared: bool = False):
    t1 = time.time()

    wait_queue(q)

    total = 0
    while True:
        try:
            arr = q.get(timeout=0.01)
            total += 1
        except queue.Empty:
            break
        # arr
        if shared:
            arr.close()
            arr.unlink()

    t2 = time.time() - t1
    avg_time = t2 / total
    print(f"get time: {t2}, avg: {avg_time}, total: {total}")
    # print(arr_list[0])


def consumer_with_copy(q: mp.Queue, shared: bool = False):
    t1 = time.time()
    arr_list = []

    wait_queue(q)

    total = 0
    while True:
        try:
            arr = q.get(timeout=0.01)
            total += 1
        except queue.Empty:
            break
        if shared:
            arr_copy = arr.clone()
            arr.close()
            arr.unlink()
        else:
            arr_copy = arr
        arr_list.append(arr_copy)
    t2 = time.time() - t1
    avg_time = t2 / total
    print(f"get time: {t2}, avg: {avg_time}, total: {total}")
    # print(arr_list[0])


class SharedNDArrayTestCase(unittest.TestCase):

    def test_ndarray_mp_queue(self):
        q = mp.Queue()
        p1 = mp.Process(target=produce, args=(q,))
        p2 = mp.Process(target=consumer, args=(q,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        self.assertTrue(True)

    def test_shared_ndarray_mp_queue(self):
        q = mp.Queue()
        p1 = mp.Process(target=produce, args=(q, True))
        p2 = mp.Process(target=consumer, args=(q, True))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        self.assertTrue(True)

    def test_shared_ndarray_mp_queue_with_copy(self):
        q = mp.Queue()
        p1 = mp.Process(target=produce, args=(q, True))
        p2 = mp.Process(target=consumer_with_copy, args=(q, True))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        self.assertTrue(True)


if __name__ == "__main__":
    mp.set_start_method('spawn')
    unittest.main()
