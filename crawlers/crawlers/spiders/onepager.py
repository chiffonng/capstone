"""
Crawler for stories on just one page. Title is usually <h2> or <strong>, content is usually p.
"""

import scrapy
from crawlers.items import Story
from typing import List

URLS_H2 = [
    "https://goni.vn/truyen-ke-cho-be-nghe-truoc-gio-di-ngu",
    "https://ilo.edu.vn/truyen-cho-be-3-tuoi.htm",
]
URLS_STRONG = [
    "https://ilo.edu.vn/truyen-cho-be-3-tuoi.htm",
]
