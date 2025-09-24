# -*- coding: utf-8 -*-

"""
Generate the templates/template_enum.py file containing an enumeration of all templates.
"""

from boto3_dataclass.templates.template_helpers import gen_code

gen_code()
