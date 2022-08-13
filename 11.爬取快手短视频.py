# -*- coding = utf-8 -*-
# @time :2022/8/9 21:16
# @Author :Jachang Liang
# @File:11.爬取快手短视频.py
# @Software :PyCharm

import time
import os
import requests
from requests_html import UserAgent
import json
import re

dir_name = 'python_快手video'
if not os.path.exists(dir_name):
    os.mkdir(dir_name)

keyword = input('请输入关键字：')
url = 'https://www.kuaishou.com/graphql'
ua = UserAgent().random
header = {
    'content-type': 'application/json',
    'Cookie': 'did=web_0a72647a0d401f31bc531a6b49368848; didv=1660053898306; clientid=3; client_key=65890b29; '
              'kpf=PC_WEB; kpn=KUAISHOU_VISION',
    'Host': 'www.kuaishou.com',
    'Origin': 'https://www.kuaishou.com',
    'Referer': 'https://www.kuaishou.com/brilliant',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-platform': "Windows",
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/103.0.0.0 Safari/537.36'
}

params = {"operationName": "visionSearchPhoto",
          "variables": {"keyword": keyword, "pcursor": "", "page": "", "webPageArea": "searchxxnull"},
          "query": "fragment photoContent on PhotoEntity {\n  id\n  duration\n  caption\n  likeCount\n  viewCount\n  "
                   "realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n"
                   "  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n"
                   "  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  __typename\n}\n\nfragment feedContent "
                   "on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n"
                   "      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    "
                   "__typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  __typename\n}\n\nquery "
                   "visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, "
                   "$webPageArea: String) {\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: "
                   "$searchSessionId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    "
                   "webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    searchSessionId\n    "
                   "pcursor\n    aladdinBanner {\n      imgUrl\n      link\n      __typename\n    }\n    "
                   "__typename\n  }\n}\n"}
data = json.dumps(params)
time.sleep(2)
res = requests.post(url, headers=header, data=data)
content = res.json()
feeds = content['data']['visionSearchPhoto']['feeds']
for feed in feeds:
    title = feed['photo']['caption']
    link = feed['photo']['photoUrl']
    new_title = re.sub(r'[\/:*?"<>|\n]', '_', title)
    content = requests.get(link).content
    with open(dir_name + '/' + new_title + '.mp4', 'wb') as f:
        f.write(content)
        print(title, '下载完成...')
