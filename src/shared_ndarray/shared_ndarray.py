import numpy as np
from typing import Optional, List
from multiprocessing.shared_memory import SharedMemory

"""
reference project:

- <https://github.com/dillonalaird/shared_numpy>
- <https://github.com/crowsonkb/shared_ndarray>
- <https://github.com/meersuri/PySMArray>

- <https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html>


- <https://pytorch.org/docs/stable/multiprocessing.html>
- <https://github.com/pytorch/pytorch/blob/main/torch/multiprocessing/queue.py>

- <https://github.com/apache/mxnet/blob/master/python/mxnet/gluon/data/dataloader.py>

"""


class Meta:
    def __init__(self, key, shape, dtype, nbytes, start_pos):
        self.key = key
        self.shape = shape
        self.dtype = dtype
        self.nbytes = nbytes
        self.start_pos = start_pos


class SharedNDArray:
    def __init__(self, meta_list: List[Meta], name: Optional[str] = None) -> None:

        self._meta_list = meta_list
        total_size = sum(meta.nbytes for meta in self._meta_list)

        if name:
            self._shm = SharedMemory(name=name, create=False)
        else:
            self._shm = SharedMemory(create=True, size=total_size)

    @classmethod
    def from_numpy(cls, arr: Optional[np.ndarray] = None, **kwargs) -> "SharedNDArray":
        # kwargs can not have default key
        if "default" in kwargs.keys():
            raise ValueError("default key is reserved")

        # default
        if arr is not None:
            kwargs["default"] = arr

        # key, value
        meta_list: List[Meta] = []
        start_pos = 0
        for key, value in kwargs.items():
            if not isinstance(value, np.ndarray):
                raise ValueError(f"{key} must be numpy.ndarray")
            meta_list.append(Meta(key, value.shape, value.dtype, value.nbytes, start_pos))
            start_pos += value.nbytes

        arr = cls(meta_list)

        for key, value in kwargs.items():
            for meta in meta_list:
                if meta.key == key:
                    arr._shm.buf[meta.start_pos:meta.start_pos + value.nbytes] = value.tobytes()
        return arr

    def get(self, key: str = "default") -> bytes:
        for meta in self._meta_list:
            if meta.key == key:
                return bytes(self._shm.buf[meta.start_pos:meta.start_pos + meta.nbytes])

    def set(self, key: str, new_arr: np.ndarray) -> None:
        for meta in self._meta_list:
            if meta.key == key:
                if meta.nbytes != new_arr.nbytes:
                    raise ValueError("new_arr size must be same as original size")
                self._shm.buf[meta.start_pos:meta.start_pos + meta.nbytes] = new_arr.tobytes()

    def get_numpy(self, key: str = "default") -> np.ndarray:
        for meta in self._meta_list:
            if meta.key == key:
                return np.ndarray(meta.shape, dtype=meta.dtype,
                                  buffer=self._shm.buf[meta.start_pos:meta.start_pos + meta.nbytes])

    def clone_numpy(self, key: str = "default") -> np.ndarray:
        sh_arr = self.get_numpy(key)
        arr = np.ndarray(sh_arr.shape, dtype=sh_arr.dtype)
        arr[:] = sh_arr[:]
        return arr

    def close(self) -> None:
        self._shm.close()

    def unlink(self) -> None:
        self._shm.unlink()

    def __del__(self):
        self._shm.close()

    def __getstate__(self):
        return (self._meta_list,
                self._shm.name)

    def __setstate__(self, state):
        self.__init__(*state)


def from_numpy(arr: Optional[np.ndarray] = None, **kwargs) -> SharedNDArray:
    return SharedNDArray.from_numpy(arr, **kwargs)
