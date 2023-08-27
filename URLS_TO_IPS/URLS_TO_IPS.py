import socket
import os
import sys
from colorama import init, Fore, Style
init(autoreset=True)

args = sys.argv
project = args[1]
资产收集 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def url_to_ip(url):
    try:
        ip = socket.gethostbyname(url)
        return ip
    except socket.gaierror:
        return None

def test_ip_connectivity(ip):
    try:
        socket.create_connection((ip, 80), timeout=5)
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def count_lines(file_path):
    with open(file_path, 'r') as f:
        return sum(1 for line in f)

def process_urls(input_file, output_file):
    live_ips = []
    dead_ips = []

    with open(input_file, 'r') as f:
        total_urls = count_lines(input_file)
        print(f"总共 {total_urls} 条URL")

        for line in f:
            url = line.strip()
            ip = url_to_ip(url)
            if ip:
                if test_ip_connectivity(ip):
                    live_ips.append(ip)
                    status = f"{Fore.GREEN}Alive{Style.RESET_ALL}"
                else:
                    dead_ips.append(ip)
                    status = f"{Fore.RED}Not Alive{Style.RESET_ALL}"
                print(f"Testing {ip} - {status}")
                with open(output_file, 'a') as out_f:
                    out_f.write(f"{ip}\n")

    return live_ips, dead_ips

if __name__ == "__main__":
    input_file = f"{资产收集}\\{project}\\{project}.txt"  # 指定包含URL的文件
    output_file = f"{project}\\IPS.txt"  # 指定存活IP的输出文件
    # 在这里创建一个空的文件，确保它存在
    with open(资产收集+"\\"+output_file, 'w') as f:
        pass

    live_ips, dead_ips = process_urls(input_file, output_file)
    total_urls = count_lines(input_file)
    print("处理完成！存活IP已保存到指定文件。\r\n")
    print(f"总共测试了 {total_urls} 条URL，对应 {len(live_ips)} 条IP地址")
    print(f"存活IP数量：{len(live_ips)}")
    print(f"死亡IP数量：{len(dead_ips)}")
