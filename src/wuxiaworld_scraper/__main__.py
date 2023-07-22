import os
from pathlib import Path

from wuxiaworld_scraper import scraper, writer, navigate

if __name__ == "__main__":

    url: str = input("URL of starting chapter:\n")
    chapter_count: str = input("Number of chapters:\n")
    chapter_count = int(chapter_count)
    output_format = input(
        "Which format should should the output have? "
        "(t) txt, (e) epub, (b) both [default: both]\n"
    )
    do_login = input(
        "Should the scraper wait for you to login? " "(y) yes, (n) no [default no]\n"
    )

    write_text = output_format == "txt" or output_format == "t"
    write_epub = output_format == "epub" or output_format == "e"
    write_both = output_format == "both" or output_format == "b"

    write_both = write_both or output_format.strip() == ""
    write_text = write_text or write_both
    write_epub = write_epub or write_both

    do_login = do_login.strip() == "y" or do_login.strip() == "yes"

    text_content, epub_content = scraper.scrape_chapters(url, chapter_count, do_login)

    url_info = navigate.decompose_url(url)
    base_path = Path(os.getcwd()) / "output"

    if write_epub:
        writer.write(epub_content, base_path, url_info, True)

    if write_text:
        writer.write(text_content, base_path, url_info, False)
