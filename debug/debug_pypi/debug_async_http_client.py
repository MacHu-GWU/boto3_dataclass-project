# -*- coding: utf-8 -*-

import asyncio
from boto3_dataclass.async_http import fetch_all_urls

domain = "https://test.pypi.org"
version = "1.40.0.dev2"


def make_url(package: str) -> str:
    return f"{domain}/pypi/{package}/{version}/json"


async def fetch_package_infos():
    urls = [
        make_url("boto3-dataclass-robomaker"),
        make_url("boto3-dataclass-migration-hub-refactor-spaces"),
        make_url("boto3-dataclass-lex-runtime"),
    ]
    try:
        print(f"正在请求 {len(urls)} 个 URL...")
        results = await fetch_all_urls(urls)
        print(f"✅ 所有 {len(results)} 个请求都成功完成！")
        return results
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        raise


def main():
    results = asyncio.run(fetch_package_infos())
    for i, result in enumerate(results, 1):
        print(f"--- {i}. {result.url}")
        if result.error is None:
            print(f"{result.response.text[:100] = }")
        else:
            print(f"{result.error = }")


if __name__ == "__main__":
    main()
