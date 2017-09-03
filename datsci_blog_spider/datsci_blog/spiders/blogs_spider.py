"""
Function: Scrape blog posts. Adapted from:
https://doc.scrapy.org/en/latest/intro/tutorial.html
Author: Siobhan Grayson
"""
import scrapy
# ------------------------------------------------------------------------------
class BlogSpider(scrapy.Spider):
    name = "blogs"
    start_urls = [
        'https://www.datsciawards.ie/news/',
    ]

    def parse(self, response):
        # Start on main blog page.
        all_posts = response.css("article")
        # Extract links to page of posts themselves.
        for href in all_posts.css("div.fusion-post-wrapper a.fusion-read-more::attr(href)"):
            # Follow links to post page to extract content.
            yield response.follow(href, self.parse_blog)

    def parse_blog(self, response):
        def extract_with_css(query):
            return response.css(query).extract()

        yield {
            'title'  : extract_with_css('article h1.entry-title::text'),
            # Third item in list is date for all pages.
            'date'   : extract_with_css('div.fusion-meta-info-wrapper span::text')[2],
            # * will visit all inner tags of p (<span><strong> etc) and get text.
            # https://stackoverflow.com/questions/40985060/scrapy-css-selector-get-text-of-all-inner-tags
            # https://stackoverflow.com/questions/25019175/using-multiple-css-selectors-for-the-same-articleitem-in-scrapy
            'content': extract_with_css('article p *::text, article div.post-content li *::text')

        }
# ------------------------------------------------------------------------------
