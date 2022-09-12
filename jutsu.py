import time
import string
import random
import re
import os
import requests

# @formatter:off
head={'authority':'jut.su','accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-language':'en-US,en;q=0.9,ru;q=0.8','cache-control':'no-cache','pragma':'no-cache','sec-ch-ua':'"Google Chrome";v="107","Chromium";v="107","Not=A?Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform':'"Windows"','sec-fetch-dest':'document','sec-fetch-mode':'navigate','sec-fetch-site':'none','sec-fetch-user':'?1','upgrade-insecure-requests':'1','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}  # nopep8
cook={'PHPSESSID':'d3vblu92h7a2voqb8u9etrdd01'}
# @formatter:on
# compressed, so it doesn't use as many lines
# PHPSESSID cookie variator
cook['PHPSESSID'] = cook['PHPSESSID'].replace(random.choice(cook['PHPSESSID']), random.choice(string.ascii_letters))

HTTPError = requests.HTTPError  # export requests http error


def get_info(url: str):
    """
    Get rough anime name, season and episode from an episode URL.
    :param url Episode URL.
    """
    match = re.search(r'(?!//)(?<!/)/(.*?)/(.*?)/(.*?)\.html', url)
    if match:
        return {'name': match[1],
                'season': int(re.search(r'\d+', match[2])[0]),
                'episode': int(re.search(r'\d+', match[3])[0])}
    # need for another way to get info
    raise ValueError('Unknown episode link type.')


class Episode:
    """
    Class representing an episode page
    """

    def __init__(self, url):
        self.page = None
        self.urls = None
        self.url = url
        self.srcp = re.compile(r'<source.*?src="(.*?)".*?label="(.*?)".*?>')
        self.headers = head
        self.cookies = cook

        try:
            self.info = get_info(self.url)
            self.name, self.season, self.episode = self.info.values()
        except ValueError:
            self.info = self.name = self.season = self.episode = None

    def load(self):
        response = requests.get(self.url, cookies=self.cookies, headers=self.headers)
        if not response.ok:
            raise HTTPError(response.status_code)
        self.page = response.text
        self.urls = {i.group(2): i.group(1) for i in re.finditer(self.srcp, self.page)}


# 256 KB chunk size by default
def download(url: str, path: str, progress=False, chunk_size=2 ** 21, headers=None, cookies=None):
    """
    Downloads a file using a URL to the path.

    :param url URL to a file
    :param path Path to the file, relative or absolute
    :param progress (optional) Set True if you want the progress-showing functionality
    :param chunk_size (optional) Size of the chunk after which it is written to disk
    :param headers (optional) Headers as a dictionary suitable for Requests
    :param cookies (optional) Cookies as a dictionary suitable for Requests
    """

    if not headers:
        headers = head
    if os.path.exists(path):
        raise FileExistsError('File or directory already exists.')
    loader = requests.get(url, stream=True, cookies=cookies, headers=headers)
    size = int(loader.headers['Content-length'])
    tm = time.time()
    if progress:
        _progress = 0
        t = time.time()
        print()
    with open(path, 'ab+') as file:
        for i in loader.iter_content(chunk_size):
            if progress:  # with common internet speed should not affect performance
                # @formatter:off
                print(f'\r{_progress / 1024:.02f}/{size / 1024 / 1024:.02f}MB, {chunk_size / 1024 / (time.time() - t):.03f}KB/s, {_progress / (time.time() - tm):.03f}KB/s avg', end=' ' * 10)  # nopep8
                # @formatter:on
                # self rewriting progress line
                t = time.time()
                time.sleep(0.001)  # don't go too fast :)
                # workaround for chunks getting downloaded at exact same moment causing division by zero
                _progress += chunk_size / 1024
            file.write(i)
    if progress:
        print(' Done')
    return [size, time.time() - tm]


def get_eps(url: str):
    """Get the episode links from the base anime page (page with button links to EPs)"""
    page = requests.get(url, headers=head, cookies=cook)
    if not page.ok:
        raise HTTPError('HTTP error while getting the page. ' + url)
    if page.text.find('class="v_epi_nav"') > -1:
        raise ValueError('I think it is an episode.')
    e = re.compile(r'<a.*?href="(.*?)".*?class=".*?video.*?".*?>')
    return [Episode('https://jut.su' + [i[1] + 'episode-1.html', i[1]][i[1][-5:] == '.html']) for i in re.finditer(e, page.text)]
