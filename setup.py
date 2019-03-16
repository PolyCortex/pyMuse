from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyMuse',
    version='0.2',
    description='Python tools and apps associated with Muse headband',
    long_description=long_description,
    url='https://github.com/PolyCortex/pyMuse',
    author='PolyCortex',
    author_email='polycortex@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='muse polycortex fft eeg openbci',
    packages=find_packages(exclude=['contrib', 'docs', 'test']),
    install_requires=['python-osc', 'dataclasses'],
)