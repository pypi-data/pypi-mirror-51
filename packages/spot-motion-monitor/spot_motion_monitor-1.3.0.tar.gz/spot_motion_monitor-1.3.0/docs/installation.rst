============
Installation
============

At the command line either via easy_install or pip::

    $ easy_install spot_motion_monitor
    $ pip install spot_motion_monitor

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv spot_motion_monitor
    $ pip install spot_motion_monitor

Once you have installed the package, the provided Gaussian camera provides 
a nice way to explore the interface. However, it was designed for use with a
real camera system. The one supported by this interface is the 
`Allied Vision Technologies <https://www.alliedvision.com/en/digital-industrial-camera-solutions.html>`_ Prosilica GigE cameras. Once the supporting libraries are installed, the installed ``pymba`` package
will function correctly and allow the UI to function with a Prosilica GigE camera. The UI currently
uses version 0.3.1 of the ``pymba`` package.
