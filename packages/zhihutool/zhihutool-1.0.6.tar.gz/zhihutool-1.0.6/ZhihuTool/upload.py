import requests
from ZhihuTool.login import cookies
import random


def upload(path):
    s = requests.session()
    headers = {
        "Host": "zhuanlan.zhihu.com",
        "Origin": "https://zhuanlan.zhihu.com",
        "Referer": "https://zhuanlan.zhihu.com/write",
        'Connection': 'keep-alive',
        'User-Agent': 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36',
        'x-xsrftoken': cookies.get('_xsrf'),
        'x-requested-with': 'Fetch',
    }
    files = {'picture': open(path, 'rb')}
    post_url = 'https://zhuanlan.zhihu.com/api/uploaded_images'
    res = s.post(post_url, files=files, headers=headers, cookies=cookies)
    content = res.json()
    print(content)
    result = []
    if 'src' in content:
        origin = content['src']
        hashcode = origin[8:].split('/')[-1].split('.')
        number = random.randint(1, 7)
        low = 'https://pic{}.zhimg.com/'.format(number) + hashcode[0] + '_hd.' + hashcode[1]
        hd = 'https://pic{}.zhimg.com/'.format(number) + hashcode[0] + '.' + hashcode[1]
        result.append('True')
        result.append(low)
        result.append(hd)
        return result
    else:
        result.append('False')
        return result
