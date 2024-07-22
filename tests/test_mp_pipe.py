import time
import numpy as np
import multiprocessing as mp
import unittest


def producer(write_conn: mp.Pipe) -> None:
    # handle frame data
    frames = [np.zeros((1080, 1920, 3), dtype=np.uint8) for i in range(250)]

    start_time = time.time()
    for i in range(len(frames)):
        frame = frames[i]
        write_conn.send(frame)
        # send time
        if i % 25 == 0:
            total_time = time.time() - start_time
            start_time = time.time()
            print(f"send time: {total_time}")


def consumer(read_conn: mp.Pipe) -> None:
    i = 0
    start_time = time.time()
    while True:
        try:
            frame = read_conn.recv()
        except Exception as e:
            print(e)

        # receive time
        if i % 25 == 0:
            total_time = time.time() - start_time
            start_time = time.time()
            print(f"recv time: {total_time}")
        i += 1


class MPPipeTestCase(unittest.TestCase):

    def test_run(self):
        mp.set_start_method('spawn')
        read_conn, write_conn = mp.Pipe()
        p_process = mp.Process(target=producer, args=(write_conn,))
        p_process.start()

        consumer(read_conn)

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
