# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import BaseSgmlLinkExtractor, SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scraper.items import Post
from pprint import pprint
import sys
import datetime
sys.path.append('/Users/admin/Sites/webjobs/')
from modules.database import db_session, City, Post as P


def getStartURLs():
    cities = City.query.all()
    urls = []
    for city in cities:
        urls.append('http://' + city.name + '.craigslist.org/search/web?query=+')
    return urls


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
        post['title'] = hxs.select('//h2[@class="postingtitle"]/text()')[1].extract().strip()
        post['body'] = hxs.select("//section[@id='postingbody']/text()").extract()[0]
        try:
            post['email'] = hxs.select('//a').re(r'mailto:.*(?=</a>)')[0]
        except:
            post['email'] = ''
        post['timestamp'] = datetime.datetime.fromtimestamp(int(hxs.select('//date/@title').extract()[0]) / 1e3)

        #insert in the db if it does not exist
        if not P.query.filter_by(post_id=post['post_id']).count() and post['email'] != '':
            post = P(
                post_id=post['post_id'],
                title=post['title'],
                body=post['body'],
                email=post['email'],
                timestamp=post['timestamp'],
                url=post['url'],
            )
            db_session.add(post)
            db_session.commit()
