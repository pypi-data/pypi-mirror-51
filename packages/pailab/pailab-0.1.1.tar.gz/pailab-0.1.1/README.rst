|version|_ |Docs|_ |Travis|_ |Codecov|_ |License|_

.. |Travis| image:: https://travis-ci.org/pailabteam/pailab.svg?branch=develop
.. _Travis: https://travis-ci.org/pailabteam/pailab

.. |Codecov| image:: https://codecov.io/gh/pailabteam/pailab/branch/develop/graph/badge.svg
.. _Codecov:  https://codecov.io/gh/pailabteam/pailab

.. |Docs| image:: https://readthedocs.org/projects/pailab/badge/?version=latest
.. _Docs: https://pailab.readthedocs.io/en/latest/?badge=latest

.. |License| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
.. _License: https://opensource.org/licenses/Apache-2.0

.. |version| image:: https://img.shields.io/badge/pailab-beta-yellow.svg
.. _version: https://github.com/pailabteam/pailab


.. |frontmark| image:: https://img.shields.io/badge/powered%20by-frontmark-lightgrey.svg
.. _frontmark: https://www.frontmark.de/

.. |rivacon| image:: https://img.shields.io/badge/powered%20by-RIVACON-lightgrey.svg
.. _rivacon: https://www.rivacon.com/en/


.. |logo| image:: images/monster.png
    :height: 100
    :alt: pailab

|logo| pailab
==============
pailab is an integrated machine learning workbench to version, analyze and automatize the machine learning model building processes and deployments.
It keeps track of changes in your machine learning pipeline (code, data, parameters) similar to classical 
version control systems considering special characteristics of AI model building processes. 

It provides:

- Versioning of all objects of the ML development cycle
- Full transparency over the whole ML development cycle
- Support to work in a team on the same AI projects, sharing data, algorithms and results
- Consistency checks across the whole pipeline
- Distributed execution of parallel jobs, e.g. for parameter studies
- Standardized analysis plots
- Jupyter widgets to administrate and control the ML repo


Al objects added to the repository are split into a part containing big data and a part with the remaining 
data handling them separately with different technqiues. For example
one may use git to administrate the remaining data part. It also adds information to each object such as
the version, the author, date etc. and each object is labeled with a category defining the role in the ml process. 


|frontmark|_ |rivacon|_
