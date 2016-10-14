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