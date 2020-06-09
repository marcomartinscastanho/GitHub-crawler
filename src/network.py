import requests
from random import randrange
from bs4 import BeautifulSoup
from copy import deepcopy


def encode_request(json_input: dict) -> str:
    """
    Encodes the HTTP request based on the input parameters
    :param json_input: json-like dict containing the request parameters
    :return: the HTTP request url
    """
    # https://github.com/search?q=openstack+nova+css&type=Repositories

    keywords = "+".join(json_input["keywords"])
    url = f"https://github.com/search?q={keywords}"
    if "type" in json_input:
        search_type = json_input["type"]
        url = url + f"&type={search_type}"

    return url


def get_random_proxy(json_input: dict) -> str:
    """
    Returns a random proxy from the input to be used in all requests
    :param json_input: json-like dict with the input parameters
    :return: string with the proxy ip:port
    """
    proxies = json_input["proxies"]
    proxy_nr = randrange(len(proxies))
    return proxies[proxy_nr]


def send(request_url: str, proxy: str) -> dict:
    """
    Sends the HTTP request and waits for a response
    :param request_url: encoded request url
    :param proxy: proxy used to make the request
    :return: dict with response
    """

    proxy = {
        "https": proxy,
    }

    r = requests.get(request_url, proxies=proxy)

    return {"code": r.status_code, "encoding": r.encoding, "text": r.text}


def decode_query_response(html_response):
    """
    Decodes the HTTP response for a query request and builds the JSON-like dict output
    :param html_response: HTTP response text
    :return: JSON-like dict output
    """
    soup = BeautifulSoup(html_response, 'html.parser')

    json_response = []

    for res in soup.find_all('div', "f4 text-normal"):
        a = res.find('a')
        url = a.get('href')
        json_response.append({"url": f"https://github.com{url}"})

    return json_response


def decode_language_stats(html_response) -> dict:
    """
        Decodes the HTTP response for a query request and builds the JSON-like dict output
        :param html_response: HTTP response text
        :return: dict with extra information
        """
    soup = BeautifulSoup(html_response, 'html.parser')
    lang_stats = {}

    langs = []
    percents = []

    for res in soup.find_all('span', "lang"):
        langs.append(res.string)

    for res in soup.find_all('span', "percent"):
        percents.append(float(res.string[:-1]))

    for i, lang in enumerate(langs):
        lang_stats[lang] = percents[i]

    return lang_stats


def add_extra_information(json_output: list, proxy: str) -> None:
    """
    Adds extra information to each of the objects in the json_output by requesting it form each individual url
    :param json_output: the json_output with only the urls
    :param proxy: proxy to be used for http requests
    """

    for i, repo in enumerate(deepcopy(json_output)):
        url = repo["url"]
        response = send(url, proxy)
        json_output[i]["extra"] = {}
        json_output[i]["extra"]["language_stats"] = decode_language_stats(response["text"])
        json_output[i]["extra"]["owner"] = url.split('/')[3]
