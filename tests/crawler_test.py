import os
import shutil
from crawler.crawler import ArchiveCrawler

c = ArchiveCrawler()

def crawler_sample_archive_test():
    try:
        c.sample(3)
        print "crawler_sample_archive_test: PASS"
    except Exception as err:
        print err
        print "crawler_sample_archive_test: FAIL"
    
def crawler_get_permissions_test():
    try:
        c.get_permissions()
        print "crawler_get_permissions_test: PASS"
    
    except Exception as err:
        print err
        print "crawler_get_permissions_test: FAIL"
    
def crawler_download_test():
    try:
        c.download()
        print "crawler_download_test: PASS"
        
    except Exception as err:
        print err
        print "crawler_download_test: FAIL"
        
def crawler_test_cleanup():
    
    # delete database
    os.remove("./*.db")
    
    # delete downloaded apks
    shutil.rmtree("./apks/")
    
    print "crawler_test_cleanup: DONE"
