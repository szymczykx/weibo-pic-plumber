import dns.resolver
import json
from tqdm import tqdm
import argparse
import requests
from urllib.parse import urlparse
import os
import random

# 预定义的CDN服务器列表（2024年最新观测）
CDN_DOMAINS = [
    'wx1.sinaimg.cn', 'wx2.sinaimg.cn', 'wx3.sinaimg.cn', 'wx4.sinaimg.cn',
    'ww1.sinaimg.cn', 'ww2.sinaimg.cn', 'ww3.sinaimg.cn', 'ww4.sinaimg.cn',
    'ws1.sinaimg.cn', 'ws2.sinaimg.cn', 'ws3.sinaimg.cn', 'ws4.sinaimg.cn',
    'tva1.sinaimg.cn', 'tva2.sinaimg.cn', 'tva3.sinaimg.cn', 'tva4.sinaimg.cn',
    'g.us.sinaimg.cn'
]

# 预定义的 DNS 服务器列表
# DNS_SERVERS = [
#     "8.8.8.8",
#     "8.8.4.4",
#     "1.1.1.1",
#     "1.0.0.1",
#     "223.5.5.5",
#     "223.6.6.6"
# ]

DNS_SERVERS = ["119.29.29.29","223.5.5.5","223.6.6.6","180.76.76.76","101.226.4.6","218.30.118.6","123.125.81.6","140.207.198.6","1.1.1.1","182.254.116.116","8.8.8.8","8.8.4.4","1.0.0.1","9.9.9.9","149.112.112.112","94.140.14.14","94.140.15.15","45.90.28.0","45.90.30.0","208.67.222.222","208.67.220.220","77.88.8.8","77.88.8.1","185.228.168.9","185.228.169.9","172.104.93.80","8.26.56.26","84.200.69.80","46.250.226.242","76.76.2.1","114.114.114.114","114.114.115.115","182.254.118.118","1.2.4.8","210.2.4.8","199.85.126.10","199.85.127.10","84.200.70.40","8.20.247.20","64.6.64.6","64.6.65.6","192.95.54.3","192.95.54.1","81.218.119.11","209.88.198.133","80.80.80.80","80.80.81.81","168.126.63.1","168.126.63.2","202.38.93.153","202.141.162.123","202.141.178.13","178.79.131.110","112.124.47.27","114.215.126.16","202.96.128.86","202.103.24.68","202.96.128.166","202.103.0.68","202.96.134.33","202.96.128.68","222.246.129.80","59.51.78.211","61.177.7.1","221.228.255.1","202.103.225.68","202.103.224.68","61.147.37.1","218.2.135.1","61.139.2.69","218.6.200.139","202.96.209.133","116.228.111.118","61.128.192.68","202.96.209.5","61.128.128.68","180.168.255.118","222.172.200.68","202.101.172.35","61.166.150.123","61.153.177.196","61.153.81.75","202.98.192.67","60.191.244.5","202.98.198.167","218.85.152.99","218.30.19.40","218.85.157.99","61.134.1.4","202.101.224.69","202.100.64.68","202.101.226.68","61.178.0.93","61.132.163.68","219.141.136.10","202.102.213.68","219.141.140.10","219.150.32.132","219.146.0.130","202.106.196.115","202.102.128.68","202.106.46.151","202.102.152.3","202.106.0.20","202.102.134.68","202.106.195.68","202.102.154.3","221.5.203.98","210.21.196.6","221.7.92.98","221.5.88.88","202.99.160.68","202.102.224.68","202.99.166.4","202.102.227.68","202.97.224.69","202.98.0.68","202.97.224.68","202.98.5.68","221.6.4.66","202.99.224.68","221.6.4.67","202.99.224.8","202.99.192.66","221.11.1.67","202.99.192.68","221.11.1.68","210.22.70.3","119.6.6.6","210.22.84.3","124.161.87.155","202.99.104.68","221.12.1.227","202.99.96.68","221.12.33.227","117.50.11.11","117.50.22.22","106.186.17.181","128.199.248.105","203.248.252.2","198.153.192.1","198.153.194.1","199.85.126.20","199.85.127.20","199.91.73.222","42.120.21.30","202.14.67.4","202.14.67.14","203.80.96.10","203.80.96.9","202.67.240.222","202.67.240.221","203.83.112.1","203.83.113.1","202.45.84.58","202.45.84.59","202.81.252.1","202.81.252.2","202.85.146.104","202.60.252.8","168.95.1.1","168.95.192.1","61.56.211.185","211.78.130.2","210.200.211.193","139.175.252.16","139.175.150.20","165.21.100.88","165.21.83.88","220.220.248.1","220.220.248.2","220.220.248.9","220.220.248.10"]

