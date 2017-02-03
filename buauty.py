# -*- coding: utf-8 -*-
#coded by v5est0r

import re,requests,urllib

from pyquery import PyQuery as pq

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:48.0) Gecko/20100101 Firefox/48.0',}

#http://www.5442.com/meinv/20150813/26143_9.html
#http://www.5442.com/meinv/20170203/40483_14.html

def get_bueutyPage1(url):
    try:
        res = pq(url, headers=headers)
        jpg = res('a')
        page1 = []
        for q in jpg.items():
            q1 = q.attr('href')
            m = re.match(r"(http://www.5442.com/meinv/){1}.+\/.+html", str(q1))
            if m:
                page1.append(q1)
                page1 = list(set(page1))  # ist元素去重
    except:
        pass
    return page1

all_beautyPage = []
for i in range(1, 490):
    url = "http://www.5442.com/meinv/list_1_" + str(i) + ".html"
    print "正在匹配list1第%d页的图集首页"%i
    try:
        all_beautyPage += get_bueutyPage1(url)
    except:
        pass

all_beautyPage = list(set(all_beautyPage))
print '去重后总共得到 %s 个大图首页' %len(all_beautyPage)

chan_imglist = []
for each in all_beautyPage:
    each = each.replace(str(str(each).split("/")[5]).split(".")[0],str(str(each).split("/")[5]).split(".")[0] + '_i')
    chan_imglist.append(each)
chan_imglist = list(set(chan_imglist))

#http://www.5442.com/meinv/20150314/16576_i.html
#每个大图系列提取大图并下载
def get_img(img_html):
    #print img_html
    for i in range(5,7):
        img_list = []
        img_html1=img_html.replace('_i','_'+str(i))
        try:
            r = requests.get(img_html1, allow_redirects=False)
            if r.status_code == 200:
                print "正在匹配大图页:%s" % img_html1
                html = pq(img_html1, headers=headers)
                img = html('img')
                for qq in img.items():
                    qq1 = qq.attr('src')
                    m = re.match(r"(http://image.ytqmx){1}.+!960.jpg", qq1)
                    n = re.match(r"(http://){1}.+!960.jpg", qq1)
                    if m or n:
                        img_list.append(qq1)
                img_list += img_list
                img_list = list(set(img_list))
                print "本页抓取到%d张大图" % len(img_list)
                for pic_url in img_list:
                    print('正在下载图片%s') % pic_url
                    filename = pic_url.replace(r'/', 'v5est0r')
                    try:
                        data = urllib.urlretrieve(pic_url,filename)
                    except:
                        pass
            else:
                break
        except:
            pass
    return;


for each in chan_imglist:
    get_img(each)

#get_img("http://www.5442.com/meinv/20150813/26143_i.html")
