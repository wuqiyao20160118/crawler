import requests
from lxml import etree

def get_html(url):
    """
    获取html
    :param url: 网址
    :return: html
    """
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/70.0.3538.67 Safari/537.36",
    }
    response = requests.get(url,headers=headers)
    response.encoding = "gbk"
    return response.text

def get_text(text,key):
    """ 返回特定格式数据 """
    return text.replace(key, "").strip()

def parse_detail_url(url):
    """
    处理数据
    :param url: 网址
    :return:
    """
    result = {}
    html = get_etree_HTML_obj(url)
    div = html.xpath("//div[@id='Zoom']")[0]
    images = div.xpath(".//img/@src")
    result["poster"] = images[0]
    result["detail_img"] = images[1]
    text_list = div.xpath(".//text()")
    for text in text_list:
        if text.startswith("◎译　　名"):
            result["title"] = get_text(text,"◎译　　名")
        elif text.startswith("◎年　　代"):
            result["year"] = get_text(text,"◎年　　代")
        elif text.startswith("◎产　　地"):
            result["country"] = get_text(text,"◎产　　地")
        elif text.startswith("◎类　　别"):
            result["type"] = get_text(text,"◎类　　别")
        elif text.startswith("◎片　　长"):
            result["time"] = get_text(text,"◎片　　长")
        elif text.startswith("◎导　　演"):
            result["director"] = get_text(text,"◎导　　演")
    # 这里只挑了些好取的来做示范
    return result

def get_etree_HTML_obj(url):
    """
    获取etree的html对象
    :param url: url
    :return:
    """
    html = get_html(url)
    parser = etree.HTMLParser(encoding="utf-8")
    html = etree.HTML(text=html, parser=parser)
    return html

def get_detail_url(page):
    """
    获取每页的电影详情页链接
    :param page: 页码
    :return: 返回url列表
    """
    url = "http://www.dytt8.net/html/gndy/dyzz/list_23_%d.html"%page
    html = get_etree_HTML_obj(url)
    result = html.xpath("//div[@class='co_content8']/ul//a[@class='ulink']/@href")
    detail_url_list = list(map(lambda x: "http://www.dytt8.net{}".format(x),result))
    return detail_url_list

def get_movie(page):
    """ 获取每一页的电影数据 """
    url_list = get_detail_url(page)
    result = []
    for url in url_list:
        result.append(parse_detail_url(url))
    return result

if __name__ == '__main__':
    print(get_movie(1))