# -*- coding: utf-8 -*-

from aws_bedrock_runtime import ConverseResponse
from test_settings import bsm

model_id = "amazon.nova-micro-v1:0"
messages = [
    {
        "role": "user",
        "content": [
            {"text": "Tell me who you are in one sentence"},
        ],
    },
]

client = bsm.bedrockruntime_client
res = client.converse(
    modelId=model_id,
    messages=messages,
)
res = ConverseResponse(res)
print(f"{res.output.message.content[0].text = }")
