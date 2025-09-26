# -*- coding: utf-8 -*-

import dataclasses
import httpx
import asyncio


@dataclasses.dataclass
class HttpRequestResult:
    url: str = dataclasses.field()
    response: httpx.Response | None = dataclasses.field(init=False)
    error: Exception | None = dataclasses.field(init=False)


async def fetch_all_urls(
    urls: list[str],
    timeout: float = 30.0,
) -> list[HttpRequestResult]:
    """
    Send multiple HTTP GET requests asynchronously and ensure all return status code 200.

    :param urls: List of URLs to request
    :param timeout: Request timeout in seconds, default is 10 seconds

    :returns: A list of dictionaries containing response data for each URL

    :raises: Exception if any request fails (non-200 status code) or an error occurs
    """
    results = []
    async with httpx.AsyncClient(timeout=timeout) as client:
        # Create coroutines for all requests
        tasks = []
        for url in urls:
            task = asyncio.create_task(make_request(client, url))
            tasks.append((url, task))

        # Run all requests concurrently
        for url, task in tasks:
            result = await task
            results.append(result)

    return results


async def make_request(
    client: httpx.AsyncClient,
    url: str,
) -> HttpRequestResult:
    """
    Send single HTTP GET request

    :param client: httpx Async Client
    :param url: URL to request

    :returns: A :class:`HttpRequestResult` object
    """
    result = HttpRequestResult(url=url)
    try:
        response = await client.get(url)
        result.response = response
        try:
            response.raise_for_status()
            result.error = None
        except httpx.HTTPStatusError as error:
            result.error = error
    except Exception as error:
        result.error = error
    return result


# 使用示例
async def main():
    # 测试 URL 列表
    domain = "https://test.pypi.org"
    version = "1.40.0.dev2"
    urls = [
        f"{domain}/simple/{name}//{version}/",
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
