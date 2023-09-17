import orjson as json
from urllib import request

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
    def __init__(self, method: str, headers: dict, url: str, data: dict, proxy=None, timeout=None):
        self.method = method
        self.url = url
        self.data = data
        self.headers = headers
        self.proxy = proxy
        self.timeout = timeout

    def get_response(self):
        headers = self.headers
        if self.method == "GET":
            req = request.Request(self.url, headers=headers, method=self.method)
        else:
            json_data = json.dumps(self.data)
            req = request.Request(self.url, data=json_data, headers=headers, method=self.method)

        if self.proxy:
            proxy_handler = request.ProxyHandler({"https": "http://" + self.proxy})
            opener = request.build_opener(proxy_handler)
            response = opener.open(req, timeout=self.timeout)
        else:
            response = request.urlopen(req, timeout=self.timeout)

        content = response.read()
        return Response(content, response.headers)

class SocketReq:
    """
    Represents an HTTP/S client.
    """
    def send_request(self, method: str, url: str, data=None, proxy=None, timeout=None, headers=None) -> Response:
        headers = headers or {}
        try:
            return Request(method, headers, url, data, proxy=proxy, timeout=timeout).get_response()
        except:
            pass

    def get(self, url: str, proxy=None, timeout=None, headers=None) -> Response:
        return self.send_request(method="GET", url=url, proxy=proxy, timeout=timeout, headers=headers)

    def post(self, url: str, data: dict, proxy=None, timeout=None, headers=None):
        return self.send_request(method="POST", url=url, data=data, proxy=proxy, timeout=timeout, headers=headers)

    def put(self, url: str, data: dict, proxy=None, timeout=None, headers=None):
        return self.send_request(method="PUT", url=url, data=data, proxy=proxy, timeout=timeout, headers=headers)

    def patch(self, url: str, data: dict, proxy=None, timeout=None, headers=None):
        return self.send_request(method="PATCH", url=url, data=data, proxy=proxy, timeout=timeout, headers=headers)

    def delete(self, url: str, data: dict, proxy=None, timeout=None, headers=None):
        return self.send_request(method="DELETE", url=url, data=data, proxy=proxy, timeout=timeout, headers=headers)
