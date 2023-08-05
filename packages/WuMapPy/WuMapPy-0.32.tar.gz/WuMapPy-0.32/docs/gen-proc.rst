.. _chap-genproc-wumappy:

General Processing
******************

General processings, not bound to a specific survey method.

.. only:: html

   .. hlist::
      :columns: 3

      * :ref:`chap-genproc-threshold-wumappy`
      * :ref:`chap-genproc-peakfilt-wumappy`
      * :ref:`chap-genproc-medfilt-wumappy`
      * :ref:`chap-genproc-festoonfilt-wumappy`
      * :ref:`chap-genproc-regtrend-wumappy`
      * :ref:`chap-genproc-wallisfilt-wumappy`
      * :ref:`chap-genproc-ploughfilt-wumappy`
      * :ref:`chap-genproc-condestrip-wumappy`
      * :ref:`chap-genproc-curvdestrip-wumappy`

.. note:: 
   For more informations about this processing, see the GeophPy documentation.

.. _chap-genproc-threshold-wumappy:

Peak filtering
==============

... Not Yet Available ...

.. _chap-genproc-peakfilt-wumappy:

Thresholding
============

.. |thrsh| image:: _static/figDataSetThresholdFilteringDlgBox.png
   :height: 8cm
   :align: middle

Data thresholding for values outside of the [*Minimal value*, *Maximal value*] interval.

+---------+
| |thrsh| |
+---------+

.. note:: 
  
    For more details, see the GeophPy package documentation.

.. _chap-genproc-zeromeanfilt-wumappy:


Zero-Mean Traversing
====================

Acquisition profile detrending by removing the mean or median.

Subtracts the mean (or median) of each traverse (profile) in the dataset.

.. note::
   
   This filter is strictly equivalent to the :ref:`constant destriping filter <chap-genproc-condestrip-wumappy>` in configuration *'mono'* sensor, using *'additive'* destriping method and *Nprof=0*:

... To Be Illustrated ...


.. _chap-genproc-medfilt-wumappy:

Median filtering
================

.. |med1| image:: _static/figDataSetMedianFilteringDlgBox.png
   :height: 8cm
   :align: middle

Classic median (salt-and-pepper) filter.

+--------+
| |med1| |
+--------+

.. note:: 
  
    For more details, see the GeophPy package documentation.

.. _chap-genproc-festoonfilt-wumappy:

Festoon filtering
=================

.. |fest1| image:: _static/figDataSetFestoonFilteringDlgBox1.png
   :height: 8cm
   :align: middle

.. |fest2| image:: _static/figDataSetFestoonFilteringDlgBox2.png
   :width: 5cm
   :align: middle

.. |fest3| image:: _static/figDataSetFestoonFilteringDlgBox3.png
   :width: 5cm
   :align: middle

.. |fest4| image:: _static/figDataSetFestoonFilteringDlgBox4.png
   :width: 5cm
   :align: middle

.. |fest5| image:: _static/figDataSetFestoonFilteringDlgBox5.png
   :width: 5cm
   :align: middle

.. |fest6| image:: _static/figDataSetFestoonFilteringDlgBox6.png
   :width: 5cm
   :align: middle

.. |fest7| image:: _static/figDataSetFestoonFilteringDlgBox7.png
   :width: 5cm
   :align: middle

.. |fest8| image:: _static/figDataSetFestoonFilteringDlgBox8.png
   :width: 5cm
   :align: middle

.. |fest9| image:: _static/figDataSetFestoonFilteringDlgBox9.png
   :width: 5.5cm
   :align: middle

.. |fest10| image:: _static/figDataSetFestoonFilteringDlgBox10.png
   :width: 5cm
   :align: middle

.. |fest11| image:: _static/figDataSetFestoonFilteringDlgBox11.png
   :width: 5cm
   :align: middle

.. |fest12| image:: _static/figDataSetFestoonFilteringDlgBox12.png
   :width: 5.5cm
   :align: middle

.. |fest13| image:: _static/figDataSetFestoonFilteringDlgBox13.png
   :width: 5cm
   :align: middle

.. |corr1| image:: _static/figCorrelmapCrosscorr.png
   :width: 6cm
   :align: middle

.. |corr2| image:: _static/figCorrelmapPearson.png
   :width: 6cm
   :align: middle

.. |corr3| image:: _static/figCorrelmapSpearman.png
   :width: 6cm
   :align: middle

.. |corr4| image:: _static/figCorrelmapKendall.png
   :width: 6cm
   :align: middle

The festoon filter (destagger filter) reduces the positionning error along the survey profiles that result in a festoon-like effect.

