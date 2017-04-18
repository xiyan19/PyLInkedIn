# -*- coding: utf-8 -*-

"""
    此模块用于测试网络连接是否正常。

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate: 2/26/2017
    $Annotation: Create.
    $Author: xiyan19
"""


import time
import module_Ping


def netCheck(website):
    """
    此函数使用Ping方法测试网络简介是否正常。

    :param website: list
    :return: 无
    """
    print("*******************Start Network Test in module_Ping.py*******************")
    for url in website:
        str_time = time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime(time.time()))
        print("Ping %s at %s" % (url, str_time))
        module_Ping.M_verbose_ping(url)
    print("*******************End Network Test in module_Ping.py*******************")


if __name__ == '__main__':
    # 需要测试的URL
    web_google = "www.google.com"
    web_linkedIn = "www.linkedin.com"
    website = [web_google, web_linkedIn]

    netCheck(website)