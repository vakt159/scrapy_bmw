BOT_NAME = "cars"
SPIDER_MODULES = ["cars.spiders"]
NEWSPIDER_MODULE = "cars.spiders"

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": True}

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "cars.middlewares.RandomUserAgentMiddleware": 400,
}

ITEM_PIPELINES = {
    "cars.pipelines.ValidationCleaningPipeline": 200,
    "cars.pipelines.CarsPipeline": 300,
}

AUTOTHROTTLE_ENABLED = True
ROBOTSTXT_OBEY = False
FEED_EXPORT_ENCODING = "utf-8"