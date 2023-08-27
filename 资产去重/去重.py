import requests
import sys
import os
import re
import pickle
import traceback  
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from termcolor import cprint
from time import sleep
import argparse
import configparser
import json

#命令参数
parser = argparse.ArgumentParser(description='Process input arguments.')
parser.add_argument('-P', '-p', '--project', type=str, help='Project name', default=None)
parser.add_argument('-C', '-c', '--is_continue', type=int, help='Continue flag', default=0)
parser.add_argument('positional_project', nargs='?', default=None)
parser.add_argument('positional_continue', nargs='?', default=None)

args = parser.parse_args()

# 如果通过位置参数传递，则使用它们
if args.positional_project:
    project = args.positional_project
    IS_CONTINUE = args.positional_continue if args.positional_continue else 0
else:
    project = args.project
    IS_CONTINUE = args.is_continue
IS_CONTINUE = int(IS_CONTINUE)

#全局变量
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
资产收集 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL_FILE = f"{资产收集}\\{project}\\200.txt"
URL_LIST = []
URL_SCRIPT_DIC = {}
RESPONSE = ""
COUNT_ERROR_资产 = 0
COUNT_没有JS资产 = 0
NO_COMPARES_URLS = []
COMPARES_URLS = []
OUT_URLS_OK = []
OUT_URLS_BAD = []
COUNT_COMPARED_URLS = 0
单独模板开发的WEB资产 = []
取JS个数 = 6
比较阈值 = 4

OK_OUT_PATH = f"{资产收集}/{project}/单独开发资产.txt"
BAD_OUT_PATH = f"{资产收集}/{project}/模板开发资产.txt"


def get_url_from_file():
    """从文件中获取URL列表"""
    try:
        with open(URL_FILE, "r") as f:
            urls = f.readlines()
        for url in urls:
            URL_LIST.append(url.strip())
        return URL_LIST
    except Exception as e:
        print(f"Error reading URL file: {e}")
        return []

def get_javascript(url):
    global COUNT_ERROR_资产
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        cprint("***",end="",color="yellow")
        response = requests.get(url, verify=False)  # 禁用SSL证书验证
        response.raise_for_status()
        cprint("***",end="",color="yellow")
        return response.text
    except requests.RequestException as e:
        COUNT_ERROR_资产 += 1
        cprint(f"这个资产发生错误：{url}. Error: {e}", color="red", end="")
        NO_COMPARES_URLS.append(url)
        return ""  # 返回空字符串而不是空列表


def extract_javascript(前端代码, url):
    global COUNT_没有JS资产
    global NO_COMPARES_URLS
    global 取JS个数
    print(">>> ", end="")
    正则表达式 = r'(<script[^>]*>.*?</script>)'
    JavaScripts = re.findall(正则表达式, 前端代码, re.DOTALL)

    输出信息 = f" {url} "
    print(f"{输出信息:<{60}}",end="")
    
    if JavaScripts:  # 检查列表是否不为空
        if JavaScripts[0]:  # 检查第一个元素是否存在
            cprint("提取JS成功 [√]",color="green")
        else:
            COUNT_没有JS资产 += 1
            cprint("没有JS内容 [X]",color="red")
            NO_COMPARES_URLS.append(url)
    else:
        COUNT_没有JS资产 += 1
        cprint("没有找到JavaScript片段 [X]", color="red")
        NO_COMPARES_URLS.append(url)
        return []

    return JavaScripts[:取JS个数]



def compare_websites():
    global 取JS个数
    global 比较阈值
    global COUNT_COMPARED_URLS
    global OUT_URL_BAD

    单独模板开发资产 = set(COMPARES_URLS)
    for url1 in COMPARES_URLS:
        COUNT_COMPARED_URLS += 1
        for url2 in COMPARES_URLS:
            if url1 != url2 and url1 in 单独模板开发资产 and url2 in 单独模板开发资产:
                matching_script_part = 0
                for i in range(min(len(URL_SCRIPT_DIC[url1]), len(URL_SCRIPT_DIC[url2]), 取JS个数)):
                    if URL_SCRIPT_DIC[url1][i] == URL_SCRIPT_DIC[url2][i]:
                        #片段相同
                        matching_script_part += 1


                if matching_script_part >= 比较阈值:
                    OUT_URLS_BAD.append(url2)
                    输出信息 = f"{url1:<50}{url2:<50}"
                    cprint(f"{输出信息}[相似]", color="red")
                    单独模板开发资产.remove(url2)
        
    return 单独模板开发资产

