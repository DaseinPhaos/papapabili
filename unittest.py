import papapabili
import json
infos = papapabili.get_download_info(r"http://www.bilibili.com/video/av6678146/")
print(json.dumps(infos, indent = 2))
papapabili.download(infos,dir="./temp", workers = 4)
