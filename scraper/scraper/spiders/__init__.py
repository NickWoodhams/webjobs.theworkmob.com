# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import BaseSgmlLinkExtractor, SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scraper.items import Post
from pprint import pprint


def getStartURLs():
    cities = City.query.all()
    urls = []
    for city in cities:
        urls.append('http://' + city.name + '.craigslist.org/search/web?query=+')
    return urls


def fallback(key, item):
    try:
        post[key] = item
    except:
        raise DropItem("%s not found" % key)


class craigslistSpider(CrawlSpider):
    name = "craigs"
    allowed_domains = ["craigslist.org"]
    start_urls = getStartURLs()

    rules = (
        Rule(
            SgmlLinkExtractor(allow='.*/[0-9]{10}\.html'),
            'parse_item',
            follow=False,
        ),
    )

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        post = Post()
        post['url'] = response.url
        post['post_id'] = int(response.url[-15:-5])
        fallback('title', hxs.select('//h2[@class="postingtitle"]/text()')[1].extract().strip())
        fallback('email', hxs.select('//a').re(r'mailto:.*(?=</a>)')[0])
        fallback('body', hxs.select("//section[@id='postingbody']/text()").extract()[0])
        post['timestamp'] = datetime.datetime.fromtimestamp(int(hxs.select('//date/@title').extract()[0]) / 1e3)
        return post
