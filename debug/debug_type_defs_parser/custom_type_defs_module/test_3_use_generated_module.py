# -*- coding: utf-8 -*-

# from module_1_from_human_written import (
# from module_2_from_pre_build_type_defs_module import (
from module_3_from_parser import (
    SimpleModel,
    SimpleModelWithSubscript,
    SimpleModelWithNestedSubscript,
    SimpleContainer,
)


def test_simple_model():
    data = {
        "attr1": "hello",
    }
    model = SimpleModel(data)
    print(f"{model.attr1 = }")  # type hint works

    data = {
        "attr1": "hello",
        "attr3": ["a", "b", "c"],
    }
    model = SimpleModelWithSubscript(data)
    print(f"{model.attr1 = }")  # type hint works
    # print(f"{model.attr2 = }") # type hint works
    print(f"{model.attr3 = }")  # type hint works

    data = {
        "attr1": ["a", "b", "c"],
    }
    model = SimpleModelWithNestedSubscript(data)
    print(f"{model.attr1 = }")  # type hint works
    # print(f"{model.attr2 = }") # type hint works


# test_simple_model()


def test_simple_container():
    data = {
        "attr1": {
            "attr1": "value1",
        },
        "attr2": None,
        "attr3": {
            "attr1": "value3",
        },
        "attr5": None,
        "attr7": [
            {"attr1": "list_value1"},
            {"attr1": "list_value2"},
        ],
        "attr8": [
            {"attr1": "list_value1"},
            {"attr1": "list_value2"},
        ],
    }
    model = SimpleContainer(data)
    print(f"{model.attr1 = }")
    print(f"{model.attr2 = }")
    print(f"{model.attr3 = }")
    # print(f"{model.attr4 = }")
    print(f"{model.attr5 = }")
    # print(f"{model.attr6 = }")
    print(f"{model.attr7 = }")
    print(f"{model.attr8 = }")
    # print(f"{model.attr9 = }")

    print(f"{model.attr7[0].attr1 = }")  # type hint works
    # print(f"{model.attr8[0].attr1 = }")  # type hint works
    # print(f"{model.attr9[0].attr1 = }")  # type hint works


test_simple_container()
