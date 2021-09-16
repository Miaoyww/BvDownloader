#  Copyright (c) 2021-2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
#  By Miaomiaoywww

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
    page = 1
    while True:
        all_results = Search.get_content(keyword, page)
        while True:
            selected = input(">> 请输入序号或指令: ")  # 提示输入
            try:
                selected = int(selected)
            except:
                pass
            else:
                if selected > all_results[2]: # 判断值
                    print(">> 您输入的序号过大,请重新输入")
                elif selected == 0 or selected < 0:
                    print(">> 错误的序号")
                else:
                    print(f">> 你选中的是:{selected},对应标题为:{all_results[0][selected - 1]},BVID:{all_results[1][selected - 1]}")
                    Download.autodownload(all_results[1][selected - 1])
                    exit()
            if selected == "next":  # 翻页
                print(">> 正在翻页")
                page = page + 1
                break
            elif selected == "close":  # 关闭
                print(">> 正在关闭")    
                print("...")
                time.sleep(2)
                exit()        
            else:
                print(">> 错误的指令")



if __name__ == '__main__':
    print("")
    print(">> 当前会下载登陆账号的最高画质")
    print(">> 输入Bvid或视频名称以搜索")
    print(">> 切勿高频搜索")
    print("")
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