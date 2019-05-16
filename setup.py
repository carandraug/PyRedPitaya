# -*- coding: utf-8 -*-
import os

from distutils.core import setup
from distutils.command.build import build
from distutils.command.install import install

from PyRedPitaya import __version__

# If we want to overrid the build processe
# For example, to compile de libmonitor and install it
# Install libmonitor only for redpitaya, i.e. when 

build_dir = "monitor/"

def compile_libmonitor():
    cwd = os.getcwd() # get current directory
    try:
        os.chdir(build_dir)
        os.system("make clean")
        os.system("make all")
    finally:
        os.chdir(cwd)

def install_libmonitor(prefix=''):
    cwd = os.getcwd() # get current directory
    try:
        os.chdir(build_dir)
        os.system("make install INSTALL_DIR={prefix}".format(prefix=prefix))
    finally:
        os.chdir(cwd)


class lib_build(build):
    def run(self):
        compile_libmonitor()
        build.run(self)

class lib_install(install):
    def run(self):
        compile_libmonitor()
        install_libmonitor(self.prefix)
#        install.run(self)


cmdclass = {}
cmdclass['lib_build'] = lib_build
cmdclass['lib_install'] = lib_install

long_description = """\
Overview
========

This package provides a library to access the Red Pitaya registers. This library consist of a C library (libmonitor.c) and a ctypes interface on the Python side. 

An object oriented interface to the different application (scope, generator, PID, AMS, ...) is provided. This interface is implemented using Python properties (see usage below) and can quickly be extended to your own application. 

An rpyc server is used in order to communicate with your computer. The interface is the same on the computer as the one on the board.

Installation
============

The process to install PyRedPitaya on the board requires the installation of Python first. See <https://github.com/clade/RedPitaya/tree/master/python>.


To install PyRedPitaya on the computer download the package and run the command:: 

  python setup.py install

or use easy_install::

  easy_install PyRedPitaya


Usage
=====

You need to have Python installed on you Red Pitaya. 

Interactive Python
------------------

Logging onto the redpitaya using ssh, one can start the ipython shell and run :

.. code ::

    from PyRedPitaya.board import RedPitaya

    redpitaya = RedPitaya()

    print redpitaya.ams.temp # Read property
    redpitaya.hk.led = 0b10101010 # Write property


Remote access
-------------

You need to install the PyRedPitaya package on your PC as well as Rpyc: 

..code::

    rpyc_server

On the computer (replace REDPITAYA_IP by the string containing the IP address) : 

.. code::

    from rpyc import connect
    from PyRedPitaya.pc import RedPitaya

    conn = connect(REDPITAYA_IP, port=18861)
    redpitaya = RedPitaya(conn)

    print redpitaya.ams.temp # Read property
    redpitaya.hk.led = 0b10101010 # Write property

    from time import sleep
    from pylab import *

    redpitaya.scope.setup(frequency = 100, trigger_source=1)
    sleep(100E-3)
    plot(redpitaya.scope.times, redpitaya.scope.data_ch1)
    show()

Background script
-----------------

Example to log the FPGA temperature. Copy the following script in a file, make it exacutable and run it in the background. 

.. code::

    #!/usr/bin/python

    from PyRedPitaya.board import RedPitaya
    from time import sleep

    red_pitaya = RedPitaya()

    with open('/tmp/log.txt', 'a') as f:
        while True:
            f.write(str(red_pitaya.ams.temp)+'\n')
            sleep(1)

"""

setup(name='PyRedPitaya',
      version=__version__,
      description='Python utilities for redpitaya',
      author=u'Pierre Cladé',
      author_email='pierre.clade@upmc.fr',
      packages=['PyRedPitaya', 'PyRedPitaya.enum'],
      install_requires=['myhdl', 'rpyc', 'cached_property', 'numpy'],
      cmdclass=cmdclass, 
     )
