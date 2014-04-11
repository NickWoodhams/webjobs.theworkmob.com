# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import BaseSgmlLinkExtractor, \
    SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.exceptions import DropItem
from scraper.items import Post
from pprint import pprint
import sys
import datetime
sys.path.append('/Users/nick/Sites/apix/webjobs/')
sys.path.append('/home/nick/webjobs.apixchange.com/webjobs/')
from modules.database import db_session, City, Update, Post as P


def getStartURLs():
    cities = City.query.all()
    urls = []
    for city in cities:
        urls.append(
            'http://' + city.name + '.craigslist.org/search/web?query=+')
        urls.append(
            'http://' + city.name + '.craigslist.org/search/cpg?query=+')
    return urls


class craigslistSpider(CrawlSpider):
    name = "craigs"
    allowed_domains = ["craigslist.org"]
    # start_urls = getStartURLs()
    start_urls = ["http://kalamazoo.craigslist.org/search/web?query=+"]

    rules = (
        Rule(
            SgmlLinkExtractor(allow='.*/[0-9]{10}\.html'),
            'parse_item',
            follow=False,
        ),
    )

    def parse_item(self, response):
        hxs = Selector(response)
        post = Post()
        post['url'] = response.url
        post['post_id'] = int(response.url[-15:-5])
        post['title'] = hxs.xpath('//h2[@class="postingtitle"]/text()')[1] \
                           .extract().strip()
        # post['email'] = hxs.xpath('//a').re(r'mailto:.*(?=</a>)')[0]
        post['body'] = hxs.xpath("//section[@id='postingbody']/text()") \
                          .extract()[0]
        post['timestamp'] = hxs.xpath('//time/@datetime').extract()[0]
        return post
