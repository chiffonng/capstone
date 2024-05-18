"""
This is the spider for crawling sachhayonline.com
"""

import scrapy
from crawlers.items import Story
from typing import List


def get_urls():
    """Get starting urls for the spider"""

    root_urls: List[str] = [
        "https://www.sachhayonline.com/tua-sach/kho-tang-truyen-co-tich-viet-nam/su-tich-dua-hau/1570",
        "https://www.sachhayonline.com/tua-sach/kho-tang-truyen-co-tich-viet-nam",
    ]
    return root_urls
