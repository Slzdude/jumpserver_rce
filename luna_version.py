import os
import re
import sys
import requests
from urllib.parse import urljoin

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python", sys.argv[0], "<jumpserver url>")
        exit(1)
    host = sys.argv[1]
    luna_path = urljoin(host, "luna/")
    print("fetching luna on:", luna_path)
    ret = requests.get(luna_path, verify=False).text
    re_js = re.compile(r'src="?(\S+\.js)"?>')
    all_js = re_js.findall(ret)
    print("all possible js:", all_js)
    check_js = list(filter(lambda x: "main." in x or "app." in x, all_js))
    re_version = [re.compile(r"v\d+\.\d+\.\d+"), re.compile(r'"(\d+\.\d+\.\d+(?:-\d+)?\s+GPL.+?)"')]
    for i in check_js:
        js_path = urljoin(luna_path, i)
        print("checking js:", js_path)
        ret = requests.get(js_path, verify=False).text
        for j in re_version:
            version_list = j.findall(ret)
            if version_list:
                print("possible version:", version_list)
