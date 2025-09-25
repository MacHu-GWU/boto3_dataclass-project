.. _Boto3-Stubs-Type-Defs-Patterns:

Boto3 Stubs Type Defs Patterns
==============================================================================
在研究如何将 ``mypy_boto3_{service}/type_defs.pyi`` 中的 TypedDict 转换为不可变的 dataclass 之前, 我们先来了解一下里面出现的所有的类型定义的格式和风格, 只要我们的 parser 能处理这些类型定义, 就能处理所有的 AWS 服务.

.. dropdown:: boto3_stubs_type_defs_example.py

    .. literalinclude:: ./boto3_stubs_type_defs_example.py.py
       :language: python
       :linenos:
