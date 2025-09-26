# -*- coding: utf-8 -*-

"""
Ref: https://docs.pypi.org/api/
"""

import json
import requests

domain = "https://test.pypi.org"
package = "boto3-dataclass-iam"
version = "1.40.0.dev1"
url = f"{domain}/pypi/{package}/{version}/json"
headers = {"Accept": "application/json"}
response = requests.get(url, headers=headers)
data = response.json()
is_exists = ("info" in data)
print(json.dumps(data, indent=2))
print(f"{is_exists = }")
