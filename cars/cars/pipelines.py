# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import sqlite3

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)


class ValidationCleaningPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        for field in ("model", "name", "registration"):
            if not adapter.get(field):
                logger.warning(f"Dropping item missing '{field}': {dict(item)}")
                raise DropItem(f"Missing required field: {field}")

        mileage = adapter.get("mileage")
        if mileage:
            try:
                adapter["mileage"] = int(str(mileage).replace(",", "").strip())
            except ValueError:
                adapter["mileage"] = None

        fuel = adapter.get("fuel")
        if fuel:
            adapter["fuel"] = fuel.lower().strip()

        return item


class CarsPipeline:
    def __init__(self):
        self.conn = sqlite3.connect("bmw_cars.db")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS cars
                            (
                                registration TEXT PRIMARY KEY,
                                model        TEXT,
                                name         TEXT,
                                mileage      TEXT,
                                registered   TEXT,
                                engine       TEXT,
                                range        TEXT,
                                exterior     TEXT,
                                fuel         TEXT,
                                transmission TEXT,
                                upholstery   TEXT
                            )""")

    def process_item(self, item, spider):
        self.cur.execute(
            """INSERT OR IGNORE INTO cars
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                item["registration"],
                item["model"],
                item["name"],
                item["mileage"],
                item["registered"],
                item["engine"],
                item["range"],
                item["exterior"],
                item["fuel"],
                item["transmission"],
                item["upholstery"]))
        self.conn.commit()
        return item
