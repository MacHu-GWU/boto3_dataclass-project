# -*- coding: utf-8 -*-

from boto3_dataclass_bedrock_runtime import bedrock_runtime_caster

from boto3_dataclass.tests.aws import bsm
from rich import print as rprint

bedrockruntime_client = bsm.bedrockruntime_client

model_id = "amazon.nova-micro-v1:0"
messages = [
    {
        "role": "user",
        "content": [
            {"text": "Tell me who you are in one sentence"},
        ],
    },
]
res = bedrockruntime_client.converse(
    modelId=model_id,
    messages=messages,
)
res = bedrock_runtime_caster.converse(res)

rprint(res)
print(f"{res.output.message.content[0].text = }")
