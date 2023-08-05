from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
import io
import re

from setuptools import find_packages
from setuptools import setup

setup(
    name = 'rlipy',
    version = '0.4.15',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    py_modules = [splitext(basename(path))[0] for path in glob('src/*.py')],
    description = 'rli common library',
    author = 'Ron Li',
    author_email = 'rli@veritionfund.com',
    install_requires = ['pyzmq',
                      'redis',
		    'pysftp',
                    'pandas',
                    ],
    include_package_data = True,
    tests_require = ['pytest'
                   ],
    # ...,
)
