# -*- coding: utf-8 -*-

from pathlib import Path
from boto3_dataclass.gen_code import AwsService

name = "lambda"

dir_here = Path(__file__).absolute().parent
path_dataclass = dir_here / f"aws_{name}.py"
service = AwsService(name=name)
s = service.generate_code()
# path_dataclass.write_text(s, encoding="utf-8")
