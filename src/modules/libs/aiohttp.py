import aiohttp
import asyncio
import orjson as json

class RequestError(Exception):
    """
    Raises an error if Request class was misused
    """
    pass

class Response:
    """
    Represents the Response object given after an HTTP request.
    """
    def __init__(self, content, headers):
        self.status_code = None
        self.headers = headers
        self.content = content

    @property
    def text(self):
        return self.content.decode()

    def json(self):
        return json.loads(self.text)

class Request:
    def __init__(self, method: str, url: str, headers: dict, data: dict, proxy=None, timeout=None):
        self.method = method
        self.url = url
        self.headers = headers
        self.data = data
        self.proxy = proxy
        self.timeout = timeout

    async def get_response(self):
        async with aiohttp.ClientSession() as session:
            if self.method == "GET":
                async with session.get(self.url, headers=self.headers, proxy=self.proxy) as response:
                    content = await response.read()
                    return Response(content, response.headers)
            else:
                async with session.request(self.method, self.url, json=self.data, headers=self.headers, proxy=self.proxy) as response:
                    content = await response.read()
                    return Response(content, response.headers)

class AsyncReq:
    """
    Represents an HTTP client.
    """
    async def send_request(self, method: str, url: str, headers=None, data=None, proxy=None, timeout=None) -> Response:
        headers = headers or {}
        if proxy:
            proxy = f"http://{proxy}"
        try:
            return await Request(method, url, headers, data, proxy=proxy, timeout=timeout).get_response()
        except:
            pass

    def send_request_sync(self, method: str, url: str, headers=None, data=None, proxy=None, timeout=None) -> Response:
        try:
             return asyncio.run(self.send_request(method, url, headers, data, proxy, timeout))
        except:
            pass
        

    def get(self, url: str, headers=None, proxy=None, timeout=None) -> Response:
        return self.send_request_sync(method="GET", url=url, headers=headers, proxy=proxy, timeout=timeout)

    def post(self, url: str, data: dict, headers=None, proxy=None, timeout=None) -> Response:
        return self.send_request_sync(method="POST", url=url, headers=headers, data=data, proxy=proxy, timeout=timeout)

    def put(self, url: str, data: dict, headers=None, proxy=None, timeout=None) -> Response:
        return self.send_request_sync(method="PUT", url=url, headers=headers, data=data, proxy=proxy, timeout=timeout)

    def patch(self, url: str, data: dict, headers=None, proxy=None, timeout=None) -> Response:
        return self.send_request_sync(method="PATCH", url=url, headers=headers, data=data, proxy=proxy, timeout=timeout)

    def delete(self, url: str, data: dict, headers=None, proxy=None, timeout=None) -> Response:
        return self.send_request_sync(method="DELETE", url=url, headers=headers, data=data, proxy=proxy, timeout=timeout)
