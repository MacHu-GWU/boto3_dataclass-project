这个目录专门用来测试 boto3_dataclass_parsers.type_defs_parser.py 的功能.

我们通过创建一个极简的 module.pyi, 聚焦于某种我们想要深入研究的特殊 parsing 逻辑, 然后用 test_type_defs_parser.py 来验证解析结果.
