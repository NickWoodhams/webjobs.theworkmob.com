# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import datetime
# sys.path.append('/Users/admin/Sites/webjobs/')
sys.path.append('/home/nick/webjobs.apixchange.com/webjobs/')
from modules.database import db_session, City, Post as P
from scrapy.exceptions import DropItem


class SavePipeline(object):
    def process_item(self, post, spider):
        if P.query.filter_by(post_id=post['post_id']).count():
            raise DropItem("Item already exists")
        elif post['email'] != '':
            raise DropItem("Email not listed")
        else:
            db_post = P(
                post_id=post['post_id'],
                title=post['title'],
                body=post['body'],
                email=post['email'],
                timestamp=post['timestamp'],
                url=post['url'],
            )
            db_session.add(db_post)
            db_session.commit()
            return post
