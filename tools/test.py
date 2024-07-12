import requests

# r = requests.post(
#     url="http://www.ysxb.ac.cn/data/article/export-pdf",
#     data={"id": "aps_19850101"},
#     headers={
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     },
# )
r = requests.post(
    url="http://www.ysxb.ac.cn/data/article/export-pdf",
    data={"id": "dztb_20010101"},
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    },
)
with open("test.pdf","wb") as _:
    _.write(r.content)
pass