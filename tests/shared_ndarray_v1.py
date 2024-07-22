import numpy as np
from multiprocessing.shared_memory import SharedMemory


class SharedNDArray:
    def __init__(self, shape: tuple, dtype: np.dtype, name: str | None = None):
        self._shape = shape
        self._dtype = dtype
        if name:
            self._shm = SharedMemory(name=name, create=False)
        else:
            size = int(np.prod(shape)) * np.dtype(dtype).itemsize
            self._shm = SharedMemory(create=True, size=size)

        self._ndarray = np.ndarray(shape, dtype=dtype, buffer=self._shm.buf)

    @classmethod
    def from_numpy(cls, ndarray: np.ndarray):
        arr = cls(ndarray.shape, ndarray.dtype)
        arr._ndarray[:] = ndarray[:]
        return arr

    def numpy(self) -> np.ndarray:
        return self._ndarray

    def clone(self) -> np.ndarray:
        arr = np.ndarray(self._shape, dtype=self._dtype)
        arr[:] = self._ndarray[:]
        return arr

    def close(self) -> None:
        self._shm.close()

    def unlink(self) -> None:
        self._shm.unlink()

    def __del__(self):
        self._shm.close()

    def __getstate__(self):
        return self._shape, self._dtype, self._shm.name

    def __setstate__(self, state):
        self.__init__(*state)


def from_numpy(arr: np.ndarray) -> SharedNDArray:
    return SharedNDArray.from_numpy(arr)
