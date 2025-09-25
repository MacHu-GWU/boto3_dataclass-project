.. _Cached-Property-Field-Research:

Cached Property Field Research
==============================================================================


Background
------------------------------------------------------------------------------
在将 Boto3 API Response 转换为 DataClass 的项目中, 我们需要为每个字段提供 IDE 自动补全支持. 传统的做法是使用 ``@cached_property`` 装饰器来包装访问方法:

.. code-block:: python

    @cached_property
    def profile(self):
        return self.boto3_raw_data["profile"]


Problem Statement
------------------------------------------------------------------------------
由于项目会根据 TypeHint 生成大量的代码, 每个 ``@cached_property`` 都需要三行代码:

1. ``@cached_property`` 装饰器行
2. ``def property_name(self):`` 方法定义行
3. ``return self.boto3_raw_data["property_name"]`` 返回语句行

考虑到 AWS 服务的复杂性, 单个服务可能有数百个数据类, 每个类可能有几十个属性, 这种重复的模式会产生大量的代码. 如果我们能找到一种方式将这三行代码简化为一行, 就能显著减少整体代码量.


Research Objective
------------------------------------------------------------------------------
研究是否可以将传统的 ``@cached_property`` 模式简化为更简洁的形式:

.. code-block:: python

    profile = field("profile")

这样的简化不仅能减少代码量, 还能提高代码的可读性和维护性.


Implementation and Testing
------------------------------------------------------------------------------
我们实现了一个 ``field()`` 工厂函数来替代传统的 ``@cached_property`` 模式:

.. dropdown:: ./cached_property_field_research.py

.. literalinclude:: ./cached_property_field_research.py
    :language: python
    :linenos:

**核心实现**:

``field()`` 函数创建了一个动态的 ``cached_property``, 它:

- 接受字段名作为参数
- 返回一个 ``cached_property`` 对象
- 内部的 getter 函数从 ``boto3_raw_data`` 中提取对应字段
- 保持与传统方式相同的缓存行为和类型提示支持

**对比测试**:

- ``User1``: 使用传统 ``@cached_property`` 方式 (3 行代码)
- ``User2``: 使用优化后的 ``field()`` 函数 (1 行代码)

两种方式在功能上完全等价, 都能正确提供类型提示和 IDE 自动补全支持.


Results and Impact
------------------------------------------------------------------------------
通过在实际项目中测试这个优化方案, 我们获得了显著的代码减少效果:

**测试数据**:

- 测试文件: ``boto3_dataclass_ec2/type_defs.py``
- 优化前: 84,005 行代码
- 优化后: 59,538 行代码
- **减少: 24,467 行 (29.1% 的代码量优化) **

**优化效果分析**:

1. **代码量减少**: 近 30%的代码行数减少, 显著提高了代码的简洁性
2. **可读性提升**: 单行字段定义比三行方法定义更直观
3. **维护性改善**: 减少了重复代码, 降低了维护成本
4. **生成效率**: 代码生成过程更高效, 生成的文件更小

**性能保持**:

- 运行时行为完全相同
- 缓存机制保持不变
- 类型提示功能完整保留
- IDE 支持无任何损失
