import numpy as np
from typing import Optional
from multiprocessing.shared_memory import SharedMemory

class SharedNDArray:
    _meta_list: list
    _shm: SharedMemory

    def __init__(self, meta_list: list, name: Optional[str] = None) -> None:
        """Creates a new SharedNDArray.

        Args:
            meta_list: list of Meta.
            name: Optional; the filesystem path of the shared memory.

        Returns:
            A new SharedNDArray of the given shape and dtype and backed by the given optional name.
        """
        ...

    @classmethod
    def from_numpy(cls, arr: Optional[np.ndarray] = None, **kwargs) -> "SharedNDArray": ...

    def get(self, key: str = "default") -> bytes: ...

    def get_numpy(self, key: str = "default") -> np.ndarray: ...

    def clone_numpy(self, key: str = "default") -> np.ndarray: ...

    def set(self, key: str, new_arr: np.ndarray) -> None: ...

    def close(self) -> None: ...

    def unlink(self) -> None: ...

def from_numpy(arr: Optional[np.ndarray] = None, **kwargs) -> SharedNDArray: ...
