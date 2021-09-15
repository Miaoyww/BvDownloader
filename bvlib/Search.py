from bs4 import *
import requests

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bilibili.com/"
}


# 获取搜索页面的内容
def search(keyword, page):
    url = rf"https://search.bilibili.com/all?keyword={keyword}&page={page}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


# Bvid
def get_bvid(bvid_soup):
    targets = bvid_soup.find_all('li', class_="video-item matrix")
    bvid = []
    url = []
    url2 = []
    for url_item in targets:
        url_targets = url_item.find_all("a", class_="img-anchor")
        url.append(url_targets[0].get("href"))
    for url2_item in url:
        url2.append(url2_item.split("/"))
    for bvid_each in url2:
        bvid.append(bvid_each[4].split("?")[0])
    return bvid


# 获得Up主
def get_up(up_soup):
    targets = up_soup.find_all("span", title="up主", class_="so-icon")
    up = []
    for up_item in targets:
        up.append(up_item.a.text)
    return up


# 获取标题
def get_title(title_soup):
    targets = title_soup.find_all('li', class_="video-item matrix")
    title = []
    for title_item in targets:
        title_targets = title_item.find_all("a", class_="img-anchor")
        title.append(title_targets[0].get("title"))
    return title


# 打印内容
def res_page(keyword, page):
    search_results = search(keyword, page)
    print(f">> ------ 当前页数:{page} ------")
    title_results = get_title(search_results)
    up_results = get_up(search_results)
    bvid_results = get_bvid(search_results)
    maxlist = len(title_results)
    index = 1
    for (title_item, up_item) in zip(title_results, up_results):
        print(f"No.{index}: {title_item}")
        print(f"Up主: {up_item}")
        index = index + 1
    print(">> ------ END")
    return title_results, bvid_results, maxlist
