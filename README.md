# BlueDanube
Mass DNS record downloader/scraper

BlueDanube, named after the British Nuclear bomb, is a tool designed to massdownload/scrape DNS records from lists of domains. Due to recent enhanced versions being created in house, we have decided to opensource this older version for public use.

# WARNING
Whilst this can be used for scraping millions of records, we strongly suggest you do not, unless you want to be blocked from some DNS service providers. We also recommend not using CloudFlare dns, which is incredibly fast but does not support TYPE ANY record lookups.

# Usage

python3 BlueDanube.py -iL filename.txt > output.txt




