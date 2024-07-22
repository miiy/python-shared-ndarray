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
            arr_copy = arr.clone_numpy()
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

    def test_shared_ndarray_basic(self):
        q = mp.Queue()

        # put
        data = np.ones((1920, 1080, 3), dtype=np.uint8)
        arr = sn.from_numpy(data)
        q.put(arr)

        # get
        arr_recv = q.get()
        data2 = arr_recv.get_numpy()
        self.assertTrue(np.array_equal(data, data2))

        arr_recv.close()
        arr_recv.unlink()

    def test_shared_ndarray_multi(self):
        q = mp.Queue()

        # put
        data1 = np.ones((1920, 1080, 3), dtype=np.uint8)
        data2 = np.array([[1, 2], [2, 3]])
        arr = sn.from_numpy(data1=data1, data2=data2)
        q.put(arr)

        # get
        arr_recv = q.get()
        data1_1 = arr_recv.get_numpy("data1")
        data2_1 = arr_recv.get_numpy("data2")
        self.assertTrue(np.array_equal(data1, data1_1))
        self.assertTrue(np.array_equal(data2, data2_1))

        arr_recv.close()
        arr_recv.unlink()

    def test_shared_ndarray_update(self):
        data1 = np.ones((1920, 1080, 3), dtype=np.uint8)
        data2 = np.array([[1, 2], [2, 3]])
        arr = sn.from_numpy(data1=data1, data2=data2)

        data3 = np.array([[2, 3], [3, 4]])
        arr.set("data2", data3)
        arr_data2 = arr.get_numpy("data2")

        self.assertTrue(np.array_equal(data3, arr_data2))
        arr.close()
        arr.unlink()

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

    def test_shared_ndarray_list(self):
        mp.set_start_method('spawn')
        image_data = np.ones((1080, 1920, 3), dtype=np.uint8)
        wav_frame_num = int(44100 / 25)
        audio_data = np.zeros(wav_frame_num, dtype=np.int16)

        q = mp.Queue()

        start_time = time.time()
        for i in range(250):
            send_packet = sn.from_numpy(image=image_data, audio=audio_data)
            q.put(send_packet)
            # put time
            if i % 25 == 0:

                total_time = time.time() - start_time
                start_time = time.time()
                print(f"put time: {total_time}")

        start_time = time.time()
        for i in range(250):
            recv_packet = q.get()
            image_byte = recv_packet.get("image")
            audio_byte = recv_packet.get("audio")
            recv_packet.close()
            recv_packet.unlink()
            # get time
            if i % 25 == 0:
                total_time = time.time() - start_time
                start_time = time.time()
                print(f"get time: {total_time}")

        self.assertTrue(True)


if __name__ == "__main__":
    mp.set_start_method('spawn')
    unittest.main()
