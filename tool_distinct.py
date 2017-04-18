# -*- coding: utf-8 -*-

"""
    此脚本可将文本文件中的重复值去除。

    Last commit info:
    ~~~~~~~~~~~~~~~~~
    $LastChangedDate: 3/2/2017
    $Annotation: Create.
    $Author: xiyan19
"""


import sys


if __name__ == '__main__':
    # 按行读取文件内容到list中
    input_file_path = sys.argv[1]
    input_file = open(input_file_path, 'r')
    text = []
    for line in input_file:
        text.append(line)

    input_file.close()

    # 去重
    text = list(set(text))

    # 输出
    output_file_path = input_file_path + ".distinct"
    output_file = open(output_file_path, 'w')
    for line in text:
        output_file.write(line)

    output_file.close()