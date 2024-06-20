import time
import unittest
import multiprocessing as mp


class Data:
    def __init__(self, num: int) -> None:
        self.num = num


class WorkerProcess(mp.Process):
    def __init__(self, data: Data = None, edit_idx=0):
        super().__init__()
        self.data = data
        self.edit_idx = edit_idx

    def run(self):
        i = 0
        while True:
            if i == self.edit_idx:
                self.data.num = i
            print(self.data.num)
            time.sleep(1)
            i += 1


class SharedMPInitTestCase(unittest.TestCase):

    def test_ndarray_mp_queue(self):

        q = mp.Queue()
        data = Data(10)

        worker1 = WorkerProcess(data, 5)
        worker2 = WorkerProcess(data, 15)
        worker1.start()
        worker2.start()

        worker1.join()
        worker2.join()
        self.assertTrue(True)


if __name__ == "__main__":
    mp.set_start_method('spawn')
    unittest.main()
