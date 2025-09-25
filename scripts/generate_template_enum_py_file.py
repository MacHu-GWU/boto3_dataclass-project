# -*- coding: utf-8 -*-

"""
Use this script to generate the
`boto3_dataclass/templates/template_enum.py <https://github.com/MacHu-GWU/boto3_dataclass-project/blob/main/boto3_dataclass/templates/template_enum.py>`_
file containing an enumeration of all templates.

It uses the :func:`gen_code` defined in
`boto3_dataclass/templates/template_helpers.py <https://github.com/MacHu-GWU/boto3_dataclass-project/blob/main/boto3_dataclass/templates/template_helpers.py>`_
"""

from boto3_dataclass.templates.template_helpers import gen_code

gen_code()
