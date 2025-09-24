# -*- coding: utf-8 -*-

from boto3_dataclass.models.typed_dict import (
    TypedDictFieldAnnotation,
    TypedDictField,
    TypedDictDef,
)
from boto3_dataclass.utils import compare_code

# DEBUG = True
DEBUG = False


class TestTypedDictField:
    def test_gen_code(self):
        # case 1
        field = TypedDictField(
            name="id",
        )
        code = field.gen_code()
        expected = """
        @cached_property
        def id(self):  # pragma: no cover
            return self.boto3_raw_data["id"]
        """
        assert compare_code(code, expected, debug=DEBUG) is True

        # case 2
        field = TypedDictField(
            name="id",
            anno=TypedDictFieldAnnotation(
                is_nested_typed_dict=True,
                nested_type_name="UserTypeDef",
            ),
        )
        code = field.gen_code()

        expected = """
        @cached_property
        def id(self):  # pragma: no cover
            return User.make_one(self.boto3_raw_data["id"])
        """
        assert compare_code(code, expected, debug=DEBUG) is True


class TestTypedDictDef:
    def test_gen_code(self):
        # case 1
        typed_dict = TypedDictDef(
            name="UserTypeDef",
            fields=[
                TypedDictField(name="id"),
                TypedDictField(
                    name="user",
                    anno=TypedDictFieldAnnotation(
                        is_nested_typed_dict=True,
                        nested_type_name="UserTypeDef",
                    ),
                ),
                TypedDictField(
                    name="users",
                    anno=TypedDictFieldAnnotation(
                        is_nested_typed_dict=True,
                        nested_type_name="UserTypeDef",
                        nested_type_subscriptor="List",
                    ),
                ),
            ],
        )
        code = typed_dict.gen_code()
        expected = """
        @dataclasses.dataclass(frozen=True)
        class User:
            boto3_raw_data: "type_defs.UserTypeDef" = dataclasses.field()
        
            @cached_property
            def id(self):  # pragma: no cover
                return self.boto3_raw_data["id"]
        
            @cached_property
            def user(self):  # pragma: no cover
                return User.make_one(self.boto3_raw_data["user"])
        
            @cached_property
            def users(self):  # pragma: no cover
                return User.make_many(self.boto3_raw_data["users"])
        
            @classmethod
            def make_one(cls, boto3_raw_data: T.Optional["type_defs.UserTypeDef"]):
                if boto3_raw_data is None:
                    return None
                return cls(boto3_raw_data=boto3_raw_data)
        
            @classmethod
            def make_many(cls, boto3_raw_data_list: T.Optional[T.Iterable["type_defs.UserTypeDef"]]):
                if boto3_raw_data_list is None:
                    return None
                return [cls(boto3_raw_data=boto3_raw_data) for boto3_raw_data in boto3_raw_data_list]
        """
        assert compare_code(code, expected, debug=DEBUG) is True


if __name__ == "__main__":
    from boto3_dataclass.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto3_dataclass.models.typed_dict",
        preview=False,
    )
