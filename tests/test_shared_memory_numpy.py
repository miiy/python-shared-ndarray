import time
import numpy as np
import multiprocessing as mp
import multiprocessing.shared_memory as shm
import unittest


class SharedMemoryNumpyTestCase(unittest.TestCase):

    def test_shared_memory(self):
        shm_a = shm.SharedMemory(create=True, size=10)
        print(shm_a.name)
        print(len(shm_a.buf))
        shm_a.close()
        shm_a.unlink()
        print(shm_a.buf)
        self.assertIsNone(shm_a.buf)

    def test_np_nbytes(self):
        shape = (1920, 1080, 3)
        dtype = np.uint8
        data = np.ones(shape, dtype=dtype)
        print(f"data nbytes: {data.nbytes}")

        size = int(np.prod(shape)) * np.dtype(dtype).itemsize

        self.assertEqual(data.nbytes, size)

    def test_mp_queue(self):
        data = np.ones((1920, 1080, 3), dtype=np.uint8)
        q = mp.Queue()

        # put
        t1 = time.time()
        q.put(data)
        t2 = time.time() - t1
        print(f"put time: {t2}")

        # get
        t1 = time.time()
        _ = q.get()
        t2 = time.time() - t1
        print(f"get time: {t2}")

        self.assertTrue(True)

    def test_shared_memory_mp_queue(self):
        data = np.ones((1920, 1080, 3), dtype=np.uint8)
        q = mp.Queue()
        # put
        t1 = time.time()

        shm_a = shm.SharedMemory(create=True, size=data.nbytes)
        shm_ndarray = np.ndarray(data.shape, dtype=data.dtype, buffer=shm_a.buf)
        shm_ndarray[:] = data[:]
        shm_a.close()
        # print(shm_ndarray.shape)
        # print(shm_ndarray) error! buf is close

        q.put(shm_a.name)
        t2 = time.time() - t1
        print(f"put time: {t2}")

        # get
        t1 = time.time()
        shm_a_name = q.get()

        existing_shm = shm.SharedMemory(name=shm_a_name, create=False)
        data_recv = np.ndarray(data.shape, dtype=data.dtype, buffer=existing_shm.buf)
        data_copy = np.ndarray(data.shape, dtype=data.dtype)
        data_copy[:] = data_recv[:]
        existing_shm.close()
        existing_shm.unlink()
        # print(data_copy) ok
        # print(data_recv) error: buf is free

        t2 = time.time() - t1
        print(f"get time: {t2}")
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()

