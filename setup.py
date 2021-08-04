from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
import sys

setup(
  name='batch_jaro_winkler',
  version='0.0.1',
  description='Fast batch jaro winkler distance implementation in C99.',
  long_description='This project gets its performance from the pre-calculation of an optimized model in advance of the actual runtime calculations. Supports any encoding.',
  author='Dominik Bousquet, Sergiu Buciumas',
  author_email='buciuser@gmail.com',
  url='https://github.com/n1tk/batch_jaro_winkler_new',
  license='MIT',
  install_requires=["setuptools", "Cython"],
  python_requires='>=3.6',
  zip_safe = False,
  include_package_data = True,
  package_dir= {'': 'src'},
  ext_modules=cythonize("src/cbatch_jaro_winkler.pyx")
  #ext_modules=[Extension('batch_jaro_winkler', ['src/cbatch_jaro_winkler.c', 'src/lib/batch_jaro_winkler.c'], language='c')]
)
