import requests
import os
import sys
from urllib import parse as up
import urllib3
import re
import traceback
import time


def cd(path):
    if os.path.exists(path):
        os.chdir(path)
    else:
        os.makedirs(path, exist_ok=True)
        os.chdir(path)
# 计算文件大小


def readable_file_size(bytes, precision) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']:
        if abs(bytes) < 1024.0:
            return '%s%s' % (format(bytes, '.%df' % precision), unit)
        bytes /= 1024.0
    return '%s %s' % (format(bytes, '.%df' % precision), 'Yi')


passwd = "VIP666"

url = sys.argv[1]
try:
    filename = sys.argv[2]
except Exception:
    if up.unquote(up.urlsplit(url).path.split("/")[-1]) != "":
        filename = up.unquote(up.urlsplit(url).path.split("/")[-1])
    else:
        filename = up.urlsplit(url).hostname+".html"
try:
    speed = sys.argv[3]
    speed = int(speed)
except Exception:
    speed = 8192
try:
    path = sys.argv[4]
except Exception:
    path = "."
try:
    browser = sys.argv[5]
except Exception:
    browser = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"


def main():
    headers = {"User-Agent": browser}
    print("正在请求")
    try:

        html = requests.get(url, headers=headers,
                            stream=True, timeout=3000)
        print("请求成功")
    except TimeoutError:
        print("请求超时")
    except Exception:
        print("请求错误")
    else:
        echo_num = 0
        cd(path)
        ok = True
        is_open = False
        if filename in os.listdir():
            p = input("那个目录下有这个文件：%s，请指示\nw: 覆盖\nq: 结束\n" % filename)
            if p.upper() == "W":
                f = open(filename, "wb+")
                is_open = True
            elif p.upper() == "Q":
                ok = False
        if ok == False:
            return None
        if is_open == False:
            f = open(filename, "wb+")

        is_say = False
        is_close = False

        # print("正在获取数据")
        # content = html.content
        # num = len(content)
        # print("获取ok")
        # print("本次下载字节数："+readable_file_size(num, 1))
        # print("ok")
        password = input("请输入下载密码(不会输Not)：\n")
        if password.upper() == passwd.upper():
            print("OK, Yes!")
            for x in html.iter_content(speed):
                try:
                    f.write(x)
                    echo_num += len(x)
                    # print("一共写入%s个字符" % str(echo_num))
                    print("本次写入{}个字符，一共写入{}个字符".format(
                        str(len(x)), str(echo_num)))
                    # print("本次写入{}个字符，一共写入{}个字符，还差{}个字符结束".format(str(len(x)), str(echo_num), str(num-echo_num)))
                    # print("本次写入{}个字符，一共写入{}个字符，还差{}个字符结束， 下载进度：{:.3f}%".format(
                    # str(len(x)), str(echo_num), str(num-echo_num), float(echo_num)/float(num)*100))
                    # print("本次写入%s个字符" % str(len(x)))
                except Exception:
                    traceback.print_exc()
                    is_say = True
                    is_close = True
                    print("下载失败")
                    f.close()
                    break
            if is_say == False:
                f.close()
                is_say = True
            if is_close == False:
                print("下载完成")
                is_say = True
        else:
            print("OH, No!")
            for x in html.iter_content():
                try:
                    f.write(x)
                    echo_num += len(x)
                    # print("一共写入%s个字符" % str(echo_num))
                    # print("本次写入{}个字符，一共写入{}个字符".format(str(len(x)), str(echo_num)))
                    # print("本次写入{}个字符，一共写入{}个字符，还差{}个字符结束".format(str(len(x)), str(echo_num), str(num-echo_num)))
                    print("本次写入{}个字符，一共写入{}个字符，还差{}个字符结束， 下载进度：{:.3f}%".format(
                        str(len(x)), str(echo_num), str(num-echo_num), float(echo_num)/float(num)*100))
                    # print("本次写入%s个字符" % str(len(x)))
                    time.sleep(7)
                except Exception:
                    traceback.print_exc()
                    is_say = True
                    is_close = True
                    print("下载失败")
                    f.close()
                    break
            if is_say == False:
                f.close()
                is_say = True
            if is_close == False:
                print("下载完成")
                is_say = True


if __name__ == "__main__":
    main()
