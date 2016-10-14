import papapabili
import json
infos = papapabili. get_download_info(r"http://bangumi.bilibili.com/anime/v/96757")
print(json.dumps(infos, indent = 2))


# import requests
# _bili_headers = {
#     'Connection': 'keep-alive', 
#     'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2',
#     'Accept-Encoding': 'gzip, deflate, sdch, br',
#     'Host': 'bangumi.bilibili.com',
#     'Upgrade-Insecure-Requests': '1', 
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36', 
#     'Cache-Control': 'max-age=0'
#     }
# r = requests.get("http://bangumi.bilibili.com/anime/v/90172", headers= _bili_headers)
# with open("./temp/naruto.html", 'w', encoding='utf8') as f:
#     f.write(r.text)