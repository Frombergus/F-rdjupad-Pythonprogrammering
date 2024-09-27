import logging
from itertools import chain
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
import math
import json
       

from webscraper import WebScraper
from datacleaner import DataCleaner
from datasaver import DataSaver

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, 
                    filename='scraper_log.log', 
                    filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

ws = WebScraper()
dc = DataCleaner()
ds = DataSaver()




ws.scrape()
dc.clean()
ds.save_data()
