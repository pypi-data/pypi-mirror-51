.. _configuration:

=============
Configuration
=============

In addition to using the configuration menu from within the user interface, the
program provides a mechanism to insert configuration information into the program
on startup. The ``-c`` or ``--config_file`` flag may be passed to the ``smm_ui`` call.
The flag takes a filename corresponding to a YAML configuration file. The following sections
will describe the currently configurable parameters. Each section corresponds to a section
heading in the YAML configuration file.


General
~~~~~~~

This section, specified by the ``general`` heading, handles modification to the program's
data controller. The following variables are configured under this section.

version
  This represents the version of the configuration file being used. The telemetry system places
  this information in a generated output configuration file. The value should be recorded as a
  string.

telemetry_dir
  This is a path where the resulting telemetry data is to be stored. This parameter can
  be overridden from the command line using the ``-t`` or ``--telemetry_dir`` flag.

remove_telemetry_dir
  By default, the telemetry directory is removed when ROI acquistion is stopped. This flag can be used to override that behavior by setting it to False.

pixel_scale
  This is the sky scale on the camera CCD in units of arcseconds per pixel. This value will
  vary depending on the optical path in front of the CCD camera. 


Full Example
~~~~~~~~~~~~

This section will show a full example of all items that are configurable. The file passed
to the program does not need to contain all of the sections and variables that are shown
here.

::

    general:
      version: '1.0'
      telemetry_dir: /path/to/output/directory
      remove_telemetry_dir: False
      pixel_scale: 0.1
