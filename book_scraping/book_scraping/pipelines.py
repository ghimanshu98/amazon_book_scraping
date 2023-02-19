# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo

class BookScrapingPipeline:
    def __init__(self) -> None:
        # creating connection
        self.conn = pymongo.MongoClient('localhost', 27017)

        # creating a db
        self.db = self.conn['books_db']

        # creating collection/ table
        self.tb = self.db['books_table']


    def process_item(self, item, spider):
        self.tb.insert_one(dict(item))
        return item
