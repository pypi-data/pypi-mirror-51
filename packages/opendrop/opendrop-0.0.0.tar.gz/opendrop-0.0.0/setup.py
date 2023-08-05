from codecs import open
from os.path import abspath, dirname, join
from setuptools import find_packages, setup

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='opendrop',
    version="0.0.0",
    python_requires='>=3.6',
    description='An open Apple AirDrop implementation',
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    url='https://owlink.org',
    author='Milan Stute, Alexander Heinrich',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(),
    keywords='cli',
)
