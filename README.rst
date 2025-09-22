
.. image:: https://readthedocs.org/projects/boto3-dataclass/badge/?version=latest
    :target: https://boto3-dataclass.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/boto3_dataclass-project/actions/workflows/main.yml/badge.svg
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


Welcome to ``boto3_dataclass`` Documentation
==============================================================================
.. image:: https://boto3-dataclass.readthedocs.io/en/latest/_static/boto3_dataclass-logo.png
    :target: https://boto3-dataclass.readthedocs.io/en/latest/


Overview
------------------------------------------------------------------------------
**boto3-dataclasses** transforms AWS API responses into elegant, type-safe Python dataclasses with zero-overhead initialization and intelligent lazy loading. Instead of validating and transforming data upfront, this library wraps raw AWS responses in lightweight dataclass containers that provide clean attribute-style access while maintaining the original response structure.


Why boto3-dataclasses?
------------------------------------------------------------------------------


Lazy Loading Pattern for Performance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Traditional AWS response handling either forces you to work with raw dictionaries (losing type safety) or requires expensive upfront validation and object construction. boto3-dataclasses introduces a **lazy loading pattern** that gives you the best of both worlds:

- **Instant initialization**: Objects are created with minimal overhead—just a single `_data` assignment
- **On-demand computation**: Nested objects and complex transformations only execute when you actually access them
- **Memory efficiency**: Large AWS responses don't consume unnecessary memory for unused sections
- **Graceful degradation**: If one attribute has issues, all other attributes remain fully functional

.. code-block:: python

    # Traditional approach - all validation/construction happens immediately
    response = ComplexAWSResponse(**raw_data)  # ← Expensive!

    # Lazy loading approach - minimal cost until you need it
    response = DescribeInstancesResponse(_data=raw_data)  # ← Nearly instant
    instances = response.reservations[0].instances  # ← Computation happens here


Automatic Code Generation from boto3-stubs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Rather than manually maintaining AWS service models, boto3-dataclasses **automatically generates all dataclasses by parsing boto3-stubs TypedDict definitions**. This approach provides several key advantages:

- **Always up-to-date**: Generated directly from the same type definitions used by boto3 itself
- **Complete coverage**: Supports all AWS services with their full API surface
- **Type safety guaranteed**: Inherits the same type annotations used by boto3-stubs, ensuring perfect IDE support and mypy compatibility
- **Zero maintenance overhead**: New AWS features and API changes are automatically reflected when you regenerate

The generation process uses Python's AST (Abstract Syntax Tree) to parse `.pyi` stub files, extracting TypedDict definitions and transforming them into equivalent dataclasses with lazy-loading properties. This means every `DescribeInstancesResponseTypeDef` becomes a `DescribeInstancesResponse` dataclass with identical structure but superior ergonomics.


Core Design Philosophy
------------------------------------------------------------------------------
boto3-dataclasses operates on the principle that **AWS APIs return well-formed data that doesn't need validation**—it needs better access patterns. By wrapping responses in lazy-loading dataclasses, you get clean, Pythonic access to your data without the computational overhead of eager validation or transformation. The library acts as a thin, type-safe interface layer that makes AWS responses feel like native Python objects while preserving their original structure and performance characteristics.


.. _install:

Install
------------------------------------------------------------------------------

``boto3_dataclass`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install boto3-dataclass

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade boto3-dataclass
