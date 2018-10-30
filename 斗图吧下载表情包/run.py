import requests,os,re
from lxml import etree
from urllib import request
import queue,threading

class Producer(threading.Thread):
    """ 生产者：负责获取图片url """
    def __init__(self,url_queue,image_queue,*args,**kwargs):
        super(Producer, self).__init__(*args,**kwargs)
        self.url_queue = url_queue
        self.image_queue = image_queue

    def run(self):
        while True:
            if self.url_queue.empty():
                # url_queue为空表示获取url完成
                break
            url = self.url_queue.get()
            self.get_image_url(url)

    def get_html(self,url):
        """ 获取html """
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/70.0.3538.67 Safari/537.36"
        }
        response = requests.get(url,headers=headers)
        response.encoding = "utf-8"
        return response.text

    def get_image_url(self,url):
        """ 获取图片url """
        html = self.get_html(url)
        parser = etree.HTMLParser(encoding="utf-8")
        html = etree.HTML(text=html,parser=parser)
        img_list = html.xpath("//div[@class='page-content text-center']//img")
        for img in img_list:
            try:
                url = img.xpath("@data-original")[0][:-4]
                name = img.xpath("@alt")[0]
                name = re.sub(r"[？！。，\*\.]","",name)
                suffix = os.path.splitext(url)[1]
                filename = "{}{}".format(name,suffix)
                self.image_queue.put((url,filename))
            except Exception as e:
                pass

class Downloader(threading.Thread):
    """ 下载器 """
    def __init__(self,url_queue,image_queue,save_folder,*args,**kwargs):
        super(Downloader, self).__init__(*args,**kwargs)
        self.url_queue = url_queue
        self.image_queue = image_queue
        self.save_folder = save_folder

    def run(self):
        while True:
            if self.image_queue.empty() and self.url_queue.empty():
                # 若两个队列同时为空表示下载完成
                break
            url,filename = self.image_queue.get()
            filepath = os.path.join(self.save_folder,filename)
            self.download_image(url,filepath)
            print(filename,"下载完成")

    def download_image(self,url,file_path):
        """ 下载图片 """
        request.urlretrieve(url,file_path)

if __name__ == '__main__':
    url_queue = queue.Queue(100)        # url队列
    image_queue = queue.Queue(1000)     # 图片队列
    url = "http://www.doutula.com/photo/list/?page={page}"
    for i in range(1,100):
        temp_url = url.format(page=i)
        url_queue.put(temp_url)
    root_path = os.path.dirname(os.path.abspath(__file__))
    save_folder = os.path.join(root_path,"images")
    if not os.path.exists(save_folder):
        # 若文件夹不存在则创建这个文件夹
        os.makedirs(save_folder)
    # 创建5个生产者
    for i in range(5):
        p = Producer(url_queue,image_queue)
        p.start()
    # 创建10个下载器
    for i in range(10):
        d = Downloader(url_queue,image_queue,save_folder)
        d.start()





