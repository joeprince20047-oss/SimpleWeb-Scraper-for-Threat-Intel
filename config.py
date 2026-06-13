# config.py - Configuration File
# Centralises all threat scraper settings. No logic, only data.

FEEDS = {
    "urlhaus": "https://urlhaus.abuse.ch/downloads/text/",
    "feodotracker": "https://feodotracker.abuse.ch/downloads/ipblocklist.txt",
    "sslblacklist": "https://sslbl.abuse.ch/blacklist/sslipblacklist.txt"
}

OUTPUT_DIR = "output/"
REQUEST_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
DEFAULT_FORMAT = "json"  # json | csv | txt
