import re
import time

from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


@dataclass
class UrlInfo:

    base_url: str
    novel_name: str
    chapter_prefix: str


def decompose_url(url: str) -> UrlInfo:

    novel_name = re.search(r"(?<=novel/).*(?=/)", url)
    if novel_name is not None:
        novel_name = novel_name.group(0)

    chapter_prefix = re.search(rf"(?<={novel_name}/).*[^\d](?=\d+$)", url)
    if chapter_prefix is not None:
        chapter_prefix = chapter_prefix.group(0)

    base_url = re.search(rf"^.*(?=/{novel_name}/)", url)
    if base_url is not None:
        base_url = base_url.group(0)

    url_info = UrlInfo(base_url, novel_name, chapter_prefix)

    return url_info


def get_chapter_url(url_info: UrlInfo, chapter: int) -> str:
    return (
        f"{url_info.base_url}/{url_info.novel_name}/{url_info.chapter_prefix}{chapter}"
    )


def get_chapter_from_url(url: str) -> int:

    chapter = re.search(r"(?<=[^\d])\d+$", url)
    if chapter is None:
        return -1

    chapter = int(chapter.group(0))
    return chapter
