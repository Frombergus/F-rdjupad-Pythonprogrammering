import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
import math
import json


class WebScraper:
    """This class provides the functionality of collecting web data on housing from Hemnet.se. 
    Returns data as a json file."""

    def __init__(self):
        self.data = []
        self.input = []                                     # Added self.input to test carry some frequently used variables over the functions in the class.
        self.session = requests.Session()                   # Request session to self as it supposed to increase speed slightly vs reopening every iteration.
        self.logger = logging.getLogger(__name__)

    def save_data(self, data):
        self.logger.info('Saving data...')

    def add_input(self):
        url = 'https://www.hemnet.se/bostader?item_types[]=bostadsratt&location_ids[]=17753'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'}

        self.input = [url, headers]  # Initialize input list directly

        logging.info(f'Input list updated with URL: {url} and headers: {headers}.')
        return self.input

    def add_start_data(self):
        try:
            self.session.headers.update(self.input[1])              # Headers stored in self.input. quite handy when switching to another user or operating system.

            start_page_reg = self.session.get(self.input[0])
            if start_page_reg.status_code != 200:
                raise ValueError("Request using input URL/headers returned an error.")

            start_page_soup = BeautifulSoup(start_page_reg.content, 'lxml')     # Fetch 1st search page as starting point.

            for grid_script in start_page_soup.find_all("main", attrs={"class": "Layout_main__Fn5Ho", "tabindex": '-1', "id": "huvudinnehall"}):        # Extracting the main json file that contain the links to all objects on the search page.
                grid_script_content = grid_script.contents[0].text.strip()      # Filtering 
                grid_dict = json.loads(grid_script_content)        # Using json library for easy json to dict conversion.

            objects = grid_dict["numberOfItems"]        # Calculation how many search page iterations needed
            iterations = math.ceil(objects / 50)

            self.input.append(objects)
            self.input.append(iterations)

            logging.info(f'Input list updated with number of objects: {objects} and how many iterations it will take: {iterations}.')  
            return self.input

        except Exception as e:
            logging.error(f'Unable to create Grid dicr  from {self.input[0]} Error occurred: {e} ')


    def scrape_data(self):
        list_data = []
        for nbr in range(self.input[3]):   # nbr of iterations 
            try:
                object_page_url = f'{self.input[0]}&page={nbr + 1}'             # +1 as there are  no search page 0
                object_page_reg = self.session.get(object_page_url)
                object_page_soup = BeautifulSoup(object_page_reg.content, 'lxml')   # Fetching the page list of links to iterate over.

                for grid_script in object_page_soup.find_all("main", attrs={"class": "Layout_main__Fn5Ho", "tabindex": '-1', "id": "huvudinnehall"}): # Search and filter to make list of links usefull.
                    grid_script_content = grid_script.contents[0].text.strip()
                    grid_dict = json.loads(grid_script_content)     
                    logging.info(f'Grid dict for iteration {nbr} created with {len(grid_dict)} values.')

                if not grid_dict:
                    raise ValueError("Unable to parse HTML data from page request")

                for i in range(len(grid_dict["itemListElement"])):      # Start looping over the links.

                    page_url = grid_dict["itemListElement"][i]['url']
                    page_req = self.session.get(page_url)
                    page_soup = BeautifulSoup(page_req.content, 'lxml')

                    position = nbr*50 + grid_dict["itemListElement"][i]['position']         
                    page_dict = {'id': [position], 'Länk': [page_url]}      # Creating dict with an Id: for tracking and the link.

                    for dd, dt in page_soup.find_all('div', {'class': 'hcl-flex--container hcl-flex--direction-row'}):      # Fetching data for the object.
                        dd_text = dd.text.strip()
                        dt_text = dt.text.strip()

                        page_dict.setdefault(dd_text, []).append(dt_text)

                    for adr in page_soup.find_all('h1', {'class': 'Heading_hclHeading__KufPZ Heading_hclHeadingSize2__VUGbl'}):
                        page_dict.setdefault('Adress', []).append(adr.text.strip())

                    for pris in page_soup.find_all('span', {'class': 'ListingPrice_listingPrice__jg_CG'}):
                        page_dict.setdefault('Pris', []).append(pris.text.strip())

                    for besk in page_soup.find_all('span', {'class': 'Description_description__myLUo'}):
                        page_dict.setdefault('Beskrivning', []).append(besk.text.strip())

                    if not page_dict:
                        raise ValueError(f"Error processing data from {page_url}: {e}")

                    logging.info(f'page -> temp. Grid loop: {nbr} page loop: {i} vars in obj {len(page_dict)}. & collectet obj: {len(list_data)}')

                    list_data.append(page_dict)     # Collecting the data for each object 
                logging.info(f'(summera logg data stats till en snygg översikt)output data_list with: {len(list_data)} rows.')   

            except Exception as e:
                logging.error(f"Error processing data from {page_url}: {e}")        # Issues during scraping rarely manifested as error to catch, hence logging is quite detailed and can be used to trace back issues.

        self.data = list_data              
        with open("scraped_data.json", "w") as fp:
            json.dump(list_data, fp) 

    
    def scrape(self):
        self.add_input()
        self.add_start_data()
        self.scrape_data()
        print('data saved as scraped_data.json')