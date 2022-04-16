# -*- coding: utf-8 -*-


import time
from bvlib import Download,Search
import bilibili_api.exceptions
from bilibili_api import video


def by_bvid(input_bvid):
    Download.autodownload(input_bvid)
    exit()


def by_search(keyword):
    print(">> next可以翻到下一页")
    print(">> close可以关闭程序")
    print(">> restart可以返回主界面")
    page = 1
    while True:
        all_results = Search.get_content(keyword, page)
        while True:
            selected = input(">> 请输入序号或指令: ")  # 提示输入
            try:
                selected = int(selected)
            except:
                print(">> 请输入一个正确的 数字")
            else:
                if selected not in all_results:
                    print(">> 错误的序号")
                else:
                    print(
                        f">> 你选中的是:{selected},"
                        f"对应标题为:{all_results[selected]['title']},"
                        f"BVID:{all_results[selected]['bvid']}"
                        )
                    Download.autodownload(all_results[selected]['bvid'])
                    exit()
            if selected == "next":  # 翻页
                print(">> 正在翻页")
                page = page + 1
                break
            elif selected == "close":  # 关闭
                print(">> 正在关闭")    
                time.sleep(1)
                exit()
            elif selected == "restart":  # 重启
                print(">> 正在重启")
                print("\n\n")
                main()
            else:
                print(">> 错误的指令")
    

def main():
    while True:
        input_value = input(">> 输入: ")
        if input_value:  
            try:
                video.Video(input_value)
            except bilibili_api.exceptions.ApiException:
                by_search(input_value)
            else:
                by_bvid(input_value)
        else:
            print(">> 不可为空")


if __name__ == '__main__':
    print("")
    print(">> 当前会下载登陆账号的最高画质")
    print(">> 输入Bvid或视频名称以搜索")
    print(">> 切勿高频搜索")
    print("")
    main()