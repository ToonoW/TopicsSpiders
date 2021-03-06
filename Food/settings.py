# -*- coding: utf-8 -*-

# Scrapy settings for TopicsSpiders project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Food'

LOG_LEVEL = 'WARNING'

SPIDER_MODULES = ['Food.spiders']
NEWSPIDER_MODULE = 'Food.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'TopicsSpiders (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-Hans-CN, en-CN, en-us',
    'User-Agent': 'FoodLibrary/2017121500',
    'Phone-Model': 'iPhone',
    'App-Key': 'food',
    'App-Version': '2.7.5',
    'App-Device': 'ios',
    'Device_Id': 'ec259f2092b1464a8f54eeff633a5fd4',
    'Os-Version': '11.2.1',
    'Host': 'food.boohee.com',
    'Content-Type': 'application/json; charset=utf-8',
}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'TopicsSpiders.middlewares.TopicsspidersSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'TopicsSpiders.middlewares.MyCustomDownloaderMiddleware': 543,
    # 'TopicsSpiders.middlewares.MyAgentMiddleware': 544,
    # 'TopicsSpiders.middlewares.DoubanCookieChangeMiddleware': 545,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'TopicsSpiders.pipelines.TopicsspidersPipeline': 300,
    'TopicsSpiders.pipelines.DuplicatesPipeline': 300,
    'TopicsSpiders.pipelines.CollectImageUrlPipeline': 301,
    'TopicsSpiders.pipelines.ImagesDownloadPipeline': 302,
    'TopicsSpiders.pipelines.MongoDBPipeline': 310,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# MongoDB Database Info
MONGO_URI = 'mongodb://120.24.63.55:37017'    # 生产用
MONGO_URI = 'mongodb://localhost:27017'         # 开发用
MONGO_DATABASE = 'food'
MONGO_COLLECTION = 'food_items'

# 图片存储
IMAGES_STORE = './images'
# 避免重复下载，设置图片过期时间
IMAGES_EXPIRES = 30
