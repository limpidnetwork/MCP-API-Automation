import json
import requests
from urllib.parse import urlunparse

def authorize_with_MCP(host, username, password):
    """
    Authorize a user with MCP and return a token which must be supplied in all other API requests.
    :param host: MCP Host
    :param username: MCP user username
    :param password: MCP user password
    :return: a token to be used as a "bearer" token. Part of the bearer authorization model.
    """
    path = "/tron/api/v1/tokens"

    # build the URL String
    url = urlunparse(('https', host, path, None, None, None))

    auth_payload = "username={uname}&password={passwd}&tenant=master".format(uname=username, passwd=password)
    auth_headers = {"cache-control": "no-cache", "content-type": "application/x-www-form-urlencoded"}

    # TODO Do not use "verify=False" for production applications. Always modify to fit your HTTP certificate model
    response = requests.post(url, data=auth_payload, headers=auth_headers, verify=False)
    data = response.json()

    # return the token from the response json
    return data["token"]


