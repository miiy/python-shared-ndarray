# python-shared-ndarray

A pickleable wrapper for sharing numpy ndarray between processes

## Examples

```python
import numpy as np
import shared_ndarray as sn
import multiprocessing as mp

data = np.ones((1920, 1080, 3), dtype=np.uint8)
q = mp.Queue()

# put
arr = sn.from_numpy(data)
q.put(arr)

# get
arr: sn.SharedNDArray = q.get()
arr_copy = arr.clone()
arr.unlink()
```

## build

build in docker

```bash
docker run --rm -it -v $(PWD):/home/python-shared-ndarray python:3.12 bash

pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt
make build  
```

cross compile

not planned to do this

<https://stackoverflow.com/questions/48518055/cross-compile-extension-on-linux-for-windows>
