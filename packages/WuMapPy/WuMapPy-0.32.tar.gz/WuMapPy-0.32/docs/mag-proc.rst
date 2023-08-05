.. _chap-magproc-wumappy:

Magnetic Processing
*******************

Processing specific to magnetic survey data.

.. only:: html

   .. hlist::
      :columns: 3

      * :ref:`chap-magproc-log-wumappy`
      * :ref:`chap-magproc-polred-wumappy`
      * :ref:`chap-magproc-cont-wumappy`
      * :ref:`chap-magproc-anasig-wumappy`
      * :ref:`chap-magproc-magstratum-wumappy`
      * :ref:`chap-magproc-totgradconv-wumappy`
      * :ref:`chap-magproc-eulerdeconv-wumappy`


.. _chap-magproc-log-wumappy:

Logarithmic transformation
==========================

The logarithmic transformation is contrast enhancement filter.

Originally used for geological magnetic data, it enhances information present in the data at low-amplitude values while preserving the relative amplitude information via logarithmic transformation procedure.

.. image:: _static/figDataSetLogTransformationDlgBox.png

.. note:: 
   For more informations about this processing, see the GeophPy documentation.

.. _chap-magproc-polred-wumappy:

Pole reduction
==============

Classic reduction to the pole.

The reduction to the magnetic pole is a way to facilitate magnetic data interpretation and comparison. 
It simulates the anomaly that would be measured at the north magnetic pole (inclination of the magnetic field is maximum, i.e. vertical).

.. image:: _static/figDataSetPoleReductionDlgBox.png

.. note:: 
   For more informations about this processing, see the GeophPy documentation.

.. _chap-magproc-cont-wumappy:

Continuation
============

Upward or downward continuation of potential field data (magnetic or gravimetric).

The filter computes the data that would be measured at an upper (`upward continuation`) or lower (`downward continuation`) survey altitude. 
The computation is done in the spectral (frequency) domain using the Fast Fourier Transform.


.. image:: _static/figDataSetContinuationDlgBox.png

.. note:: 
   For more informations about this processing, see the GeophPy documentation.

.. _chap-magproc-anasig-wumappy:

Analytic signal
===============

Computes the 3-D Analytic Signal.

The Analytic Signal (also known as the total gradient magnitude or energy envelope) is a way to ease magnetic source characterization independently from the direction of its magnetization.

.. image:: _static/figDataSetAnalyticSignalDlgBox.png

.. note:: 
   For more informations about this processing, see the GeophPy documentation.

.. _chap-magproc-magstratum-wumappy:

Equivalent stratum magnetic susceptibility
==========================================

.. image:: _static/figDataSetEquivStratumInMagSusceptDlgBox.png

.. note:: 
   For more informations about this processing, see the GeophPy documentation.

.. _chap-magproc-totgradconv-wumappy:

Gradient <-> Total field Conversion
===================================

Conversion between the different sensor's configurations.

Magnetic data are all derived from the same potential and thereby contains in the same information, making theoretical conversion from one sensor configuration to another is possible.


.. image:: _static/figDataSetConversionGradientMagFieldDlgBox.png

.. note:: 
   For more informations about this processing, see the GeophPy documentation.

.. _chap-magproc-eulerdeconv-wumappy:

Euler deconvolution
===================

Classic Euler deconvolution.

Euler deconvolution is a method to estimate the depth of magnetic sources that do not required reduced-to-the-pole data.

.. image:: _static/figDataSetEulerDeconvolutionDlgBox.png

The "Undo" Button allow to cancel the last action.
After having calculated Euler deconvolution for severals zones, it's possible to save these data in a "csv" file (with ';' as delimiter) by clicking on the "Save" button.

.. note:: 
   For more informations about this processing, see the GeophPy documentation.