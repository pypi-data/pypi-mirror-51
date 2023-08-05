===========
Development
===========

The main addition to this user interface would be the addition of a new camera
interface. This consists of the following steps.

#. Add a new class to the ``camera`` package with a name like ``BlahCamera``
   and inherit from ``BaseCamera``.
#. Fill out the required interface functions present in the ``BaseCamera`` class.
#. Add unit tests for camera if possible. This can only happen if the interface package
   is ``pip`` installable and does not require a hardware connection to work.
#. Add a configuration panel (if necessary) to the ``views`` package.
#. Add the first part of the camera class name (``Blah`` in this example) to the
   ``names`` list in ``__init__.py`` of the ``camera`` package.

If the interface package for the new camera is available to the UI, it will now show up in 
the list of camera choices. Continuing this example, a ``Blah`` menu entry would appear in
the ``Camera`` menu of the UI.
