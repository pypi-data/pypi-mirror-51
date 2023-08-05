========
Usage
========

This package is used as the front-end to a Dome Seeing Monitor. It currently 
does not have any useful module imports. 

To run the user interface, do::

    smm_ui

Command-line help can be acquired by doing::

    smm_ui -h

or::

    smm_ui --help

User Interface Description
~~~~~~~~~~~~~~~~~~~~~~~~~~

The user interface is designed to follow a spot on a CCD over time. The centroid of the spot
is calculated on a frame-by-frame basis. The main operational mode for the UI acquires the CCD
frame in a region-of-interest (ROI) mode around the spot. This allows the camera to run at higher
frame rates while still doing the centroid calculation frame-by-frame. The x and y (in pixels) components of the centroid are stored in a buffer after each calculation. The size of the buffer sets the total acquisition time along with the frame rate for the camera. Each time a buffer fills, a set of calculations is performed and the plots and information on the user interface are updated. 

The following sections will describe the sections of the user interface. The user interface looks
like the following when first started (minus the blue lettering) and shows the seven main areas
along with the program menu.

.. image:: _static/ui_annotated.png
  :alt: Annotated User Interface

The plots are made using the `pyqtgraph <http://pyqtgraph.org/>`_ library and have many adjustments available by right-clicking on the particular plot. The user interface also provides some plot configuration as well. More information on that configuration can be found here: PlotConfig_.

The camera is interacted with via the *Camera Control* section. It contains spinners to set
the camera frame rate (FPS or frames per second)and the number of frames kept in the internal program buffer. The *Start/Stop Camera* button controls the startup or shutdown of the currently chosen camera. The *Start/Stop Acquire Frames* button controls frame acquisition from the CCD. The *Acquire ROI* checkbox restricts the camera readout to a 50x50 (default) ROI section around the spot centroid. Once the camera is started and acquiring frames, the current images from the CCD is displayed in the *CCD* plot. The *Show Frames* checkbox turns the *CCD* plot display on and off. With the camera acquiring in ROI mode (the *Acquire ROI* checkbox is checked), the *ROI FPS* and *Buffer Size* spinners are disabled to prevent modification of the buffer information during running. To enable the spinners again, uncheck the *Acquire ROI* checkbox.

While the camera is running, information from the acquired frames is displayed in the *Data Information* section. Not all widgets display information while acquiring full CCD frames. In this mode, only the
*Flux*, *Maximum* and *Centroid* widgets display information. When acquiring in ROI mode, all widgets
are reset until the first buffer fills. Once that happens, the *Updated* widget shows the local time when the information was written to all the widgets. The *Accumulation Period* widget is filled based on the size of the current buffer and the current frame rate of the camera (:math:`T_{Acq} = L\,/ FPS`). The *Flux* widget displays the mean of all the fluxes stored in the buffer. The *Maximum* widget shows the mean of the maximum values stored in the buffer. The *x* and *y* *Centroid* widgets show the mean of the x and y centroid values respectively. The *RMS* widget shows the standard deviation of the x and y centroid values in the buffer times the pixel scale for the optical system. 

The *Save Buffer Data* checkbox in the *Data Information* section can be used to write out the current
buffer being displayed by the widgets. When this option is checked and a buffer is filled and calculated, two HDF5 files are written to the execution directory. One file, called ``smm_centroid_YYYYMMDD_HHMMSS.h5``, writes the *x* and *y* centroid component arrays and the other, called ``smm_psd_YYYYMMDD_HHMMSS.h5``, writes out the currently calculated 1D *x* and *y* power spectrum distributions (see PSD_). The time tag is the current UTC time at file creation. The contents for each file are wrapped into a ``pandas.DataFrame`` and placed as an entry in the file indexed by the UTC time of the data insertion: ``DT_YYYYMMDD_HHMMSS``. More contents are stored in separate time coded entries within the corresponding files. The centroid file also contains an entry for the current camera frame rate.

As soon as the first centroid is calculated in ROI mode, the *1D Centroid* plots begin to update. They plot the pixel position of the frame calculated centroid in both the x and y directions. The plots fill to the right until the buffer is filled. Once that occurs, a new centroid value is plotted on the right while the oldest one on the left is removed. The plot now becomes a rolling buffer.

