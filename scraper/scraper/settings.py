# -*- coding: utf-8 -*-
"""
    scrapy stuff
    ~~~~~~~~
    scrapy settings file
"""
# Scrapy settings for scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

ITEM_PIPELINES = {
    'scraper.pipelines.SavePipeline': 300
}

LOG_ENABLED = True

# Crawl responsibly by identifying yourself on the user-agent
# USER_AGENT = 'scraper (+http://www.yourdomain.com)'
