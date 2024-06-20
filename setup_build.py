from setuptools import setup, find_packages

# cython
from Cython.Build import cythonize
from distutils.core import Extension

extensions = [
    Extension("shared_ndarray.shared_ndarray", ["src/shared_ndarray/shared_ndarray.py"]),
]

setup(
    name="shared_ndarray",
    version="0.1.0",
    package_dir={"": "build"},
    packages=find_packages(where="src"),
    package_data={"shared_ndarray": ["*.so", "*.pyi"]},
    # cython
    ext_modules=cythonize(extensions, language_level=3),
)
