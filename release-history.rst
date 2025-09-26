.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.40.0 (2025-09-26)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**First release**

- Released master package ``boto3-dataclass`` and 412 per-service packages ``boto3-dataclass-{service_name}`` on PyPI
- Core feature: provides ``{service_name}_caster`` to convert boto3 API responses to type-safe dataclasses
- Transform boring boto3 dictionaries into beautiful dataclasses with full autocomplete support
- Say goodbye to ``response['Key']['SubKey']`` and hello to ``response.Key.SubKey`` with full IDE support
- Supports all AWS services that have mypy-boto3 stubs
- Zero performance overhead with lazy loading
- 100% compatible with existing boto3 code
