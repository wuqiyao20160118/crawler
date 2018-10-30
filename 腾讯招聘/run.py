"""
练习抓取腾讯招聘信息
"""
import requests
from bs4 import BeautifulSoup

def get_job_detail(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
    }
    result = {}
    response = requests.get(url,headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text,"lxml")
    result["sharetitle"] = soup.find_all("td",id="sharetitle")[0].string.strip()
    tr = soup.find_all("tr",class_="c bottomline")[0]
    td_list = tr.find_all("td")
    result["workplace"] = td_list[0].text[5:]
    result["jobcategory"] = td_list[1].text[5:]
    result["number"] = td_list[2].text[5:]
    ul_list = soup.find_all("ul",class_="squareli")
    result["job_duties"] = ul_list[0].text
    result["job_claim"] = ul_list[1].text
    print(result)

def get_job_urls(keywords,start):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
    }
    url = "https://hr.tencent.com/position.php?keywords={}&start={}#a".format(keywords,start)
    response = requests.get(url,headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text,"lxml")
    tr_list = soup.find_all("tr",class_="even") + soup.find_all("tr",class_="odd")
    url_list = []
    for tr in tr_list:
        a = tr.find_all("a")[0]
        url_list.append(a["href"])
    url_list = list(map(lambda x:"https://hr.tencent.com/{}".format(x),url_list))
    return url_list

if __name__ == '__main__':
    url_list = get_job_urls("python",0)
    result = []
    for url in url_list:
        result.append(get_job_detail(url))