import os
from pathlib import Path

from wuxiaworld_scraper import scraper, writer, navigate

if __name__ == "__main__":

    url: str = input("URL of starting chapter:\n\n")
    print()
    chapter_count: str = input("Number of chapters:\n\n")
    print()
    chapter_count = int(chapter_count)

    write_epub = True

    url = "https://www.wuxiaworld.com/novel/second-life-ranker/slr-chapter-19"
    content = scraper.scrape_chapters(url, chapter_count, write_epub)

    url_info = navigate.decompose_url(url)
    base_path = Path(os.getcwd()) / "output"

    writer.write(content, base_path, url_info, write_epub)
