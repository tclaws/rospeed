import orjson as json
import httpx

class RequestError(Exception):
    """
    Raises an error if Request class was misused
    """
    pass

class Response:
    """
    Represents the Response object given after an HTTPs request.
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

    def get_response(self):
        if self.proxy:
            client = httpx.Client(proxies='http://' + self.proxy, timeout=self.timeout)
        else:
            client = httpx.Client(timeout=self.timeout)
        response = None

        if self.method == "GET":
            response = client.get(self.url, headers=self.headers)
        else:
            response = client.request(self.method, self.url, json=self.data, headers=self.headers)

        content = response.read()
        client.close()
        return Response(content, response.headers)

class HttpReq:
    """
    Represents an HTTP/S client.
    """
    def send_request(self, method: str, url: str, headers=None, data=None, proxy=None, timeout=None) -> Response:
        headers = headers or {}
        try:
           return Request(method, url, headers, data, proxy=proxy, timeout=timeout).get_response()
        except:
            pass

    def get(self, url: str, headers=None, proxy=None, timeout=None) -> Response:
        return self.send_request(method="GET", url=url, headers=headers, proxy=proxy, timeout=timeout)

    def post(self, url: str, data: dict, headers=None, proxy=None, timeout=None):
        return self.send_request(method="POST", url=url, headers=headers, data=data, proxy=proxy, timeout=timeout)

    def put(self, url: str, data: dict, headers=None, proxy=None, timeout=None):
        return self.send_request(method="PUT", url=url, headers=headers, data=data, proxy=proxy, timeout=timeout)

    def patch(self, url: str, data: dict, headers=None, proxy=None, timeout=None):
        return self.send_request(method="PATCH", url=url, headers=headers, data=data, proxy=proxy, timeout=timeout)

    def delete(self, url: str, data: dict, headers=None, proxy=None, timeout=None):
        return self.send_request(method="DELETE", url=url, headers=headers, data=data, proxy=proxy, timeout=timeout)
