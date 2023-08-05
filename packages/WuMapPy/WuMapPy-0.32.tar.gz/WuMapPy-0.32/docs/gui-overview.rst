.. _chap-gui-overview-wumappy:

GUI Overview
************

.. _chap-main-window-wumappy:

Main Window
===========

+-------------------------------------------------+
|                                                 |
| .. figure:: _static/figMainWindowWithMenus.png  |
|    :align: center                               |
|                                                 |
+-------------------------------------------------+

From the main window you can access the :ref:`chap-main-files-wumappy`, :ref:`Settings <chap-main-settings-wumappy>` and :ref:`Help <chap-main-help-wumappy>` menus. From there you can:

 - Open processed data or :ref:`Import new data from ascii files <chap-import-from-ascii-wumappy>`.
 - Import or :ref:`chap-open-geoposet-wumappy` files.
 - Change the GUI :ref:`chap-main-settings-lang-wumappy`, :ref:`chap-main-settings-font-wumappy` and others :ref:`chap-main-settings-misc-wumappy`.
 - Access the GUI :ref:`Help and  documentation <chap-main-help-wumappy>`.


.. _chap-main-files-wumappy:

Files
+++++

+---------------------------------------------------------------------------------+-------------------------------------------------+
|From the file menu you can:                                                      |                                                 |
| * Open a Data Set file (*.nc*, NetCDF);                                         | .. figure:: _static/figMainWindowFilesMenu.png  |
| * :ref:`Import data from (X,Y,Z) ascii files <chap-import-from-ascii-wumappy>`; |    :width: 4cm                                  |
| * Open a Geographic Positions Set (*.netcdf*);                                  |    :align: center                               |
| * Import a shapefile (*.shp*).                                                  |                                                 |
+---------------------------------------------------------------------------------+-------------------------------------------------+

Settings
++++++++

+-----------------------------------------+---------------------------------------------------+
|From the file menu you can:              |                                                   |
| * Change the GUI Language;              | .. figure:: _static/figMainWindowSettingsMenu.png |
| * Change the GUI Font;                  |    :width: 4cm                                    |
| * Change others Miscellaneous Settings: |    :align: center                                 | 
|                                         |                                                   | 
|    * GUI auto update                    |                                                   | 
|    * GUI GroubBox/Tab layout            |                                                   | 
+-----------------------------------------+---------------------------------------------------+

Help
++++

+------------------------------------------------------+------------------------------------------------+
|From the file menu you can:                           |                                                |
| * WuMapPy and GeophPy versions number;               | .. figure:: _static/figMainWindowHelpMenu.png  |
| * WuMapPy and GeophPy documentations in html or pdf. |    :width: 6cm                                 |
|                                                      |    :align: center                              |
|                                                      |                                                |
+------------------------------------------------------+------------------------------------------------+

.. _chap-dataset-window-wumappy:

Dataset Window
==============

+---------------------------------------------------+
|                                                   |
| .. figure:: _static/figDataSetWindow.png          |
|    :width: 12cm                                   |
|    :align: center                                 |
|                                                   |
+---------------------------------------------------+

Once opened, a DataSet is displayed in a window with a menu bar that contains the different available options:

.. hlist::
   :columns: 2

   * :ref:`chap-datasetwin-files-wumappy` (save and export the data)
   * :ref:`chap-datasetwin-disp-wumappy`
   * :ref:`chap-datasetwin-genproc-wumappy` (general processings)
   * :ref:`chap-datasetwin-magproc-wumappy`
   * :ref:`chap-georef-wumappy`
   * :ref:`chap-main-settings-misc-wumappy`

.. _chap-datasetwin-files-wumappy:

Files
+++++

+----------------------------------------------+----------------------------------------------------+
|From the *Files* menu you can:                |                                                    |
| * Close the current dataset;                 | .. figure:: _static/figDataSetWindowFilesMenu.png  |
| * Save the dataset in a netcdf file format ; |    :width: 6cm                                     |
| * Export the dataset in several formats.     |    :align: center                                  |
|                                              |                                                    |
+----------------------------------------------+----------------------------------------------------+

.. _chap-datasetwin-disp-wumappy:

Display Settings
++++++++++++++++

.. |disp1| image:: _static/figDataSetDisplaySettingsDlgBox.png
   :height: 8cm
   :align: middle

With this menu, it's possible to changes the DataSet display options (colormap, axis, value limits, ...)

+---------+
| |disp1| |
+---------+

.. _chap-datasetwin-oper-wumappy:

Operations
++++++++++

