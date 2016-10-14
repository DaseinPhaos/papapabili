import papapabili
import json
infos = papapabili.get_download_info(r"http://bangumi.bilibili.com/anime/v/63669")
print(json.dumps(infos, indent = 2))
papapabili.download(infos,dir="./temp", workers = 4)
