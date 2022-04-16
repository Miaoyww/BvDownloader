from bs4 import *
import requests


# 头
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bilibili.com/"
}


# 获取页面的html
def get_html(keyword, page):
    url = rf"https://search.bilibili.com/all?keyword={keyword}&page={page}"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


# 获取Bvid
def get_bvid(bvid_soup):
    targets = bvid_soup.find_all('li', class_="video-item matrix")
    bvid = []
    url = []  # 用于迭代出bvid
    url2 = []  # 同
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


# 获取页面内容
def get_content(keyword, page):
    search_results = get_html(keyword, page)
    print(f">> ------ 当前页数:{page} ------")
    title_results = get_title(search_results)  # 视频标题
    up_results = get_up(search_results)  # up主名称
    bvid_results = get_bvid(search_results)  # 视频bvid
    maxlist = len(title_results)  # 一个页面最多显示的视频数
    index = 1  # 序号
    result = {
        
    }
    for (title_item, up_item) in zip(title_results, up_results):
        print(f"No.{index}: {title_item}")
        print(f"Up主: {up_item}")
        result[index] = {
            "title": title_item,
            "up": up_item,
            "bvid": bvid_results[index - 1]
        }
        index = index + 1
    print(">> ------ END")

    return result
