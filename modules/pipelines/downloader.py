import json
import requests
from urllib.parse import urlunparse

def get_data(host, path, token):
    """
    Access and return the first Network Construct in the system
    :param host: MCP Host
    :param token: Authorization token
    :return: The first Network Contruct
    """

    # build the url string
    url = urlunparse(('https', host, path, None, None, None))

    auth_headers = {"authorization": "bearer " + token, "cache-control": "no-cache", "content-type": "application/json"}

    # TODO Do not use "verify=False" for production applications. Always modify to fit your HTTP certificate model
    response = requests.get(url, headers=auth_headers, verify=False)
    data = response.json()
    return data["data"]
