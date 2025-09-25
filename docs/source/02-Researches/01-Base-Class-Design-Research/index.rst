.. _-Base-Class-Design-Research:

Base Class Design Research
==============================================================================


Background
------------------------------------------------------------------------------
在将 Boto3 API Response 从 TypedDict 转换为 DataClass 的项目中, 我们面临一个关键的设计决策: 如何设计一个稳定, 高效且具有良好类型提示支持的基础数据类结构.

项目的核心目标是让开发者在使用 AWS API 响应时获得完整的 IDE 类型提示支持, 同时确保:

- Constructor 的稳定性和一致性
- 对嵌套结构 (Nested Structure) 的良好支持
- 属性为其他 DataClass 时的正确解析
- 属性为 DataClass 列表时的正确解析
- 尽可能小的内存占用和运行时开销


Research Process
------------------------------------------------------------------------------
为了找到最佳的设计方案, 我们进行了三个阶段的研究和实验.


Example 1: Generic Base Class Approach
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
第一个尝试是使用泛型(Generic)来标注 Base 类的 ``_data`` 属性类型.

.. dropdown:: ./example1.py

.. literalinclude:: ./example1.py
:language: python
:linenos:

**研究发现:**

- 由于 Generic[] 中的类型需要从 stub 文件导入, 必须放在 ``TYPE_CHECKING`` 保护下
- 使用双引号包裹的类型导致 Generic 无法正常工作
- ``make_one`` 方法的类型提示失效
- 虽然实例方法和 ``raw_data`` 属性的类型提示正常工作, 但构造函数的类型提示存在问题


Example 2: Non-Generic Base Class Approach
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
第二个尝试是去掉 Generic, 使用普通的基类设计.

.. dropdown:: ./example2.py

.. literalinclude:: ./example2.py
    :language: python
    :linenos:

**研究发现:**

- 当 factory classmethod 直接返回 ``cls()`` 时, 子类无需重写也能获得正确的类型提示
- 但是在其他情况下(如 list comprehension), 类型提示会丢失
- 需要在子类中重写 ``make_many`` 方法才能保持类型提示
- 增加了代码复杂度和维护成本


Final Decision: Simple Frozen DataClass
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
基于前两个实验的经验, 我们做出了最终决策: 不使用任何复杂的基类继承设计.

.. dropdown:: ./my_decision.py

.. literalinclude:: ./my_decision.py
    :language: python
    :linenos:

**最终方案特点:**

- 每个 DataClass 都是独立的, 不依赖继承
- 使用 ``frozen=True`` 确保数据不可变性
- 统一的接口设计, 每个类都包含:

- ``boto3_raw_data: "TypeDef"`` 字段存储原始数据
- ``make_one`` 类方法处理单个对象创建
- ``make_many`` 类方法处理批量对象创建

- 完美的类型提示支持, 包括:

- 实例方法的类型提示
- 属性访问的类型提示
- 原始数据字典键的类型检查


Conclusion
------------------------------------------------------------------------------
通过这次研究, 我们确定了最简单且最有效的设计方案. 虽然放弃了基类继承可能会增加一些代码重复, 但换来的是:

1. **稳定的类型提示**: 所有场景下都能获得完整的 IDE 支持
2. **简单的结构**: 没有复杂的继承关系, 易于理解和维护
3. **一致的接口**: 统一的 ``make_one`` 和 ``make_many`` 方法
4. **高性能**: 没有额外的继承开销

这个设计决策为整个项目的后续开发奠定了坚实的基础, 确保了代码的可维护性和开发者体验的一致性.
