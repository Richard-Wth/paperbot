from pathlib import Path
from typing import Dict, List
from urllib.parse import urljoin, urlencode

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}


class Spider:
    """
    《地质通报》和《岩石学报》的基于 requests 的爬虫，这两个网站都是使用的相同的框架，
    均为前后端分离，后端返回的 json 格式相同，下载的途径也相同。
    """

    mapping = {
        "dztb": {
            "index": "https://www.cgsjournals.com/",
            "publisherId": "dztb",
        },  # 地质通报
        "ysxb": {"index": "http://www.ysxb.ac.cn/", "publisherId": "aps"},  # 岩石学报
    }

    def __init__(
        self,
        name: str,
    ) -> None:
        assert name in self.mapping.keys()
        self.name = name
        self.before_start()
        self.start()
        self.after_start()

    def start(self) -> None:
        issue_links = self.get_issue_links()
        for issue in issue_links:
            pass

    def get_issue_links(self) -> List[str]:
        url = (
            urljoin(self.mapping[self.name]["index"], "/data/article/archive-list-data")
            + "?publisherId="
            + self.mapping[self.name]["publisherId"]
        )
        res = requests.get(url, headers=headers).json()
        link_prefix = urljoin(
            self.mapping[self.name]["index"], "/data/article/archive-article-data"
        )
        return [
            link_prefix
            + "?"
            + urlencode(
                {
                    "issue": data["issue"],
                    "publisherId": data["publisherId"],
                    "volume": "",
                    "year": data["year"],
                }
            )
            for data in res["data"]
        ]

    def get_issue_info(issue_url: str):
        res = requests.get(issue_url, headers=headers).json()
        return res


if __name__ == "__main__":
    s = Spider("dztb")
