from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import sys

setup(
  name='batch_jaro_winkler',
  version='0.1.1',
  description='Fast batch jaro winkler distance implementation in C99.',
  long_description='This project gets its performance from the pre-calculation of an optimized model in advance of the actual runtime calculations. Supports any encoding.',
  author='Dominik Bousquet',
  author_email='bousquet.dominik@gmail.com',
  url='https://github.com/dbousque/batch_jaro_winkler',
  license='MIT',
  # I know, doesn't work but I don't want to use setuptools. Won't compile if < 3.3 anyway.
  install_requires=["setuptools", "wheel", "Cython"],
  python_requires='>=3.6',
  zip_safe = False,
  include_package_data = True,
  package_dir= {'': 'src'},
  ext_modules=[Extension('batch_jaro_winkler', ['src/cbatch_jaro_winkler.c', 'src/ext/batch_jaro_winkler.c'], language='c')]
)
