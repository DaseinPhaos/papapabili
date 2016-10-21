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
import json
infos = papapabili.get_download_info(r"http://bangumi.bilibili.com/anime/v/63669")
print(json.dumps(infos, indent = 2))
papapabili.download(infos,dir="./temp", workers = 4)
```
"""

import subprocess
import json
import requests
import os
import concurrent.futures
import time

_invalid_filename_characters = {
    '\\', '/', '<', '>', ':', '?', '"', '|'
}


_configs = {}
with open("dataconfig.json") as f:
    _configs.update(json.loads(f.read()))
_phantomjs_path = _configs['phantomjs_path']
_script_path = _configs['script_path']

_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36" # "Mozilla/5.0 (Linux; Android 6.0.1; SHV36 Build/S7150; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/50.0.2661.86 Mobile Safari/537.36"
}

def _get_url_with_phantomjs(url, redirect = None):
    cmd = '"{2}" {0} "{1}"'.format(_script_path, url, _phantomjs_path)
    # stdout, _ = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()
    stdout, stderr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE , shell=True).communicate()
    phantomout = stdout.decode('utf8')
    if redirect != None:
        with open(redirect, 'w', encoding='utf8') as f:
            f.write(phantomout)
    title = phantomout[phantomout.find("Title: "):]
    title = title[6:title.find('\n')].strip() 
    url = phantomout[phantomout.find("Target found: "):]
    url = url[14:url.find('\n')].strip()
    return (title, url)

def get_download_info(url):
    title, d_info_url = _get_url_with_phantomjs(url)
    # print("[{0}]".format(d_info_url))
    if d_info_url == "": return {}
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36" # "Mozilla/5.0 (Linux; Android 6.0.1; SHV36 Build/S7150; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/50.0.2661.86 Mobile Safari/537.36"
    }
    r = requests.get(d_info_url, headers = headers)
    if r.status_code != 200: r.raise_for_status()
    # result = r.json()
    result = r.text[r.text.find("{"):r.text.rfind("}")+1]
    result = json.loads(result)
    result.update({"title": title})
    return result

def _start_download(dinfo, relative_path, format):
    try:
        order = dinfo['order']
        size = dinfo['size']
        chunk_c = 0
        print("Chunk#{0} downloading started...".format(order))
        # _continue_header = {'Range': 'bytes={0}-'.format(bytes_downloaded)}
        r = requests.get(dinfo['url'], stream=True)
        with open("{0}/{1}.{2}".format(relative_path, dinfo['order'], format), 'wb') as f:
            next_status = 0.01
            for chunk in r.iter_content(4096):
                chunk_c += 4096
                if chunk_c/size > next_status:
                    print("Chunk#{0} status: {1:.2f}".format(order, chunk_c/size))
                    next_status += 0.01
                f.write(chunk)
    except Exception as identifier:
        print(identifier)
        return False
    return True

def download(download_infos, dir=".", workers = 2):
    title = download_infos["title"]
    for c in _invalid_filename_characters:
        title = title.replace(c, ' ')
    print("Start downloading {0}...".format(title))
    subdir = dir+"/"+ title
    try:
        os.mkdir(subdir)
    except FileExistsError as identifier:
        pass
    format = download_infos["format"]
    if format == "hdmp4": format = "mp4"
    with concurrent.futures.ThreadPoolExecutor(max_workers = workers) as executor:
        futures = []
        for urlinfo in download_infos["durl"]:
            futures.append(executor.submit(_start_download, urlinfo, subdir, format))
        done_count = 0
        for future in futures:
            if future.result() == True:
                done_count += 1
        print("Works done, {0} of {1} successfully downloaded.".format(done_count, len(futures)))

