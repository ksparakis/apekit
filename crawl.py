'''
    Crawl the archive.org repositories for 1000 randomly
    sample Android apks.
'''

from datetime import datetime
from crawler.crawler import ArchiveCrawler

NUM_SAMPLES = 1000

c = ArchiveCrawler()
print ("="*80)
print "{:<40}{:>40}".format("CRAWL STARTED", str(datetime.now()))
print ("="*80)
c.sample(NUM_SAMPLES)
print ("="*80)
print "{:<40}{:>40}".format("SAMPLING COMPLETED", str(datetime.now()))
print ("="*80)
c.get_permissions()
print ("="*80)
print "{:<40}{:>40}".format("PERMISSIONS COMPLETED", str(datetime.now()))
print ("="*80)
c.download()
print ("="*80)
print "{:<40}{:>40}".format("CRAWL COMPLETED", str(datetime.now()))
print ("="*80)
