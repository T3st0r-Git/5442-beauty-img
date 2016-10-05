# -*- coding: UTF-8 -*-
#coding by v5est0r
#根据500个美女页面每页对应的大图页面,再匹配下载大图

import re,requests

from pyquery import PyQuery as pq


headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:48.0) Gecko/20100101 Firefox/48.0',}

def get_bueutyPage1(url):
    res = pq(url, headers=headers)
    #print type(res)
    jpg = res('a')

    page1 = []
    for q in jpg.items():
        q1 = q.attr('href')
        m = re.match(r"(http://www.5442.com/meinv/){1}.+\/.+html", str(q1))
        if m:
            page1.append(q1)
            page1 = list(set(page1))  # list元素去重
    #for each in page1:
        #print each
    return page1


all_beautyPage = []

for i in range(2,4):
    url = "http://www.5442.com/meinv/list_1_" + str(i) + ".html"
    print '第%s页抓到%d个大图首页' %(i,len(get_bueutyPage1(url)))
    all_beautyPage += get_bueutyPage1(url)

all_beautyPage = list(set(all_beautyPage))

chan_imglist = []
for each in all_beautyPage:
    each = each.replace(str(str(each).split("/")[5]).split(".")[0],str(str(each).split("/")[5]).split(".")[0] + '_i')
    chan_imglist.append(each)
#print chan_imglist

yuan_imglist = []
for each in all_beautyPage:
    each = each.replace(str(str(each).split("/")[5]).split(".")[0],str(str(each).split("/")[5]).split(".")[0] + '_1')
    yuan_imglist.append(each)

print '去重后总共得到 %s 个大图首页' %len(all_beautyPage)



#创建在大图首页里提取大图的函数
def get_imgUrl(url):
    img_list = []
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:48.0) Gecko/20100101 Firefox/48.0',}
    html = pq(url,headers=headers)
    img = html('img')
    for qq in img.items():
        qq1 = qq.attr('src')
        m = re.match(r"(http://pic.5442){1}.+\/[0-9]{2}\.jpg.+\.jpg", str(qq1))
        if m:
            img_list.append(qq1)
    img_list = list(set(img_list))
    return img_list

#判断页面状态 并开始抓取大图链接
'''
for imgHtml in yuan_imglist:
    r = requests.get(imgHtml, allow_redirects=False)
    if r.status_code == 200:
        for i in range(0, 40):
            try:
                for each in chan_imglist:
                    each = each.replace('_i', "_" + str(i))
                    print each
                    get_imgUrl(each)
                    print '本页抓取到%d张大图' % len(get_imgUrl(url))
            except:
                pass
'''

all_imglist = []
for i in range(1, 3):
    for each in chan_imglist:
        each = each.replace('_i', "_" + str(i))
        #print each
        r = requests.get(each, allow_redirects=False)
        if r.status_code==200:
            #print each
            get_imgUrl(each)
            for imgUrl in get_imgUrl(each):
                all_imglist.append(imgUrl)
                all_imglist = list(set(all_imglist))
            print "本页抓取到 %d 张大图" % len(get_imgUrl(each))
    print "这个大图首页系列共抓取到 %d 张大图" %len(all_imglist)
    all_imglist += all_imglist
print "合计共抓取到 %d 张大图" %len(all_imglist)

for each in all_imglist:
    print each