# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import datetime
sys.path.append('/Users/admin/Sites/webjobs/')
from modules.database import db_session, City, Post as P


class SavePipeline(object):
    def process_item(self, item, spider):
        if P.query.filter_by(post_id=post['post_id']).count():
            print "item already exists"
        else:
            print "inserting item"
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

        return item
