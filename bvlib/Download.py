from bilibili_api import video, sync
from tqdm import tqdm
import requests
import os
import re
import math
import time
import ffmpy

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bilibili.com/"
}


def autodownload(bvid):
    video_info = get_video_info(bvid)  # 获取 标题 作者
    av_url = get_download_url(bvid)  # 获取 视频链接 音频链接
    if os.path.exists(f"{video_info[0]}.mp4"):  # 判断相同文件是否存在
        while True:
            decide = input(f">> 相同文件: '{video_info[0]}.mp4' 已经存在，是否替换?(y/n): ")
            if decide == "y":
                os.remove(f"{video_info[0]}.mp4")
                down(av_url[0], av_url[1])
                ffmpeg(video_info[0])
                exit()
            elif decide == "n":
                print(">> 已取消下载")
                print("...")
                time.sleep(2)
                exit()
            else:
                print(">> 你只能输入y 或 n")
    down(av_url[0], av_url[1])
    ffmpeg(video_info[0])


# 获取音视频链接
def get_download_url(bvid):
    new_bvid = video.Video(bvid)  # 实例化
    url = sync(new_bvid.get_download_url(page_index=0))  # 获取资源链接

    video_url = url['dash']['video'][0]['base_url']  # 视频链接
    audio_url = url['dash']['audio'][0]['base_url']  # 音频链接
    av_url = [video_url, audio_url]  # 将所有的信息集合成一个文件

    return av_url


# 获取视频信息
def get_video_info(bvid):
    new_bvid = video.Video(bvid)  # 实例化
    get_info = sync(new_bvid.get_info())  # 获取视频信息

    video_title = get_info['title']  # 标题
    strs = r"[\/\\\:\*\?\"\<\>\|]"  # 非法字符的定义
    video_title = re.sub(strs, "_", video_title)  # 更改视频标题中所有的非法字符
    video_owner = get_info['owner']['name']  # 所有者

    video_info = [video_title,video_owner]
    print(">> 视频信息: \n" 
          f">> 标题: {video_title} \n"
          f">> 作者: {video_owner}")

    return video_info


# 下载
def down(video_url, audio_url):
    get_video = requests.get(video_url, headers=headers, stream=True)  # 视频资源
    video_size = math.ceil(int(get_video.headers.get('Content-Length')) / 1024 / 1024)
    get_audio = requests.get(audio_url, headers=headers, stream=True)  # 音频资源
    audio_size = math.ceil(int(get_audio.headers.get('Content-Length')) / 1024 / 1024)
    print(f">> 获取到视频大小: {video_size}MB")
    print(f">> 获取到音频大小: {audio_size}MB")
    print(">> 开始下载")
    with open("videotemp.mp4", "wb") as w:
        for data in tqdm(iterable=get_video.iter_content(1024 * 1024), total=video_size, desc='>> 正在下载 视频文件',
                         unit='MB'):
            w.write(data)
    with open("audiotemp.mp3", "wb") as w:
        for data in tqdm(iterable=get_audio.iter_content(1024 * 1024), total=audio_size, desc='>> 正在下载 音频文件',
                         unit='MB'):
            w.write(data)


# 混流
def ffmpeg(video_title):
    ff = ffmpy.FFmpeg(
    inputs={'videotemp.mp4': None,
            'audiotemp.mp3': None
    },
    outputs={f'{video_title}.mp4': [
        '-vcodec', 'copy',
        '-acodec', 'copy'
    ]}
    )
    ff.run()
    os.remove("videotemp.mp4")
    os.remove("audiotemp.mp3")
    print(">> 下载成功")
    print("...")
    time.sleep(2)
