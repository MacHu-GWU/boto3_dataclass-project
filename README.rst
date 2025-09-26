
.. image:: https://readthedocs.org/projects/boto3-dataclass/badge/?version=latest
    :target: https://boto3-dataclass.readthedocs.io/en/latest/
    :alt: Documentation Status

.. .. image:: https://github.com/MacHu-GWU/boto3_dataclass-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/boto3_dataclass-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/boto3_dataclass-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/boto3_dataclass-project

.. image:: https://img.shields.io/pypi/v/boto3-dataclass.svg
    :target: https://pypi.python.org/pypi/boto3-dataclass

.. image:: https://img.shields.io/pypi/l/boto3-dataclass.svg
    :target: https://pypi.python.org/pypi/boto3-dataclass

.. image:: https://img.shields.io/pypi/pyversions/boto3-dataclass.svg
    :target: https://pypi.python.org/pypi/boto3-dataclass

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/boto3_dataclass-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/boto3_dataclass-project

------

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://boto3-dataclass.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/boto3_dataclass-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/boto3_dataclass-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/boto3_dataclass-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/boto3-dataclass#files


🚀 boto3-dataclass: Transform Your boto3 Experience
==============================================================================
.. image:: https://boto3-dataclass.readthedocs.io/en/latest/_static/boto3_dataclass-logo.png
    :target: https://boto3-dataclass.readthedocs.io/en/latest/

📚READ `FULL DOCUMENTATION HERE <https://boto3-dataclass.readthedocs.io/en/latest/>`_

Welcome to **boto3-dataclass**! This library transforms boring boto3 dictionaries into beautiful, type-safe dataclasses with full autocomplete support. Say goodbye to ``response['Key']['SubKey']`` and hello to ``response.Key.SubKey`` with full IDE support!

.. _install:

📦 Installation
------------------------------------------------------------------------------

Install the service you need (e.g., for IAM, S3):

.. code-block:: console

    $ pip install boto3-dataclass[iam,s3]

Or match with your boto3 version:

.. code-block:: console

    $ pip install "boto3-dataclass[iam,s3]>=1.40.0,<1.41.0"

Or install everything at once:

.. code-block:: console

    $ pip install boto3-dataclass[all]  # Installs all AWS services

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade boto3-dataclass
