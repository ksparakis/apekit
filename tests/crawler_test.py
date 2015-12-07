from orangutan.crawler import ArchiveCrawler

c = ArchiveCrawler()
c.sample(3)
c.get_permissions()
c.download()
