import requests
from requests_toolbelt import MultipartEncoder
from ZhihuTool.login import cookies


def set_watermark(status=False):
    url = 'https://www.zhihu.com/api/v4/me/settings'
    s = requests.session()
    if status is False:
        m = MultipartEncoder(fields={'type': 'watermark', 'value': 'disable'})
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
            'Content-Type': m.content_type,
            'x-xsrftoken': cookies.get('_xsrf')}
        res = s.put(url, headers=headers, data=m, cookies=cookies)
        if res.status_code == 204:
            return True
        else:
            return False
    elif status is True:
        m = MultipartEncoder(fields={'type': 'watermark', 'value': 'enable'})
        headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
            'Content-Type': m.content_type,
            'x-xsrftoken': cookies.get('_xsrf')}
        res = s.put(url, headers=headers, data=m, cookies=cookies)
        if res.status_code == 204:
            return True
        else:
            return False
