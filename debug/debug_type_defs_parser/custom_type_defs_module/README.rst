Type Definitions Parser Testing Module
==============================================================================


Overview
------------------------------------------------------------------------------
这个测试模块基于精心设计的简短测试数据来验证 TypeDefs Parser 的功能. 测试使用了 `boto3_dataclass/tests/gen_code/type_defs.pyi <https://github.com/MacHu-GWU/boto3_dataclass-project/blob/main/boto3_dataclass/tests/gen_code/type_defs.pyi>`_ 文件作为输入源, 并通过手动建模的 `boto3_dataclass/tests/gen_code/typed_dict_def_mapping.py <https://github.com/MacHu-GWU/boto3_dataclass-project/blob/main/boto3_dataclass/tests/gen_code/typed_dict_def_mapping.py>`_ 文件来对比测试结果.


Test Data Foundation
------------------------------------------------------------------------------
**Base Test File**: `boto3_dataclass/tests/gen_code/type_defs.pyi <https://github.com/MacHu-GWU/boto3_dataclass-project/blob/main/boto3_dataclass/tests/gen_code/type_defs.pyi>`_

这个文件包含了精心设计的 TypedDict 定义, 涵盖了以下测试场景:

- **SimpleModelTypeDef**: 基本的单属性模型
- **SimpleModelWithSubscriptTypeDef**: 包含 ``Required``, ``NotRequired`` 和 ``List`` 类型注解的模型
- **SimpleModelWithNestedSubscriptTypeDef**: 嵌套的 ``Required[List[str]]`` 和 ``NotRequired[List[str]]`` 类型
- **SimpleContainerTypeDef**: 包含嵌套 TypedDict 对象的复杂容器类型
- **UserTypeDef**: 使用函数式定义的 TypedDict (通过 ``TypedDict("UserTypeDef", {...})``)

**Manual Data Modeling**: `boto3_dataclass/tests/gen_code/typed_dict_def_mapping.py <https://github.com/MacHu-GWU/boto3_dataclass-project/blob/main/boto3_dataclass/tests/gen_code/typed_dict_def_mapping.py>`_

手动创建的数据模型, 不依赖 parser, 直接使用项目的数据模型类来定义相同的结构, 用作对比基准.


Testing Approach
------------------------------------------------------------------------------
测试采用了三种不同的代码生成方式来验证一致性:


**1. Human Written Module**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``module_1_from_human_written.py`` 完全手写的数据类实现, 展示了理想的代码结构和最佳实践:

- 使用 ``field()`` 函数优化简单属性访问
- 对嵌套对象使用完整的 ``@cached_property`` 实现
- 包含详细的类型注解处理规则注释:

- 不对 ``NotRequired`` 和 ``Required`` 进行特殊处理
- 如果尝试访问不存在的 ``NotRequired`` 属性, 应该抛出 ``KeyError``
- 对于 ``Optional`` 类型, 直接访问即可 (字段必须存在, 但值可以是 None)
- 对于 ``List`` 类型使用 ``make_many`` 方法, 单个对象使用 ``make_one`` 方法


**2. Generated from Pre-built Type Definitions**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``module_2_from_pre_build_type_defs_module.py`` 通过 ``test_1_gen_code_from_pre_build_type_defs_module.py`` 生成:

.. dropdown:: test_1_gen_code_from_pre_build_type_defs_module.py

    .. literalinclude:: ./test_1_gen_code_from_pre_build_type_defs_module.py
       :language: python
       :linenos:

这种方式使用手动建模的数据结构来生成代码, 验证了代码生成器的正确性.


**3. Generated from Parser**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``module_3_from_parser.py`` 通过 ``test_2_gen_code_from_parser.py`` 生成:

.. dropdown:: test_2_gen_code_from_parser.py

    .. literalinclude:: ./test_2_gen_code_from_parser.py
       :language: python
       :linenos:

这是最关键的测试, 验证 parser 能否正确解析 ``.pyi`` 文件并生成与手动版本一致的代码.


Test Execution and Validation
------------------------------------------------------------------------------
**Runtime Testing**: ``test_3_use_generated_module.py``

实际运行测试, 导入生成的模块并验证:

- **Type Hint Support**: 所有属性访问都应该有正确的类型提示
- **Data Access**: 能够正确访问嵌套数据和列表数据
- **Error Handling**: ``NotRequired`` 字段的错误处理行为
- **Object Creation**: ``make_one`` 和 ``make_many`` 方法的正确性

测试覆盖了不同的数据访问模式:

.. dropdown:: test_3_use_generated_module.py

    .. literalinclude:: ./test_3_use_generated_module.py
       :language: python
       :linenos:


Key Testing Scenarios
------------------------------------------------------------------------------
**Type Annotation Handling**:

- ``Required[T]`` vs ``NotRequired[T]`` 的正确解析
- ``Optional[T]`` 类型的处理
- ``List[T]`` 和嵌套列表类型的支持
- 复杂的组合类型如 ``Required[Optional[T]]`` 和 ``NotRequired[List[T]]``

**Nested Object Processing**:

- 嵌套 TypedDict 对象的识别和处理
- 自动生成合适的 ``make_one`` 和 ``make_many`` 调用
- 类型依赖关系的正确解析

**Code Generation Consistency**:

通过比较三个模块的生成结果, 确保:
- Parser 解析的准确性
- 代码生成器的一致性
- 手动建模与自动解析的对等性


Results and Benefits
------------------------------------------------------------------------------
这个测试模块提供了:

1. **Complete Validation Pipeline**: 从 ``.pyi`` 文件解析到最终代码生成的完整验证
2. **Multi-approach Comparison**: 三种不同生成方式的对比, 确保结果一致性
3. **Edge Case Coverage**: 覆盖各种复杂的 TypedDict 定义模式
4. **Runtime Verification**: 实际运行测试确保生成的代码功能正确
5. **Type Safety Validation**: 验证生成的代码保持完整的类型提示支持

这个测试框架为项目的核心解析和代码生成功能提供了可靠的验证基础, 确保在处理真实的 AWS Boto3 API 定义时能够产生正确, 高质量的 DataClass 代码.
