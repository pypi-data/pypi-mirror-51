EMDA version 1.1
===================

EMDA is a Python library for Electron Microscopy map and model
manipulations. EMDA was developed in Python3 environment, but it also supports Python2.


Dependencies
===================

EMDA has several dependencies in addition to general python modules (e.g. Numpy, Scipy).
They are 
pandas
gemmi
mrcfile
matplotlib
All dependencies will be automatically checked and installed, if necessary during
EMDA installation.


Installing EMDA version 1.1  
===============================

For installation you may need administrator permissions, 
please consult your system administrator if needed.


Installing from binaries:
-----------------------------------------
EMDA can be easily installed using the Python package manager (pip) by executing
pip install emda==1.1
however, installing from binaries is discouraged because this may lead to missing some
important shared libraries depending on the targeted hardware and operating systems.


Installing from source
--------------------------------------------
This is the recommended method of installation of EMDA. 
If you downloaded EMDA tar file then, 
 - go to the directory containing tar file and execute
   'pip install emda-1.1.tar.gz'
That's it. You are ready to go.

After installation, you may check the installation by typing
'emda_test' on your terminal. All tests must pass.


License
=======

EMDA-1.1 comes under Mozilla Public License Version 2.0 licence.
Please look at LICENSE.txt for more details.


Citations
=========

Please contact authors: ranganaw@mrc-lmb.cam.ac.uk,
garib@mrc-lmb.cam.ac.uk


Acknowledgments
===============

Wellcome Trust- Validation tools for Cryo EM grant (208398/Z/17/Z)

This README file was last time modified on 19.08.2019