When a buffer is filled and all the calculations are performed, the *Centroid Scatter* plot is updated with the x, y pairs from the calculated centroids. Positions earlier in the buffer are shown as brighter gray while older one get progressively darker. The *X Projection* and *Y Projection* plots are the respective projections of the scatter plot into histograms for display.

.. _PSD: 

The *1D PSD* and *PSD Waterfall* plots are also updated when a buffer fills. The 1D plot shows the currently calculated power spectrum distribution (PSD) from the buffer. The PSD is calculated via the following.

.. math::
  PSD = \frac{|FFT(C)|^2}{L \times FPS} 

where :math:`C` is the x or y centroid component buffer, :math:`L` is the buffer size and :math:`FPS` is the current camera frame rate. The PSD is made symmetric about zero by adding the values at the corresponding positive and negative frequencies. The zero frequency component is also discarded. The frequency array is calculated via the following.

.. math::
  \nu = \frac{FPS}{L} \times [1, 2, ... L/2]

The waterfall plot shows the current 1D spectrum as a strip at the top of the plot. As more buffers are filled and calculated, the most recent 1D spectrum is placed at the top of the plot and all other rows are moved one level down. Once the allotted number of rows is filled, when a new row is placed at the top of the plot, the row at the bottom will be discarded. The time show on the y axis of the waterfall plot is derived from the acquisition time (:math:`T_{Acq}`) times the total number of rows in the plot. 

The figure below shows a user interface that has been operating long enough to fill the waterfall plot.

.. image:: _static/ui_operating.png
  :alt: Operating User Interface

The program menu offers four entries for further control: *File*, *Camera*, *Config* and *Help*.
The *File* menu only offers one entry: *Exit* which is self explanatory. The *Camera* menu is dynamically created and will be filled based on the camera APIs available to the program. The default camera, *Gaussian* will always have an entry. The currently supported cameras besides that are *Vimba*. This menu allows one to switch back and forth between camera types. The checked entry will be the interface used when the *Start Camera* button is clicked. Also, when the *Start Camera* button is clicked, the *Camera* menu is disabled. It will return to enabled when the *Stop Camera* button is clicked. The *Help* menu provides one entry: *About*. This brings up a dialog with a brief program description and version information.

User Interface Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The *Configure* menu contains the following entries: *Camera*, *Plots* and *General*. Each entry brings up a configuration dialog containing different widgets depending on the chosen entry. The following will detail each of the configuration dialogs. A general note about the entry widgets. Many of them have input validators which will cause the entered value's text to turn blue, the dialog's *OK* button to be disabled or may not allow further typing of a value if that entered value violates the validator. To see the valid range, hover over the particular entry widget to get the details.

.. image:: _static/data_config.png
  :width: 243
  :height: 250
  :align: center
  :alt: Data Configuration Dialog

The *General* configuration dialog has only one widget: *Pixel Scale*. This is the factor that multiplies the standard deviation of the centroid component array to get the value posted in the *RMS* widget in the *Data Information* section. 

The *Camera* configuration entry will bring up a dialog that is dependent on the checked *Camera* entry in the main menu. Each of the currently supported cameras will be shown in turn. When the *Start Camera* button is clicked, the *Camera* configuration entry is disabled. It will return to enabled when the *Stop Camera* button is clicked.

.. image:: _static/gaussian_camera_config.png
  :width: 243
  :height: 250
  :align: center
  :alt: Gaussian Camera Configuration Dialog

This dialog is used for configuring the default Gaussian camera. The *ROI Size* sets the size in pixels of the region around the centroid when in ROI mode. The *Do Spot Oscillation* checkbox controls the movement of the simulated spot on the CCD. If unchecked, the spot will remain in the same location on the CCD. When checked, the spot will move according to the parameters shown in the configuration widgets below and the widgets will be active for modification. The *Amplitude* widgets control the size of the oscillation in each of the two directions and are specified in pixels. The *Frequency* widgets specify the rate of oscillation for both directions. 

.. image:: _static/vimba_camera_config.png
  :width: 243
  :height: 250
  :align: center
  :alt: Vimba Camera Configuration Dialog

This dialog is used for configuring the Vimba class of cameras. The *ROI Size* sets the size in pixels of the region around the centroid when in ROI mode. The *ROI Flux Minimum* sets the lowest acceptable flux for an ROI frame when the flux is summed over the ROI region. The *ROI Exposure Time* widget sets the length of exposure before capturing a CCD frame.

