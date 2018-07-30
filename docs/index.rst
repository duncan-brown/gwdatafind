
##########
GWDataFind
##########

============
Installation
============

.. tabs::

   .. tab:: Pip

      .. code-block:: bash

          $ python -m pip install gwdatafind

      Supported python versions: 2.7, 3.4+.

   .. tab:: Conda

      .. code-block:: bash

          $ conda install -c conda-forge gwdatafind

      Supported python versions: 2.7, 3.5+.

   .. tab:: Debian Linux

      .. code-block:: bash

          $ apt-get install python3-gwdatafind

      Supported python versions: 2.7, 3.4 (Jessie), 3.5 (Stretch), 3.6 (Buster),
      `click here for instructions on how to add the required debian repositories
      <https://wiki.ligo.org/DASWG/SoftwareOnDebian>`__.

   .. tab:: Scientific Linux

      .. code-block:: bash

          $ yum install python-gwdatafind

      Supported python versions: 2.7, `click here for instructions on how to add
      the required yum repositories
      <https://wiki.ligo.org/DASWG/ScientificLinux>`__.

   .. tab:: Macports

      .. code-block:: bash

          $ port install py37-gwdatafind

      Supported python versions: 2.7, 3.6+.

================
Package overview
================

.. automodapi:: gwdatafind
   :no-inheritance-diagram:
   :no-heading:
   :skip: get_default_host
   :skip: find_credential

========
See Also
========

.. toctree::
   :maxdepth: 1

   utils
   migrating