def save_to_config():
    global NO_COMPARES_URLS, COMPARES_URLS, URL_LIST
    global COUNT_ERROR_资产, COUNT_没有JS资产, 取JS个数, 比较阈值
    global CURRENT_PATH

    config = configparser.ConfigParser()
    temp = configparser.ConfigParser()

    config['Settings'] = {
        '取JS个数': 取JS个数,
        '比较阈值': 比较阈值,
    }

    temp['temp'] = {
        'NO_COMPARES_URLS': json.dumps(NO_COMPARES_URLS),
        'COMPARES_URLS': json.dumps(COMPARES_URLS),
        'URL_LIST': json.dumps(URL_LIST),
        'COUNT_ERROR_资产': COUNT_ERROR_资产,
        'COUNT_没有JS资产': COUNT_没有JS资产,
    }

    if not os.path.exists(f'{CURRENT_PATH}\\config'):
        os.makedirs('config')

    with open(f'{CURRENT_PATH}\\config\\config.ini', 'w') as configfile:
        config.write(configfile)

    with open(f'{CURRENT_PATH}\\config\\temp.ini', 'w') as tempfile:
        temp.write(tempfile)

def load_from_config():
    global NO_COMPARES_URLS, COMPARES_URLS, URL_LIST
    global COUNT_ERROR_资产, COUNT_没有JS资产, 取JS个数, 比较阈值
    global CURRENT_PATH

    config = configparser.ConfigParser()
    temp = configparser.ConfigParser()

    if not os.path.isfile(f'{CURRENT_PATH}\\config\\config.ini'):
        save_to_config()

    config.read(f'{CURRENT_PATH}\\config\\config.ini')
    temp.read(f'{CURRENT_PATH}\\config\\temp.ini')

    NO_COMPARES_URLS = json.loads(temp['temp']['NO_COMPARES_URLS'])
    COMPARES_URLS = json.loads(temp['temp']['COMPARES_URLS'])
    URL_LIST = json.loads(temp['temp']['URL_LIST'])
    COUNT_ERROR_资产 = int(temp['temp']['COUNT_ERROR_资产'])
    COUNT_没有JS资产 = int(temp['temp']['COUNT_没有JS资产'])
    #取JS个数 = int(config['Settings']['取JS个数'])
    #比较阈值 = int(config['Settings']['比较阈值'])


def end():
    global NO_COMPARES_URLS
    global 单独模板开发的WEB资产
    global OUT_URLS_OK
    global OUT_URLS_BAD
    global OK_OUT_PATH
    global BAD_OUT_PATH
    global COUNT_COMPARED_URLS
    OUT_URLS_OK = NO_COMPARES_URLS + list(单独模板开发的WEB资产)

    with open(OK_OUT_PATH, 'w') as file:
        for item in OUT_URLS_OK:
            file.write("%s\n" % item)
    with open(BAD_OUT_PATH, 'w') as file:
        for item in OUT_URLS_BAD:
            file.write("%s\n" % item)    
    横杠 = "-"
    cprint(f"\n{横杠*150}\n",color="yellow")
    cprint(">>> 以下URL使用了独特的模板：",color="green")
    for url in 单独模板开发的WEB资产:
        cprint(f"{url:<100}[√]", color="green")

    cprint(f"\n{横杠*150}\n",color="yellow")
    cprint(f"共{COUNT_ERROR_资产}条错误请求资产",color="green")
    cprint(f"共{COUNT_没有JS资产}条资产没有JS",color="green")    
    cprint(f"已检查{COUNT_COMPARED_URLS}条资产是否相重合\n",color="green")
    cprint(f"\t{len(OUT_URLS_OK)}条独立资产")
    cprint(f"\t{len(OUT_URLS_BAD)}条模板资产")

if __name__ == '__main__':
    try:
        #如果为继续，则直接读取序列化后的数据，
        #如果不继续，则请求并且解析，然后反序列化存入serialize.data
        
        if(IS_CONTINUE == 1):
            print("正在加载数据")
            load_from_config()
            URL_SCRIPT_DIC = pickle.load(open(f"{CURRENT_PATH}\\config\\URL_SCRIPT_DIC.data", "rb"))
        else:
            print("去重启动中")
            URL_LIST = get_url_from_file()
            for url in URL_LIST:
                RESPONSE = get_javascript(url)
                URL_SCRIPT_DIC[url] = extract_javascript(前端代码=RESPONSE, url=url)
            COMPARES_URLS = list(set(URL_LIST) - set(NO_COMPARES_URLS))
            save_to_config()
            with open(f"{CURRENT_PATH}\\config\\URL_SCRIPT_DIC.data", "wb") as file:
                pickle.dump(URL_SCRIPT_DIC, file)
                
       
        单独模板开发的WEB资产 = compare_websites()
        
    except Exception as e:
        error_msg = f"An unexpected error occurred: {e}\n"
        tb = traceback.format_exc()  # 获取完整的异常跟踪信息
        error_msg += tb  # 将跟踪信息添加到错误消息中
        print(error_msg)
    end()