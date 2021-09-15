#  Copyright (c) 2021-2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.
#  By Miaomiaoywww

import time
from bvlib import Download,Page
import bilibili_api.exceptions
from bilibili_api import video


def by_bvid():
    while True:
        input_bvid = input(">> Input: 输入Bvid: ")
        try:
            video.Video(input_bvid)
        except bilibili_api.exceptions.ApiException:
            print(">> ERROR: bvid 提供错误，必须是以 BV 开头的纯字母和数字组成的 12 位字符串（大小写敏感）。")
        else:
            Download.auto(input_bvid)
            exit()


def by_search():
    print(">> 100可以翻到下一页")
    print(">> 0可以重新搜索")
    print(">> -100可以关闭程序")
    while True:
        page = 1
        input_kyw = input(">> 搜索: ")
        while True:
            all_results = Page.res_page(input_kyw, page)
            selected = int(input(">> 请输入序号: "))  # 提示输入序号
            if selected == 100:  # 1为翻页
                print(">> 正在翻页")
                page = page + 1
            elif selected > all_results[2]:  # 判断是否大于最大长度
                print(">> 您输入的序号过大,请重新输入")
            elif selected == +0:  # 0为重新搜索
                print(">> 重新搜索")
                break
            elif selected == -100:  # -1为关闭
                print(">> 正在关闭")
                print("...")
                time.sleep(2)
                exit()
            else:
                print(f">> 你选中的是:{selected},对应标题为:{all_results[0][selected - 1]},BVID:{all_results[1][selected - 1]}")
                print(">> 正在下载")
                Download.auto(all_results[1][selected - 1])
                exit()


if __name__ == '__main__':
    print("")
    print(">> 当前会下载登陆账号的最高画质")
    print(">> 你可以选择一下两种Get视频的方式: ")
    print(">> 1.Bvid直接Get     2.通过搜索Get")
    print("")
    while True:
        try:
            decide = int(input(">> 请输入你的选择: "))
            print("")
        except ValueError:
            print(">> 错误的选择")
        else:
            if decide == 1:
                by_bvid()
                break
            elif decide == 2:
                by_search()
                break
            else:
                print(">> 错误的选择")