+---------+
| |fest1| |
+---------+

An optimum shift is estimated based on the correlation of a particular profile and the mean of its surrounding profiles. 
The filter's windows display 3 differents tabs :

.. hlist::
   :columns: 3
   
   * The correlation map,
      +---------+
      | |fest2| |
      +---------+

   * The correlation sum profile, 
      +---------+
      | |fest3| |
      +---------+

   * The filtered data.
      +---------+
      | |fest4| | 
      +---------+

Different options are available:

* **Method** for correlation calculation (Cross-correlation or Pearson and Spearman or Kendall correlation):

   +---------+---------+
   | |corr1| | |corr2| | 
   +---------+---------+
   | |corr3| | |corr4| |
   +---------+---------+

   Due to the extensive computation time, Pearson, Spearman and Kendall correlation method are not computed over the whole shift domain.

   The usage of Cross-correlation is hence recommended. 

* **Uniform** shift throughout the data:

   +---------+---------+---------+
   | |fest5| | |fest6| | |fest7| |
   +---------+---------+---------+

   Return the best average shift for the dataset (based on the correlation sum off the dataset). Can be problematic when the position error is not regular over the dataset.

* **Non uniform** shift (different for each profile):

   +---------+---------+----------+
   | |fest8| | |fest9| | |fest10| |
   +---------+---------+----------+

   Return the best shift for each profile of the dataset (based on the correlation map).

* and required **minimum correlation** value:

   +----------+----------+----------+
   | |fest11| | |fest12| | |fest13| |
   +----------+----------+----------+

   Prevents shifting profiles if correlation value is to low, here is an example for 1 (i.e. no shift allowed).

.. note:: 
  
    For more details, see the GeophPy package documentation.

.. _chap-genproc-regtrend-wumappy:

Regional trend filtering
========================

.. |regtrend1| image:: _static/figDataSetRegTrendDlgBox.png
   :height: 8cm
   :align: middle

Remove the background (or regional response) from a dataset to enhance the features of interest. 

+-------------+
| |regtrend1| |
+-------------+

.. note:: 
  
    For more details, see the GeophPy package documentation.

.. _chap-genproc-wallisfilt-wumappy:

Wallis filtering
================

The Wallis filter is a locally adaptative contrast enhancement filter. 

It is based on the local statistical properties of sub-window in the image.
It adjusts brightness values (grayscale image) in the local window so that the local mean and standard deviation match target values.

.. |wall1| image:: _static/figDataSetWallisFilteringDlgBox.png
   :height: 8cm
   :align: middle

+---------+
| |wall1| |
+---------+

.. note:: 
  
    For more details, see the GeophPy package documentation.

.. _chap-genproc-ploughfilt-wumappy:

Ploughing filtering
===================

Directional filter.

Apply a directional filter to reduce agricultural ploughing effect in the dataset (or any other directional feature).

... To Be Completed ...


.. _chap-genproc-condestrip-wumappy:

Constant destriping
===================

.. |dest0| image:: _static/figDataSetConstantDestripingDlgBox.png
   :height: 8cm
   :align: middle

.. |dest1| image:: _static/figDataSetConstantDestripingDlgBox1.png
   :width: 5cm
   :align: middle

.. |dest2| image:: _static/figDataSetConstantDestripingDlgBox2.png
   :width: 5cm
   :align: middle

.. |dest3| image:: _static/figDataSetConstantDestripingDlgBox3.png
   :width: 5cm
   :align: middle

Acquisition profile detrending by removing a constant value.

Remove from the dataset the strip noise effect arising from profile-to-profile differences in sensor height, orientation, drift or sensitivity (multi-sensors array).
Constant destriping is done using Moment Matching method.

+---------+
| |dest0| |
+---------+

The filter's windows display 3 different tabs:

.. hlist::
   :columns: 3

   * The filtered dataset
      +---------+
      | |dest1| |
      +---------+

   * The mean cross-track profile
      +---------+
      | |dest2| | 
      +---------+

   * The dataset histogram.
      +---------+
      | |dest3| | 
      +---------+

.. note:: 
  
    For more details, see the GeophPy package documentation.

.. _chap-genproc-curvdestrip-wumappy:

Curve destriping
================

.. |curdest0| image:: _static/figDataSetCubicDestripingDlgBox.png
   :height: 8cm
   :align: middle

Acquisition profile detrending by removing a polynomial fit.

Remove from the dataset the strip noise effect by fitting and subtracting a polynomial curve to each profile on the dataset.

+------------+
| |curdest0| |
+------------+

.. note:: 
  
    For more details, see the GeophPy package documentation.