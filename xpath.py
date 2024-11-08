from bs4 import BeautifulSoup
import requests


def xpxp(url_ex,headers):



    response = requests.get(url_ex, headers=headers)
    response.encoding = response.apparent_encoding
    # 因为网站使用的不是通用的utf-8格式，而是gzip，所以要让它判断解码格式
    html = BeautifulSoup(response.text, 'html.parser')
    # 获取到的网页信息需要进行解析，使用lxml解析器，其实默认的解析器就是lxml，但是这里会出现警告提示，方便你对其他平台移植
    content = html.select(
        '#__next > div.mantine-AppShell-root.bg-background.page-main-wrapper.mantine-1udmbix > div > main > div')
    # 将复制好的选择器信息放进select方法中，将获取到的内容作为tag形式放入一个列表中
    info = content[0].getText().replace('。', '。\n')
    return info
