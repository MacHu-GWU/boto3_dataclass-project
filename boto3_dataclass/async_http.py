# -*- coding: utf-8 -*-

import dataclasses
import httpx
import asyncio


@dataclasses.dataclass
class HttpResult:
    """
    Result of an HTTP request.
    """

    url: str = dataclasses.field()
    response: httpx.Response | None = dataclasses.field(init=False)
    error: Exception | None = dataclasses.field(init=False)


async def fetch_all_urls(
    urls: list[str],
    timeout: float = 30.0,
) -> list[HttpResult]:
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
) -> HttpResult:
    """
    Send single HTTP GET request

    :param client: httpx Async Client
    :param url: URL to request

    :returns: A :class:`HttpResult` object
    """
    result = HttpResult(url=url)
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