.. _PlotConfig:

The *Plots* sub-menu brings up a tabbed dialog containing configuration of both the centroid and PSD plots. The centroid plot configuration will be covered first followed by the PSD plot configuration.

.. image:: _static/centroid_plots_config.png
  :width: 243
  :height: 398
  :align: center
  :alt: Centroid Plot Configuration Dialog

The *X* and *Y* *1D* widgets control the plots in the *1D Centroid* section of the UI. The *Autoscale* widget contains three settings: ``ON``, ``PARTIAL`` and ``OFF``. If in the ``ON`` selection, the 1D plots will automatically scale on the y axis to any data changes. This will cause all the other configuration widgets associated with the 1D plots to be disabled. If in the ``PARTIAL`` selection, the plots start out in with automatic scaling on the y axis. However, after fifteen frames an average of the y values is obtained and the value in the *Pixel Addition* widget is add and subtracted from that average to set the y axis scale. After that, the y axis remains fixed. In the ``OFF`` state, the y axis scale limits need to be set so the *Minimum* and *Maximum* widgets become active to allow that range to be set. The values in the widgets are then used as the y axis scale in the 1D centroid plots. The last widget, *Num Histogram Bins*, controls the number of histogram bins used in the *X Projection* and *Y Projection* plots. The *Centroid Scatter* plot currently has no configuration associated with it.

.. image:: _static/psd_plots_config.png
  :width: 243
  :height: 398
  :align: center
  :alt: PSD Plot Configuration Dialog

The *Auto Scale 1D* checkboxes control the automatic y axis scaling for each of the *1D PSD* plots. When checked, the y axis will automatically scale to any data changes. If unchecked, the *1D Maximum* widgets will become active. This allows for the maximum y axis value to be specified for plotting. The minimum value of the y axis is set to zero. The *Waterfall Number of Bins* widget is used to set the number of rows kept in the *PSD Waterfall* plots. The *Waterfall Color Map* widget is a drop-down list of color map selections to use for data display on the *PSD Waterfall* plots.

Telemetry
~~~~~~~~~

When the UI is in the acquiring ROI mode and the first buffer is filled, the system
writes out a file containing information that may be of wider interest. LSST will
leverage this information and place it into their Engineering Facilities Database
when the Dome Seeing Monitor is running. By default, the telemetry files show up in
the current running directory under one called ``dsm_telemetry``. A configuration file
or the command-line can be used to specify an alternate directory. See the :ref:`configuration` 
section for more details. Once the UI is no longer in the acquiring ROI mode, all of the
telemetry files are deleted and the telemetry directory removed. If ROI mode is still active and frame acquisition is stopped, the telemetry directory will still be removed as the ROI checkbox is forced to be unchecked. A configuration file setting (see :ref:`configuration`) may be used to stop the telemetry directory from being removed, but the files will still be removed even in this case.

In the telemetry directory, two types of files will be present. One file called
``dsm_ui_config.yaml`` contains the current configuration of the user interface
at the time the telemetry was started. It contains the following information.

timestamp
---------
The time at which the configuration file was created.

ui_versions
-----------

code
  The current version of the user interface.

config
  The version of a specified configuration file. This is ``null`` if no file is used.

config_file
  The filename of a specified configuration file. This is ``null`` if no file is used.

camera
------

name
  This is the general classifier of the camera. Supported names are ``Gaussian`` and
  ``Vimba``

fps
  This is the value for the current frames per second (FPS) setting on the camera.

data
----

buffer_size
  This is the size of the buffer to capture the ROI frame information into.

acquisition_time
  This is the total time it takes to fill a buffer at the above size and FPS


The second file, generally called ``dsm_YYYYMMDD_HHMMSS.dat``, contains the telemetry
information at the time a buffer is filled. The timestamp is the UTC time when
the file was created. The file contains a comma-delimited set of information in the
following order.

  1. The file creation UTC timestamp in ISO format
  #. The UTC time when the first value of the buffer was filled in ISO format
  #. The UTC time when the last value of the buffer was filled in ISO format
  #. The RMS of the centroid in the X direction on the camera in units of arcseconds
  #. The RMS of the centroid in the Y direction on the camera in units of arcseconds

Each time a buffer is filled, a new file is generated.
