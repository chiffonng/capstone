# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
import scrapy


@dataclass
class Story:
    url: str
    title: str
    text: str
    category: str | List[str]
    is_synthetic: bool = False

    def __post_init__(self):
        valid_categories = ["tale", "story", "textbook", "student writing"]
        if self.category not in valid_categories:
            raise ValueError(
                f"Invalid category: {self.category}. Valid categories are: {valid_categories}"
            )
