.. _chap-install-wumappy:

Installation
************

You can install :program:`WuMapPy` as a Python package or a stand-alone version. 
In the former case, a Python (3.x) installation is necessary to install the package.

Using pip
=========

You can install :program:`WuMapPy` directly from the `PyPI`_ repository using ``pip``.

First, make sure you have an up-to-date version of ``pip`` using the command:

    >>>  pip install --upgrade pip
    >>>  or
    >>>  python -m pip install --upgrade pip

Then, install, upgrade (or uninstall) :program:`WuMapPy` directly from `PyPI`_ repository using ``pip`` with these commands:

    >>>  pip install wumappy
    >>>  pip install --upgrade wumappy
    >>>  pip uninstall wumappy

You can also download the zip file "WuMapPy-vx.y" from the `PyPI`_ repository, and from the download folder use:

    >>>  pip install WuMapPy-vx.y.zip

.. _`PyPI`: https://pypi.org/project/WuMapPy/

Building from sources
=====================

Download the zip file "WuMapPy-vx.y" and unzip it. 
Go to the unzipped folder and run the install script with the following command:

    >>>  python setup.py install
    >>>  or
    >>>  python -m setup.py install

Dependencies
============

:program:`WuMapPy` is a GUI for the GeophPy package, it requires:

.. list-table:: 
   :header-rows: 1
   :widths: auto
   :stub-columns: 0
   :align: center

   *  -  Name
      -  Version
      -  Comment
   *  -  GeophPy
      -  3.2 (or greater)
      -  
   *  - Qt binding for Python
      - 
      - PySide, Qt4, Pyside2 or Qt5
   *  -  QT.py
      - 
      - 
   *  -  matplotlib
      -
      -
   *  -  Sphinx
      - 1.4.3 (or greater)
      - 

.. tip:: Failure on :program:`Windows`

   :program:`WuMapPy` uses others Python modules and packages that should be automatically installed. 
   However, the installation of these modules may failed on :program:`Windows` (in the absence of a C++ compiler for instance). 

   They can be installed independently using the useful website: http://www.lfd.uci.edu/~gohlke/pythonlibs/.
   This website provides many popular scientific Python packages precompiled for :program:`Windows` distributions.

   To install a package independently:

   #. Download the precompiled package sources corresponding to your Python version and :program:`Windows` distribution (SomePackage-vx.y-cp3x-cp3xm_winxx.whl);

      .. image:: _static/figInstallWuMapPyPackages.png
                :height: 4cm

   #. In download folder, use a command prompt and install the package using ``pip`` with the name of the downloaded archive:

       >>> python setup.py install SomePackage-vx.y-cp3x-cp3xm_winxx.whl
       >>> or
       >>> python -m setup.py install SomePackage-vx.y-cp3x-cp3xm_winxx.whl

   #. Repeat the process for all packages which installation failed before re-installing :program:`WuMapPy`.

MSI installer
=============

You can install :program:`WuMapPy` as a stand-alone software (no need of a Python distribution) using the msi installer. 

#. Download the "WuMapPy-vx.y-winxx.msi" installer that matches your OS system and double-click on it;

   .. image:: _static/figInstallWuMapPymsi.png
      :height: 1cm

#. Select the installation path

   .. WARNING::

      The installation path must contain **NO SPACE**. 
      Especially not like the default :program:`Windows` *Program Files*.

   .. image:: _static/figInstallWuMapPymsiPath.png
      :height: 6cm

#. Add a :program:`WuMapPy` shortcut to the :program:`Windows` Sart Menu by righ-clicking on the WuMapPy.exe icon the installation folder and selecting *Pin shortcut to Start Menu*:

   .. image:: _static/figInstallWuMapPymsiShortcut.png
      :height: 6cm

Uninstallation
==============

The Python package can simply be uninstalled using ``pip``:

    >>> pip uninstall wumappy
    >>> or
    >>>  python -m pip uninstall wumappy

Or, for the standalone version:

* by right-clicking on the :program:`WuMapPy` shortcut and selecting uninstall

       .. image:: _static/figInstallWuMapPymsiShortcutUninstall.png
          :height: 3cm
 
* via uninstall program provided by :program:`Windows` (*Control Panel/Programs/Uninstall a program*).

       .. image:: _static/figInstallWuMapPymsiUninstall.png
          :height: 6cm
