from scrapy import cmdline

cmdline.execute("scrapy crawl science".split())
#cmdline.execute("scrapy crawl id -s JOBDIR=crawls/somespider-1".split())