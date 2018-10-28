"""
爬取豆瓣正在上映的电影和即将上映的电影
"""
import requests
from lxml import etree

def get_html(region):
    """
    抓取页面
    :param region: 地区
    :return: html
    """
    url = "https://movie.douban.com/cinema/nowplaying/%s/"%region
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/70.0.3538.67 Safari/537.36",
        "Referer":"https://movie.douban.com/"
    }
    response = requests.get(url,headers=headers)
    return response.text

def get_data(ul_element):
    """
    解析数据
    :param ul_element: ul元素
    :return:
    """
    li_list = ul_element.xpath(".//li[@class='list-item']")
    result = []
    for li in li_list:
        item = {}
        item["title"] = li.xpath("@data-title")[0]         # 电影标题
        item["duration"] = li.xpath("@data-duration")[0]   # 电影时长
        item["region"] = li.xpath("@data-region")[0]       # 地区
        item["director"] = li.xpath("@data-director")[0]   # 导演
        item["actors"] = li.xpath("@data-actors")[0]       # 主演
        item["category"] = li.xpath("@data-category")[0]   # 状态类型,正在上映，即将上映
        if item["category"] == "nowplaying":
            item["poster"] = li.xpath(".//img[@src]/@src")[0]   # 获取封面
            item["score"] = li.xpath("@data-score")[0]          # 评分
            item["release"] = li.xpath("@data-release")[0]      # 上映年份
            item["votecount"] = li.xpath("@data-votecount")[0]  # 评论人数
        elif item["category"] == "upcoming":
            item["wish"] = li.xpath("@data-wish")[0]       # 想看人数
            item["release"] = li.xpath("./ul/li[3]/text()")[0].strip()
        result.append(item)
    return result

def parse_html(html):
    """
    解析html数据
    :param html: html字符串
    :return: 数据字典
    """
    parser = etree.HTMLParser(encoding="utf-8")
    html = etree.HTML(text=html,parser=parser)
    # 获取正在上映和准备上映两个ul
    now_playing,upcoming = html.xpath("//ul[@class='lists']")
    result = {}
    item = get_data(now_playing)
    result["now_playing"] = item
    item = get_data(upcoming)
    result["upcoming"] = item
    return result

if __name__ == '__main__':
    html = get_html("shenzhen")
    print(parse_html(html))



