'''
    Crawl the archive.org repositories for 1000 randomly
    sample Android apks.
'''

from crawler.crawler import ArchiveCrawler

c = ArchiveCrawler()
c.sample(1000)
c.get_permissions()
c.download()
