import json
import requests
import logging

from sys import argv as sys_argv
from bs4 import BeautifulSoup


def fudan_daily(username, passwd):
    # 伪造 UA
    headers = {
        "Origin": "https://zlapp.fudan.edu.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
        "Referer": "https://zlapp.fudan.edu.cn/site/ncov/fudanDaily?from=history"
    }

    # 学号 & UIS密码
    data = {
        "username": username,
        "password": passwd
    }

    login_url = "https://uis.fudan.edu.cn/authserver/login?service=https%3A%2F%2Fzlapp.fudan.edu.cn%2Fa_fudanzlapp%2Fapi%2Fsso%2Findex%3Fredirect%3Dhttps%253A%252F%252Fzlapp.fudan.edu.cn%252Fsite%252Fncov%252FfudanDaily%253Ffrom%253Dhistory%26from%3Dwap"
    get_info_url = "https://zlapp.fudan.edu.cn/ncov/wap/fudan/get-info"
    save_url = "https://zlapp.fudan.edu.cn/ncov/wap/fudan/save"

    s = requests.Session()
    response = s.get(login_url)
    content = response.text
    soup = BeautifulSoup(content, "lxml")
    inputs = soup.find_all("input")

    for i in inputs[2::]:
        data[i.get("name")] = i.get("value")

    response = s.post(login_url, data=data)
    response = s.get(get_info_url)

    old_pafd_data = json.loads(response.text)
    pafd_data = old_pafd_data["d"]["info"]

    pafd_data.update({
        "ismoved": 0,
        "number": old_pafd_data["d"]["uinfo"]["role"]["number"],
        "realname": old_pafd_data["d"]["uinfo"]["realname"],
        "area": old_pafd_data["d"]["oldInfo"]["area"],
        "city": old_pafd_data["d"]["oldInfo"]["city"],
        "province": old_pafd_data["d"]["oldInfo"]["province"],
        "sfhbtl": 0,
        "sfjcgrq": 0,
        "sftgfxcs": 1
    })

    logging.info(pafd_data["area"])
    s.headers.update(headers)
    response = s.post(save_url, data=pafd_data)

    logging.info(response.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    uid, pwd = sys_argv[1].strip().split(' ')
    fudan_daily(uid, pwd)
