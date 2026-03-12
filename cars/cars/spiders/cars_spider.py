import json
import re
import scrapy
from scrapy_playwright.page import PageMethod
from cars.items import CarsItem


class CarsSpider(scrapy.Spider):
    name = "usedcars"
    start_urls = [
        "https://usedcars.bmw.co.uk/result/?payment_type=cash&size=23&source=home"
    ]
    MAX_PAGES = 5

    async def start(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "div[data-list-id]"),
                    ],
                },
                callback=self.parse,
            )

    def parse(self, response):
        current_page = int(response.url.split("page=")[1].split("&")[0]) \
            if "page=" in response.url else 1

        cars = response.css("div[data-list-id]")
        self.logger.info(f"Page {current_page}: found {len(cars)} cars")

        for car in cars:
            href = car.css("a.btn.btn-primary::attr(href)").get()
            if href:
                yield scrapy.Request(
                    response.urljoin(href),
                    callback=self.parse_car,
                )

        if current_page < self.MAX_PAGES:
            next_url = f"https://usedcars.bmw.co.uk/result/?page={current_page + 1}&size=23"
            yield scrapy.Request(
                next_url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "div[data-list-id]"),
                    ],
                },
                callback=self.parse,
            )

    def parse_car(self, response):
        match = re.search(r'UVL\.AD\s*=\s*(\{.*?\});', response.text, re.DOTALL)
        if not match:
            self.logger.warning(f"No UVL.AD found on {response.url}")
            return

        data = json.loads(match.group(1))

        car = CarsItem()

        car["model"] = data.get("title")
        car["name"] = data.get("specification", {}).get("derivative")
        car["registration"] = data.get("identification", {}).get("registration")
        car["registered"] = data.get("dates", {}).get("registration")
        car["fuel"] = data.get("engine", {}).get("fuel")
        car["transmission"] = data.get("specification", {}).get("transmission")
        car["exterior"] = data.get("colour", {}).get("manufacturer_colour")
        car["upholstery"] = data.get("specification", {}).get("interior")

        mileage = data.get("condition_and_state", {}).get("mileage")
        car["mileage"] = str(mileage) if mileage is not None else None

        engine_cc = data.get("engine", {}).get("size", {}).get("cc")
        car["engine"] = str(engine_cc) if engine_cc else None

        range_value = data.get("consumption", {}).get("range", {}).get("values", {}).get("total")
        car["range"] = str(range_value) if range_value else None

        yield car