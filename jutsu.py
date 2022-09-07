import time
import re
import os
import requests

headers = {'authority': 'jut.su',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'accept-language': 'en-US,en;q=0.9,ru;q=0.8', 'cache-control': 'no-cache', 'pragma': 'no-cache',
           'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?0',
           'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'document', 'sec-fetch-mode': 'navigate',
           'sec-fetch-site': 'none', 'sec-fetch-user': '?1', 'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}  # nopep8
cookies = {'PHPSESSID': 'd3vblu92h7a2voqb8u9etrdd01'}


class Episode:
    """Class representing an episode page"""

    def __init__(self, url):
        self.url = url
        self.srcp = re.compile(
            r'<source.*?src="(.*?)".*?label="(.*?)".*?>')
        self.headers = headers
        self.cookies = cookies
        response = requests.get(
            url, cookies=self.cookies, headers=self.headers)
        if not response.ok:
            raise requests.HTTPError(response.status_code)
        self.page = response.text
        self.urls = {i.group(2): i.group(1)
                     for i in re.finditer(self.srcp, self.page)}


def get_info(url):
    """Get rough anime name, season and episode from URL."""
    match = re.search(r'(?!//)(?<!/)/(.*?)/(.*?)/(.*?)\.html', url)
    if match:
        return [match[1], int(re.search(r'\d+', match[2])[0]), int(re.search(r'\d+', match[3])[0])]
    # need for another way to get info
    raise ValueError('Unknown episode link type.')


# 256 KB chunk size by default
def download(url: str, path: str, progress=False, chunk_size=2 ** 21, headers=headers, cookies=None):
    '''Downloads a file using URL to path

    :param url URL to a file
    :param path Path to the file, relative or absolute
    :param progress (optional) Set True if you want the progress-showing functionality
    :param chunk_size (optional) Size of the chunk after which it is written to disk
    :param headers (optional) Headers as a dictionary suitable for Requests
    :param cookies (optional) Cookies as a dictionary suitable for Requests'''
    if os.path.exists(path):
        raise FileExistsError('File or directory already exists.')
    loader = requests.get(
        url, stream=True, cookies=cookies, headers=headers)
    _progress = 0
    t = time.time()
    if progress:
        print()
    with open(path, 'ab+') as file:
        for i in loader.iter_content(chunk_size):
            if progress:  # with common internet speed should not affect performance
                print(
                    f'\r{_progress / 1024:.02f}MB, {_progress / 1024 / (time.time() - t):.03f}KB/s',
                    end=' ' * 10)  # self overwriting progress line
                t = time.time()
                _progress += chunk_size / 1024
            file.write(i)
    if progress:
        print(' Done')


def get_eps(url: str):
    """Get the episode links from the base anime page (page with button links to EPs)"""
    page = requests.get(url, headers=headers, cookies=cookies)
    if not page.ok:
        raise requests.HTTPError("HTTP error while getting the page. " + url)
    if page.text.find('class="v_epi_nav"') > -1:
        raise ValueError("I think it is an episode.")
    e = re.compile(r'<a.*?href="(.*?)".*?class=".*?video.*?".*?>')
    return [i[1] for i in re.finditer(e, page.text)]


def slicer(*rules: str):
    '''Parses user expressions like 21-9; 9-12; 5 to ranges'''
    p1 = re.compile(r'\d+-\d+')
    for i in rules:
        tr = re.search(p1, i)
        if tr:
            # fix order, convert numbers to indices and range
            yield range(*(lambda a: [a[0] - 1, a[1]])(sorted(map(int, tr))))
        else:
            # convert to indice single number range
            yield range(int(i) - 1, int(i))