def update_cdn():
    print("从各解析节点获取 CDN 服务器")
    cdn_results = {}
    total_iterations = len(DNS_SERVERS) * len(CDN_DOMAINS)
    with tqdm(total=total_iterations, desc="节点解析进度") as pbar:
        for server in DNS_SERVERS:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [server]
            for domain in CDN_DOMAINS:
                try:
                    answers = resolver.resolve(domain, 'A')
                    ips = [rdata.address for rdata in answers]
                    if domain not in cdn_results:
                        cdn_results[domain] = []
                    cdn_results[domain].extend(ips)
                except Exception as e:
                    pass
                    # print(f"  {domain} 解析失败: {e}")
                pbar.update(1)

    # 去重
    for domain in cdn_results:
        cdn_results[domain] = list(set(cdn_results[domain]))

    # 保存到 RescueWeiBoImage.json
    with open('RescueWeiBoImage.json', 'w') as f:
        json.dump(cdn_results, f, ensure_ascii=False, indent=4)

    # 计算所有域名的唯一IP总数
    all_ips = set()
    for ips in cdn_results.values():
        all_ips.update(ips)
    total_ips = len(all_ips)
    print(f"{total_ips}个 IP 地址已更新到RescueWeiBoImage.json\n")


def save_pic(url):
    print(f"尝试获取图片 {url.split('/')[-1]}")
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    with open('RescueWeiBoImage.json', 'r') as f:
        cdn_data = json.load(f)
    
    if domain not in cdn_data:
        print(f"Error: Domain {domain} not found in CDN data")
        return
    
    available_ips = cdn_data[domain]
    if not available_ips:
        print(f"Error: No IP addresses available for {domain}")
        return
    
    filename = os.path.basename(parsed_url.path)
    success = False
    random.shuffle(available_ips)
    
    pbar = tqdm(total=len(available_ips), desc="尝试进度")
    current_progress = 0
    
    for i, ip in enumerate(available_ips):
        try:
            headers = {
                "host": domain,
                'accept': 'accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'priority': 'i',
                'referer': 'https://weibo.com/',
                'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'image',
                'sec-fetch-mode': 'no-cors',
                'sec-fetch-site': 'cross-site',
                'sec-fetch-storage-access': 'active',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
            }
            
            ip_url = f"https://{ip}{parsed_url.path}"
            response = requests.get(ip_url, headers=headers, verify=False, timeout=5)
            
            if response.status_code == 200 and [] == response.history:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                success = True
                # 更新到当前进度
                pbar.update(i + 1 - current_progress)
                break
            
        except Exception as e:
            pass
            # print(f"Failed with IP {ip}: {str(e)}")
        
        # 更新进度条，记录当前进度
        pbar.update(1)
        current_progress = i + 1
    
    pbar.close()
    if not success:
        print("❌ 所有CDN节点尝试失败")
    else:
        print(f"✅ 图片已保存到 {filename}")

def main():
    parser = argparse.ArgumentParser(description="利用 CDN 缓存获取被删除不久的微博图片")
    parser.add_argument("picUrls", nargs="*", help="微博图片的URL，可传入多个")
    parser.add_argument("--updatecdn", action="store_true", help="更新微博图床的 CDN 服务器列表")
    
    args = parser.parse_args()
    
    if args.updatecdn:
        update_cdn()
    elif args.picUrls:
        for pic_url in args.picUrls:
            save_pic(pic_url)

if __name__ == "__main__":
    # Disable SSL verification warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    main()