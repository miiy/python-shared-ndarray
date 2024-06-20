import numpy as np
from multiprocessing.shared_memory import SharedMemory


def from_numpy(arr: np.ndarray) -> SharedNDArray: ...


class SharedNDArray:
    _shape: tuple
    _dtype: np.dtype
    _shm: SharedMemory
    _ndarray: np.ndarray

    def __init__(self, shape: tuple, dtype: np.dtype, name: str | None = None) -> None:
        """Creates a new SharedNDArray.

        Args:
            shape: Shape of the wrapped ndarray.
            dtype: Data type of the wrapped ndarray.
            name: Optional; the filesystem path of the shared memory.

        Returns:
            A new SharedNDArray of the given shape and dtype and backed by the given optional name.
        """
        ...

    @classmethod
    def from_numpy(cls, ndarray: np.ndarray) -> "SharedNDArray": ...

    def numpy(self) -> np.ndarray: ...

    def clone(self) -> np.ndarray: ...

    def close(self) -> None: ...

    def unlink(self) -> None: ...
