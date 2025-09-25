# -*- coding: utf-8 -*-

"""
这个模块负责对 Client 转换器 (Caster) 进行数据建模. 用于将 boto3 原生响应
自动转换为对应的 dataclass 对象.

Caster 模块的作用是提供一个便捷的转换层, 让用户可以无缝地将 boto3 client 的
响应从 TypedDict 格式转换为更易于使用的 dataclass 对象.

例如::

    # 原生 boto3 用法
    client = boto3.client('iam')
    response = client.get_role(RoleName='my-role')  # 返回 dict
    role_id = response['Role']['RoleId']  # 需要手动访问字典键

    # 使用 Caster 后的用法
    response = client.get_role(RoleName='my-role')
    role = caster.get_role(response)  # 转换为 dataclass
    role_id = role.Role.RoleId  # 类型安全的属性访问
"""

import dataclasses

from ..templates.template_enum import tpl_enum


@dataclasses.dataclass
class CasterMethod:
    """
    储存着单个转换器方法的信息, 对应一个 AWS service client 的方法.

    每个 CasterMethod 代表一个从 boto3 原生响应到 dataclass 的转换方法.
    例如 IAM service 的 get_role 方法会对应一个 CasterMethod 实例.

    :param method_name: 方法名称, 例如 'get_role', 'list_users'
    :param boto3_stubs_type_name: boto3-stubs 中的 TypedDict 类型名称,
        例如 'GetRoleResponseTypeDef'
    :param boto3_dataclass_type_name: 对应的 dataclass 类型名称,
        例如 'GetRoleResponse' (移除了 'TypeDef' 后缀)
    """
    method_name: str = dataclasses.field()
    boto3_stubs_type_name: str = dataclasses.field()
    boto3_dataclass_type_name: str = dataclasses.field()

    def gen_code(self) -> str:
        """
        生成转换器方法的代码字符串.

        生成的代码会是一个方法, 接收 boto3 原生响应并返回对应的 dataclass 对象.
        """
        tpl = tpl_enum.boto3_dataclass_service__package__caster_method
        return tpl.render(caster_method=self)


@dataclasses.dataclass
class CasterModule:
    """
    储存着整个服务的转换器模块信息, 包含该服务所有可转换方法的集合.

    每个 AWS 服务 (如 IAM, S3, EC2) 都会对应一个 CasterModule 实例,
    包含该服务所有返回 TypedDict 的 client 方法的转换器.

    :param service_name: AWS 服务名称, 例如 'iam', 's3', 'ec2'
    :param cms: CasterMethod 列表, 包含该服务所有可转换的方法
    """
    service_name: str = dataclasses.field()
    cms: list[CasterMethod] = dataclasses.field(default_factory=list)

    def gen_code(self) -> str:
        """
        生成整个转换器模块的代码字符串.

        生成的代码会是一个完整的 Python 模块, 包含该服务所有转换器方法.
        用户可以直接导入并使用这个模块来转换 boto3 响应.
        """
        tpl = tpl_enum.boto3_dataclass_service__package__caster_py
        return tpl.render(caster_module=self)
