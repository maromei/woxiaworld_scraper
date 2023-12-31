import time

import getpass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from wuxiaworld_scraper import navigate


SCRAPING_SLEEP = 1


class Scraper:
    def __init__(self, base_url) -> None:
        self.browser = webdriver.Firefox()
        self.visit(base_url)

    def visit(self, url) -> None:
        self.browser.get(url)

    def get_html(self) -> str:
        return self.browser.page_source

    def get_title(self) -> str:
        element = self.browser.find_element(By.TAG_NAME, "h4")
        return element.text

    def get_body(self) -> str:

        element = self.browser.find_element(By.CSS_SELECTOR, "div.chapter-content")
        body = element.find_element(By.XPATH, "./*")

        epub_body = body.get_attribute("innerHTML")
        epub_body = epub_body.replace("&nbsp;", "")

        text_bdoy = parse_body_to_text(body)

        return epub_body, text_bdoy

    def close(self):
        self.browser.close()


def get_style_dict(style: str) -> dict:

    style_dict = {
        "font-style": "normal",
    }

    return style_dict

    if style is None:
        return style_dict

    style_list = style.split(";")
    for style_elem in style_list:

        key, value = style_elem.split(":")
        style_dict[key] = value

    return style_dict


def parse_span(span: WebElement) -> dict[str, str]:

    text = span.text

    style = span.get_dom_attribute("style")

    style_dict = get_style_dict(style)

    span_info = {
        "text": text,
        "style": style_dict,
    }

    return span_info


def parse_body_to_text(element: WebElement):

    p_elements = element.find_elements(By.TAG_NAME, "p")
    content_list = []

    for p in p_elements:
        spans = p.find_elements(By.XPATH, "./span")

        section_list = []

        for span in spans:
            span_info = parse_span(span)
            section_list.append(span_info)

        content_list.append(section_list)

    return content_list


def scrape_chapters(
    starting_url: str, chapter_count: int, wait_for_login: bool
) -> tuple[dict, dict]:

    url_info = navigate.decompose_url(starting_url)
    current_chapter = navigate.get_chapter_from_url(starting_url)

    epub_content = dict()
    text_content = dict()

    scraper = Scraper(url_info.host)

    if wait_for_login:
        getpass.getpass("press ENTER when you are done logging in.")

    for chapter in range(current_chapter, current_chapter + chapter_count):

        url = navigate.get_chapter_url(url_info, chapter)
        scraper.visit(url)

        time.sleep(5)

        title = scraper.get_title()
        epub_body, text_body = scraper.get_body()

        epub_content[chapter] = {"title": title, "body": epub_body}
        text_content[chapter] = {"title": title, "body": text_body}

        time.sleep(SCRAPING_SLEEP)

    scraper.close()

    return text_content, epub_content
