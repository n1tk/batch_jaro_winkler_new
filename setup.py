from setuptools import _install_setup_requires, setup, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
from setuptools import find_packages, setup
import sys
from glob import glob

#ext_modules=cythonize("src/cbatch_jaro_winkler.pyx")
#ext_modules=[Extension('batch_jaro_winkler', ['src/cbatch_jaro_winkler.c', 'src/lib/batch_jaro_winkler.c'], include_dirs=["src/lib/"], language='c')]
#['src/cbatch_jaro_winkler.pyx']
#include_dirs = ['src']
#sources = glob('src/*.pyx') #+ glob('src/*.c') + glob('src/lib/*.c')

#ext_modules=[Extension('batch_jaro_winkler',
#                         sources=sources,
#                         include_dirs=include_dirs,
#                         ),
#               ]


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = {
        'msvc': ['/EHsc', '/O2', '/std:c++11', '/W4',
                 # disable some warnings from the Cython code
                 #'/wd4127', # conditional expression is constant
                 #'/wd4100', # '__pyx_self': unreferenced formal parameter
                 #'/wd4505', # unreferenced local function has been removed
                 #'/wd4125', # decimal digit terminates octal escape sequence
                 #'/wd4310', # cast truncates constant value
                 ],
        'unix': ['-O3', '-std=c++11',
                 '-Wextra', '-Wall', '-Wconversion', '-g0',
                 #'-Wno-deprecated-declarations',
                 # the xcode implementation used in the CI has a bug, which causes
                 # this to be thrown even when it is ignored using brackets around the statement
                 #'-Wno-unreachable-code',
                 # this caused issues on the conda forge build
                 #'-Wno-unused-command-line-argument'
                 ],
    }
    l_opts = {
        'msvc': [],
        'unix': [],
    }

    if sys.platform == 'darwin':
        darwin_opts = ['-stdlib=libc++', '-mmacosx-version-min=10.9']
        c_opts['unix'] += darwin_opts
        l_opts['unix'] += darwin_opts

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        if ct == 'unix':
            opts.append('-DVERSION_INFO="%s"' %
                        self.distribution.get_version())
        elif ct == 'msvc':
            opts.append('/DVERSION_INFO=\\"%s\\"' %
                        self.distribution.get_version())
        for ext in self.extensions:
            ext.extra_compile_args += opts
            ext.extra_link_args += link_opts
        build_ext.build_extensions(self)


ext_modules = [
    Extension(
        name='batch_jaro_winkler',
        sources=[
            'src/cbatch_jaro_winkler.c',
            'src/lib/batch_jaro_winkler.c'
        ],
        include_dirs=["src/lib/"],
        language='c',
    )
]


if __name__ == "__main__":
  setup(
      name='batch_jaro_winkler',
      version='0.0.1',
      description='Fast batch jaro winkler distance implementation in C99.',
      long_description='This project gets its performance from the pre-calculation of an optimized model in advance of the actual runtime calculations. Supports any encoding.',
      author='Dominik Bousquet, Sergiu Buciumas',
      author_email='buciuser@gmail.com',
      url='https://github.com/n1tk/batch_jaro_winkler_new',
      license='MIT',
      setup_requires=["cython >=0.20"],
      install_requires=["python >=3.6"],
      python_requires='>=3.6',
      zip_safe=False,
      include_package_data=True,
      package_dir={'': 'src'},
      cmdclass={'build_ext': BuildExt},
      ext_modules=ext_modules  # ext_modules=cythonize(['src/*.pyx'])
  )
