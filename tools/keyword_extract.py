"""
提取地学 Excel 表格数据中的关键字
"""
import json
import re
from pathlib import Path
from typing import Dict, List

import pandas as pd
from tqdm import tqdm

FILE_ROOT_DIR = Path("assets/地学").resolve()
PATTERNS = [
    re.compile(r"<[^>]+>", re.S),
    re.compile(r"\u0001", re.S),
    re.compile(r"（）", re.S),
    re.compile(r"{[a-zA-z0-9]+}\.", re.S),
    re.compile(r"\[[a-zA-z0-9]+\]\.", re.S),
    re.compile(r"\s-\s[0-9]+", re.S),
    re.compile(r",\s?[0-9]+", re.S),
]


def get_file_list(dir: Path = FILE_ROOT_DIR.joinpath("xls")) -> List[Path]:
    """获取一个文件夹下的所有文件的路径

    Args:
        dir (Path, optional): 需要遍历的文件夹. Defaults to FILE_ROOT_DIR.

    Returns:
        List[Path]: 文件夹下的所有文件路径名构成的列表
    """
    f_list = []
    for f in dir.iterdir():
        f_list.append(f)
    return f_list


def get_keywords(filepath: Path, column: str = "pre_label_e") -> List[str]:
    """获取 Excel 表中的某一列并去重后作为使用的关键词

    Args:
        filepath (Path): Excel 表格的文件路径
        column (str): 列名

    Returns:
        List[str]: 关键词列表
    """
    df = pd.read_excel(filepath)
    keywords = df[column].to_list()
    keywords = list(set(keywords))
    return keywords


def clean_keywords(keyword: str) -> str:
    """对关键字进行清洗"""
    # 去除 html 标签
    keyword = PATTERNS[0].sub("", keyword)
    # 去除 \u0001
    keyword = PATTERNS[1].sub("", keyword)
    # 去除 （）
    keyword = PATTERNS[2].sub("", keyword)
    # 去除大括号和中括号
    keyword = PATTERNS[3].sub("", keyword)
    keyword = PATTERNS[4].sub("", keyword)
    # 去除 [ - 数字]
    keyword = PATTERNS[5].sub("", keyword)
    # 去除 [, 数字]
    keyword = PATTERNS[6].sub("", keyword)
    return keyword.strip()


def save_keywords(
    obj: Dict[str, List[str]], filepath: Path = FILE_ROOT_DIR.joinpath("keywords.json")
) -> None:
    """将 dict 对象储存为 json 文件"""
    with open(filepath, "w") as f:
        json.dump(obj=obj, fp=f, ensure_ascii=False)


def main():
    kwd_dict = {}
    file_list = get_file_list()
    with tqdm(file_list) as pbar:
        for topic in file_list:
            pbar.set_description(topic.stem)
            keywords = get_keywords(topic)
            keywords = list(set(map(clean_keywords, keywords)))
            kwd_dict.update({topic.stem: keywords})
            pbar.update(1)
    save_keywords(obj=kwd_dict)


if __name__ == "__main__":
    main()