This menu gives access to all the :ref:`General Operations <chap-genop-wumappy>` on datasets available in WuMapPy:

+------------------------------------+---------------------------------------------------------+
|From the Operations menu you can:   |                                                         | 
| * Get the dataset informations;    | .. figure:: _static/figDataSetWindowOperationsMenu.png  |
| * Transfrom the data geometry;     |    :width: 4cm                                          |
| * Apply basic math to the dataset; |    :align: center                                       |
| * Clip and Digitize the dataset;   |                                                         |
+------------------------------------+---------------------------------------------------------+

.. _chap-datasetwin-genproc-wumappy:

Processing
++++++++++

This menu gives access to all the :ref:`General Processing <chap-genproc-wumappy>` available in WuMapPy.

+---------------------------------------------+---------------------------------------------------------+
|From the Processing menu you can:            |                                                         | 
| * :ref:`chap-genproc-threshold-wumappy`;    | .. figure:: _static/figDataSetWindowProcessingMenu.png  |
| * :ref:`chap-genproc-peakfilt-wumappy`;     |    :width: 4cm                                          |
| * :ref:`chap-genproc-zeromeanfilt-wumappy`; |    :align: center                                       |
| * :ref:`chap-genproc-medfilt-wumappy`;      |                                                         |
| * :ref:`chap-genproc-festoonfilt-wumappy`;  |                                                         |
| * :ref:`chap-genproc-regtrend-wumappy`;     |                                                         |
| * :ref:`chap-genproc-wallisfilt-wumappy`;   |                                                         |
| * :ref:`chap-genproc-ploughfilt-wumappy`;   |                                                         |
| * :ref:`chap-genproc-condestrip-wumappy`;   |                                                         |
| * :ref:`chap-genproc-curvdestrip-wumappy`;  |                                                         |
+---------------------------------------------+---------------------------------------------------------+

.. _chap-datasetwin-magproc-wumappy:

Magnetic Processing
+++++++++++++++++++

This menu gives acces to all the :ref:`Magnetic Processing <chap-magproc-wumappy>` available in WuMapPy:

+--------------------------------------------+-----------------------------------------------------------------+
|From the Magnetic processing menu you can:  |                                                                 | 
| * :ref:`chap-magproc-log-wumappy`;         | .. figure:: _static/figDataSetWindowMagneticProcessingMenu.png  |
| * :ref:`chap-magproc-polred-wumappy`;      |    :width: 6cm                                                  |
| * :ref:`chap-magproc-cont-wumappy`;        |    :align: center                                               |
| * :ref:`chap-magproc-anasig-wumappy`;      |                                                                 |
| * :ref:`chap-magproc-magstratum-wumappy`;  |                                                                 |
| * :ref:`chap-magproc-totgradconv-wumappy`; |                                                                 |
| * :ref:`chap-magproc-eulerdeconv-wumappy`; |                                                                 |
+--------------------------------------------+-----------------------------------------------------------------+

.. _chap-datasetwin-georef-wumappy:

Georeferencing
++++++++++++++

Dataset georeferencing using a set of Ground Control Points (GCPs). 
Available only if a Geographic Positions Set is opened and displayed.

+--------------------------------------------+-----------------------------------------------------------------+
|From the georeferencing menu you can:       |                                                                 | 
| * georeference a dataset with GCPs.        | .. figure:: _static/figDataSetGeoReferencingMenu.png            |
|                                            |    :width: 6cm                                                  |
|                                            |    :align: center                                               |
|                                            |                                                                 |
+--------------------------------------------+-----------------------------------------------------------------+


.. _chap-datasetwin-misc-wumappy:

Miscellaneous Settings
++++++++++++++++++++++

It is a simple duplicate of the Main window's :ref:`chap-main-settings-misc-wumappy`. 

+---------------------------------------------------+
|                                                   | 
| .. figure:: _static/figDataSetWindowMiscMenu.png  |
|    :width: 6cm                                    |
|    :align: center                                 |
|                                                   |
+---------------------------------------------------+


Geographic set Window
=====================

+---------------------------------------------------+
|                                                   |
| .. figure:: _static/figGeoPosSetWindow.png        |
|    :width: 12cm                                   |
|    :align: center                                 |
|                                                   |
+---------------------------------------------------+

Once opened, a Geographic Positions Set is displayed in a window with a menubar that contains the different available options:

* Files
   To save and export the Geographic Positions Set
   
   .. image:: _static/figGeoPosSetWindowFilesMenu.png
 
* Configuration
   To edit the Geographic Positions Set
   
   .. image:: _static/figGeoPosSetConfigDlgBox.png



