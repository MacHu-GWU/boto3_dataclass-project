# -*- coding: utf-8 -*-

import json
import requests
import dataclasses
from pathlib import Path
from functools import cached_property

from rich import print as rprint

from ._version import __version__
from .paths import path_enum
from .utils import write
from .config import config

from .structures.api import Boto3DataclassServiceStructure

import asyncio
import httpx
from typing import List, Dict, Any


async def fetch_all_urls(
    urls: List[str],
    timeout: float = 30.0,
) -> List[Dict[str, Any]]:
    """
    Send multiple HTTP GET requests asynchronously and ensure all return status code 200.

    :param urls: List of URLs to request
    :param timeout: Request timeout in seconds, default is 10 seconds

    :returns: A list of dictionaries containing response data for each URL

    :raises: Exception if any request fails (non-200 status code) or an error occurs
    """
    results = []
    failed_requests = []

    async with httpx.AsyncClient(timeout=timeout) as client:
        # 创建所有请求的协程
        tasks = []
        for url in urls:
            task = asyncio.create_task(make_request(client, url))
            tasks.append((url, task))

        # 并发执行所有请求
        for url, task in tasks:
            try:
                result = await task
                results.append(result)
            except Exception as e:
                failed_requests.append({"url": url, "error": str(e)})

    # 检查是否有失败的请求
    if failed_requests:
        error_msg = "以下请求失败:\n"
        for failed in failed_requests:
            error_msg += f"- {failed['url']}: {failed['error']}\n"
        raise Exception(error_msg)

    return results


async def make_request(client: httpx.AsyncClient, url: str) -> Dict[str, Any]:
    """
    发送单个 HTTP GET 请求

    Args:
        client: httpx 异步客户端
        url: 请求的 URL

    Returns:
        包含响应信息的字典

    Raises:
        Exception: 如果请求失败或状态码不是 200
    """
    try:
        response = await client.get(url)

        # 确保状态码是 200
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.reason_phrase}")

        return {
            "url": url,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": response.text,
            "content_length": len(response.content),
            "encoding": response.encoding,
        }

    except httpx.RequestError as e:
        raise Exception(f"请求错误: {e}")
    except httpx.HTTPStatusError as e:
        raise Exception(f"HTTP 状态错误: {e}")
    except Exception as e:
        raise Exception(f"未知错误: {e}")


# 使用示例
async def main():
    # 测试 URL 列表
    urls = [
        "https://httpbin.org/get",
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://httpbin.org/json",
        "https://jsonplaceholder.typicode.com/users/1",
        "https://httpbin.org/headers",
        "https://jsonplaceholder.typicode.com/albums/1",
        "https://httpbin.org/user-agent",
        "https://jsonplaceholder.typicode.com/todos/1",
        "https://httpbin.org/ip",
    ]

    try:
        print(f"正在请求 {len(urls)} 个 URL...")
        results = await fetch_all_urls(urls)

        print(f"✅ 所有 {len(results)} 个请求都成功完成！")

        # 打印结果摘要
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['url']}")
            print(f"   状态码: {result['status_code']}")
            print(f"   内容长度: {result['content_length']} 字节")
            print(f"   编码: {result['encoding']}")
            print()

    except Exception as e:
        print(f"❌ 请求失败: {e}")


# 如果直接运行此脚本
if __name__ == "__main__":
    asyncio.run(main())


@dataclasses.dataclass
class PyPIStatus:
    version: str = dataclasses.field(default=__version__)

    @cached_property
    def path_cache_file(self) -> Path:
        return path_enum.dir_cache / f"{self.version}.json"


def get_project(name: str):
    # url = f"{domain}/pypi/{name}/json"
    url = f"{domain}/simple/{name}/"
    headers = {"Accept": "application/vnd.pypi.simple.v1+json"}
    res = requests.get(url, headers=headers)
    rprint(res.json())


name = "boto3-dataclass-iam"
get_project(name)
