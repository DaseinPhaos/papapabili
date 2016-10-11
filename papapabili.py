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
_bili_headers = {
    'Connection': 'keep-alive', 
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2',
    'Host': 'interface.bilibili.com',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Upgrade-Insecure-Requests': '1', 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36', 
    'Cache-Control': 'max-age=0'
    }
def _get_har_with_phantomjs(url):
    cmd = '"{2}" {0} "{1}"'.format(_script_path, url, _phantomjs_path)
    stdout, _ = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
    # stdout = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=False).stdout.readlines()
    har = stdout.decode('utf8')
    return json.loads(har[har.find("{"):])

def get_download_info(url):
    infos = {}
    harjs = _get_har_with_phantomjs(url)
    page = harjs['log']['pages'][0]
    infos['title'] = page['title']
    d_info_url = None
    for entry in harjs['log']['entries']:
        if entry['request']['url'].find('playurl') != -1:
            d_info_url = entry['request']['url']
            break
    r = requests.get(d_info_url, headers=_bili_headers)
    if r.status_code != 200: r.raise_for_status()
    d_info = json.loads(r.text)
    infos['format'] = d_info['format']
    infos['timelength'] = d_info['timelength']
    infos['durl'] = d_info['durl']
    return infos