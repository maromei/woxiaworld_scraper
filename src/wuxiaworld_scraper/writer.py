import os
from pathlib import Path
from textwrap import TextWrapper

import pypub

from wuxiaworld_scraper.navigate import UrlInfo


def fix_character_encoding(line: str) -> str:
    # ignore many characters which f.e. epub will not display
    # --> only ascii symbols
    return line.encode("ascii", "ignore").decode("utf-8")


def generate_text_content(title: str, body: list[dict]) -> str:

    formatted_title = title + "\n" + "-" * len(title)

    sections = []

    text_wrapper = TextWrapper()
    text_wrapper.width = 80

    for section in body:

        section_list = [fix_character_encoding(entry["text"]) for entry in section]
        section_text = "".join(section_list)
        section_text = "\n".join(text_wrapper.wrap(section_text))
        sections.append(section_text)

    sections.insert(0, formatted_title)
    content = "\n\n".join(sections)

    return content


def write_epub(title: str, content: dict, out_dir: Path | str):

    epub = pypub.Epub(title)

    for _, content_dict in content.items():

        chapter_title = fix_character_encoding(content_dict["title"])
        chapter_html = fix_character_encoding(content_dict["body"])

        epub_chapter = pypub.Chapter(chapter_title, chapter_html.encode("utf-8"))
        epub.add_chapter(epub_chapter)

    chapter_numbers = content.keys()
    min_chapter_num = min(chapter_numbers)
    max_chapter_num = max(chapter_numbers)

    epub_name = f"{title}_chapters_{min_chapter_num:04d}-{max_chapter_num:04d}"
    if min_chapter_num == max_chapter_num:
        epub_name = f"{title}_chapters_{min_chapter_num:04d}"

    epub_path = Path(out_dir) / epub_name

    if epub_path.exists():
        os.remove(epub_path)

    epub.create(epub_path)


def write_text(content: dict, out_dir: Path | str):

    for chapter, content_dict in content.items():

        chapter_text = generate_text_content(
            content_dict["title"], content_dict["body"]
        )

        file_path = Path(out_dir) / f"chapter_{chapter:04d}.txt"
        with open(file_path, "w+") as f:
            f.write(chapter_text)


def write(content: dict, base_path: str | Path, url_info: UrlInfo, as_epub: bool):

    out_dir = Path(base_path) / url_info.novel_name
    if not out_dir.exists():
        os.makedirs(out_dir)

    if as_epub:
        write_epub(url_info.novel_name, content, out_dir)
    else:
        write_text(content, out_dir)
