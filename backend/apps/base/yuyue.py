import random
import threading
import time
import urllib
import json
import requests
import datetime

angents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]

# 等待返回结果
def wait_handle(url):
    headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': random.choice(angents)
    }
    data = {'name':'朱小芳','tel':'17316280277','sn':'411522199410063623'}
    request = requests.post(url=url, data=data, headers=headers)
    response = request.content.decode('utf8')
    res_obj = json.loads(response)
    print('路由', url ,'==> 预约结果：', res_obj)
    return res_obj.get('status')

def begain_handle(url, re_list):
    headers={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': random.choice(angents)
    }
    data = {'name':'朱小芳','tel':'17316280277','sn':'411522199410063623'}
    request = requests.post(url=url, data=data, headers=headers)
    response = request.content.decode('utf8')
    res_obj = json.loads(response)
    print('路由', url ,'==> 预约结果：', res_obj)
    res_msg = res_obj.get('message')
    re_list.append({'路由':url,'结果':res_msg})

# 并发运行
def main():
    result_list = []
    urls = ['http://%s.duotucms.com/index.php/index/order' % str(item) for item in range(1,8)]
    # begain_handle(url, re_list)
    workers = [threading.Thread(target=begain_handle, args=(url, result_list, )) for url in urls]
    # 多线程异步提交
    [worker.start() for worker in workers]
    [worker.join() for worker in workers]

# 逐一运行 等待返回结果
def one_handle():
    urls = ['http://%s.duotucms.com/index.php/index/order' % str(item) for item in range(1,8)]
    print('当前请求时间：', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    for url in urls:
        if wait_handle(url) == '0':
            break
    print('\n')

if __name__ == "__main__":
    # 并发执行
    # main()
    # 等待结果执行
    one_handle()
