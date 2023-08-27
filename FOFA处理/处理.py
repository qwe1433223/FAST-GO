import os
import sys
import argparse
import pandas as pd
import chardet
import glob
from urllib.parse import urlparse


资产收集 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_encoding(file):
    with open(file, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def process_csv_files(input_dir):
    data = []

    # 遍历指定目录下的所有.csv文件
    指定目录 = os.path.join(资产收集, input_dir)

    
    for filename in os.listdir(指定目录):
        if filename.endswith(".csv"):
            file_path = os.path.join(指定目录, filename)
            df = pd.read_csv(file_path, encoding=get_encoding(file_path))
            if 'link' in df.columns:
                data.extend([str(link) for link in df['link'].tolist()])  # 将 link 转换为字符串
            if 'url' in df.columns:    
                data.extend([str(url) for url in df['url'].tolist()])
    return data



def remove_protocol(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc:
        return parsed_url.netloc
    return url

def append_and_deduplicate(file1, file2):
    # 读取 file1 的内容
    with open(file1, 'r') as f:
        lines_to_append = f.readlines()

    # 读取 file2 的内容
    with open(file2, 'r') as f:
        original_lines = f.readlines()

    # 将 file1 的内容追加到 file2 的内容
    all_lines = original_lines + lines_to_append

    # 去重
    unique_lines = list(set(all_lines))

    # 将去重后的内容写回 file2
    with open(file2, 'w') as f:
        f.writelines(unique_lines)

# 使用方法：
# append_and_deduplicate('file1.txt', 'file2.txt')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CSV files and append to a target text file.")
    parser.add_argument("project", help="指定从x.csv读取url的目标目录")
    args = parser.parse_args()

    PROJECT = args.project
    output_filename = f"{资产收集}\\{PROJECT}\\{PROJECT}.txt"
    
    data = process_csv_files(PROJECT)
    data = [remove_protocol(url) for url in data]
    
    with open(output_filename, 'w') as f:
        for item in data:
            f.write("%s\n" % item)
    print("处理完成，生成文件：{}".format(output_filename))
    

    target_files = glob.glob(f"资产收集\\{PROJECT}\\OneForAll\\all_subdomain_result_*.txt")
    
    for target_file in target_files:
        append_and_deduplicate(target_file,f"{资产收集}\\{PROJECT}\\{PROJECT}.txt")