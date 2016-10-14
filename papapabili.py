"""
##Introduction
An in-building programming api for http://www.bilibili.com
Currently it has only achived the bare minimum to retrieve video download links.

##Requirement
- python 3
- **requests** 2.1.0 + by Kenneth Reitz : https://github.com/kennethreitz/requests/, which can also be installed via `pip install requests`
- **Phantomjs** 2.1.1 + : http://phantomjs.org/download.html. Note that its path should be set properly in `dataconfig.json`.

##Example
```python
import papapabili
infos = papapabili.get_download_info("http://www.bilibili.com/video/av1762101")
print(infos)
```
"""

import subprocess
import json
import requests
_configs = {}
with open("dataconfig.json") as f:
    _configs.update(json.loads(f.read()))
_phantomjs_path = _configs['phantomjs_path']
_script_path = _configs['script_path']

_headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; SHV36 Build/S7150; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/50.0.2661.86 Mobile Safari/537.36"
}

def _get_url_with_phantomjs(url, redirect = None):
    cmd = '"{2}" {0} "{1}"'.format(_script_path, url, _phantomjs_path)
    # stdout, _ = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
    stdout, stderr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE , shell=True).communicate()
    phantomout = stdout.decode('utf8')
    if redirect != None:
        with open(redirect, 'w', encoding='utf8') as f:
            f.write(phantomout)
    foundsub = phantomout[phantomout.find("Target found: "):]
    return foundsub[14:foundsub.find('\r\n')]

def _decode_url(url):
    host, paramstr = url.split("?")
    params = paramstr.split("&")
    ps = {}
    for param in params:
        k,v = param.split("=")
        ps[k]=v
    return (host,ps)


def get_download_info(url, redirect = None):
    d_info_url = _get_url_with_phantomjs(url, redirect)
    print("[{0}]".format(d_info_url))
    if d_info_url == "": return {}
    host, params = _decode_url(d_info_url)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; SHV36 Build/S7150; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/50.0.2661.86 Mobile Safari/537.36"
    }
    # r = requests.get(host, params = params, headers= _headers)
    r = requests.get(d_info_url, headers = headers)
    if r.status_code != 200: r.raise_for_status()
    return r.json()