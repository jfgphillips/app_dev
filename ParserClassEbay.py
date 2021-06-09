from random import randint
from time import sleep
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


class ParserClass:

    scrape_Count = 0  # this counts how many times the scrape is performed

    def __init__(self, search_term: str, pages: int):
        """
        :param search_term: string
                            --------------------------------
                            this containing the search term,
                            replaces " " with +
                            for ebay url parsing
                            --------------------------------
        :param pages: int
                            --------------------------------
                            this is an argument for the
                            number of pages to parse
                            --------------------------------
        """

        self.search_term = search_term.replace(" ", "+")
        self.li_url = "https://www.ebay.co.uk/sch/i.html?__fsrp=1&_nkw=" + \
                      self.search_term + \
                      "&_sacat=0&_from=R40&rt=nc&LH_SellerType=1"
        self.so_url = "https://www.ebay.co.uk/sch/i.html?__fsrp=1&_nkw=" + \
                      self.search_term + \
                      "&_sacat=0&_from=R40&LH_Complete=1&rt=nc&LH_Sold=1&LH_SellerType=1"
        self.pages = pages
        self.li_df = self.scrape_data(self.li_url)
        self.so_df = self.scrape_so_data(self.so_url)

        ParserClass.scrape_Count += 1

    def scrape_data(self, url: str):
        print("Scraping current listing data")
        """
        :param url: string
                    --------------------------------
                    This is a string for the url
                    in the future the url will
                    contain extra search parameters
                    controlled by a function in menu
                    --------------------------------

        :return: scraped_df: pandas df
                    --------------------------------
                    This is a df containing raw
                    scraped data from ebay. Allows
                    for differentiation between
                    auction and buy it now by identifying
                    "-" or a cell with that contains a str
                    --------------------------------
        """

        headers = {"Accept-Language": "en-UK, en;q=0.5"}

        # Ebay initiate data storage
        link = []
        title = []
        state = []
        price = []
        bids = []
        timer = []
        buy_now = []

        total_pages = np.arange(0, self.pages, 1)

        for page in total_pages:
            if page == 0:
                page = requests.get(url, headers=headers)
                print("the page is: ", page)
            else:
                page = requests.get(url + "&_pgn=" + str(total_pages), headers=headers)
                print("the page is: ", page)

            soup = BeautifulSoup(page.text, 'html.parser')
            print("printing soup:", soup)

            ebay_div = soup.find_all('div', class_="s-item__info clearfix")

            sleep(randint(2, 5))

            for container in ebay_div:
                # attrs = {'href': re.compile("^http://")
                entry_link = container.find('a', class_="s-item__link").get('href')
                link.append(entry_link)

                entry_name = container.a.h3.text
                title.append(entry_name)

                condition = container.find('span', class_='SECONDARY_INFO').text \
                    if container.find('span', class_='SECONDARY_INFO') \
                    else np.nan

                state.append(condition)

                if container.find('span', class_='s-item__price'):
                    cost = container.find('span', class_="s-item__price").text
                    for idx, blank in {"£": "", ",": ""}.items():  # this can be added to to remove all other currencies
                        cost = cost.replace(idx, blank)
                    price.append(cost)
                else:
                    cost = np.nan
                    price.append(cost)

                auction = container.find('span', class_="s-item__bids s-item__bidCount").text \
                    if container.find('span', class_='s-item__bids s-item__bidCount') \
                    else np.nan
                bids.append(auction)

                countdown = container.find('span', class_="s-item__time-left").text \
                    if container.find('span', class_='s-item__time-left') \
                    else np.nan
                timer.append(countdown)

                buy_now_price = container.find('span', class_="s-item__purchase-options-with-icon").text \
                    if container.find('span', class_='s-item__purchase-options-with-icon') \
                    else '-'
                buy_now.append(buy_now_price)

        scraped_df = pd.DataFrame({
            'listing link': link,
            'listing title': title,
            'price £': price,
            'condition': state,
            'Auction': bids,
            'time remaining': timer,
            'buy it now': buy_now
        })

        print(scraped_df)

        scraped_df['buy it now'].replace(np.nan, "Buy it now/Best offer", inplace=True)
        scraped_df['buy it now'].replace('-', np.nan, inplace=True)

        # replaces all instances of failed parsing e.g. price ranges 2.99 to 3.99 with nan
        scraped_df["price £"] = pd.to_numeric(scraped_df["price £"], errors='coerce').astype(float)
        # scraped_df["price £"].convert_objects(convert_numeric=True).astype(float)

        # removes duplicate entries from file
        scraped_df.drop_duplicates(inplace=True)
        return scraped_df

    def scrape_so_data(self, url: str):
        print("scraping sold data")
        headers = {"Accept-Language": "en-UK, en;q=0.5"}

        # Ebay initiate data storage
        link = []
        title = []
        state = []
        price = []
        bids = []
        timer = []
        buy_now = []

        total_pages = np.arange(0, self.pages, 1)

        for page in total_pages:
            if page == 0:
                page = requests.get(url, headers=headers)
                print("the page is: ", page)
            else:
                page = requests.get(url + "&_pgn=" + str(total_pages), headers=headers)
                print("the page is: ", page)

            soup = BeautifulSoup(page.text, 'html.parser')
            print("printing soup:", soup)

            ebay_div = soup.find_all('li', class_="s-item")
            print("printing div")
            print(ebay_div)

            sleep(randint(2, 5))

            for container in ebay_div:
                print("printing container")
                print(container)
                # attrs = {'href': re.compile("^http://")
                entry_link = container.find('a', class_="s-item__link").get('href')
                link.append(entry_link)

                entry_name = container.a.h3.text
                title.append(entry_name)

                condition = container.find('span', class_='SECONDARY_INFO').text \
                    if container.find('span', class_='SECONDARY_INFO') \
                    else np.nan

                state.append(condition)

                if container.find('span', class_='s-item__price'):
                    cost = container.find('span', class_="s-item__price").text
                    for idx, blank in {"£": "", ",": ""}.items():  # this can be added to to remove all other currencies
                        cost = cost.replace(idx, blank)
                    price.append(cost)
                else:
                    cost = np.nan
                    price.append(cost)

                auction = container.find('span', class_="s-item__bids s-item__bidCount").text \
                    if container.find('span', class_='s-item__bids s-item__bidCount') \
                    else np.nan
                bids.append(auction)

                countdown = container.find('span', class_="s-item__time-left").text \
                    if container.find('span', class_='s-item__time-left') \
                    else np.nan
                timer.append(countdown)

                buy_now_price = container.find('span', class_="s-item__purchase-options-with-icon").text \
                    if container.find('span', class_='s-item__purchase-options-with-icon') \
                    else '-'
                buy_now.append(buy_now_price)

        scraped_df = pd.DataFrame({
            'listing link': link,
            'listing title': title,
            'price £': price,
            'condition': state,
            'Auction': bids,
            'time remaining': timer,
            'buy it now': buy_now
        })

        print(scraped_df)

        scraped_df['buy it now'].replace(np.nan, "Buy it now/Best offer", inplace=True)
        scraped_df['buy it now'].replace('-', np.nan, inplace=True)

        # replaces all instances of failed parsing e.g. price ranges 2.99 to 3.99 with nan
        scraped_df["price £"] = pd.to_numeric(scraped_df["price £"], errors='coerce').astype(float)
        # scraped_df["price £"].convert_objects(convert_numeric=True).astype(float)

        # removes duplicate entries from file
        scraped_df.drop_duplicates(inplace=True)
        return scraped_df



    def get_li_url(self):
        return self.li_url

    def get_so_url(self):
        return self.so_url

    def get_li_df(self):
        return self.li_df

    def get_so_df(self):
        return self.so_df


