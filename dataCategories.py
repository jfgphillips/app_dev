import copy


class DataCategories:
    scrape_Count = 0  # this counts how many times the scrape is performed

    def __init__(self, listing_df, sold_df):
        """

        :param listing_df:
        :param sold_df:
        """
        self.listing_df = listing_df
        self.sold_df = sold_df

        self.auction_df = self.auction_data_func(self.listing_df)
        self.buy_now_df = self.buy_it_now_func(self.listing_df)
        self.sold_auction_df = self.auction_data_func(self.sold_df)
        self.sold_buy_now_df = self.buy_it_now_func(self.sold_df)

        DataCategories.scrape_Count += 1

    def auction_data_func(self, raw_data):
        """ method to clean raw data and isolate auctions
        inputs:
        ----------
        raw_data = a pandas data frame
                   with unsorted auction and buy it now prices

        returns:
        ----------
        au_data = a clean pandas data frame
                  containing only auction data
        """
        data_copy = copy.deepcopy(raw_data)
        auction_columns = ['listing link',
                           'listing title',
                           'price £',
                           'condition',
                           'time remaining']  # these are the columns containing auction data
        au_data = data_copy[auction_columns]
        # au_data["price £"] = au_data.to_numeric(au_data['price £'], errors='coerce').astype(float)

        # brutal deletion of data rigorous testing required for validity
        au_data.dropna(axis='rows', inplace=True)

        # try:
        #    au_data["price £"] = (au_data['price £'].str.replace("£", '')).astype(float)
        # except ValueError:
        #    print("could not be converted")

        return au_data

    def buy_it_now_func(self, raw_data):
        """ method to clean raw data and isolate buy it now
        inputs:
        ----------
        raw_data = a pandas data frame
                   with unsorted aucion and buy it now prices

        returns:
        ----------
        by_data = a clean pandas data frame
                  containing only buy it now data
        """
        data_copy = copy.deepcopy(raw_data)
        buy_now_columns = ['listing link',
                           'listing title',
                           'price £',
                           'condition',
                           'buy it now']
        by_data = data_copy[buy_now_columns]

        # by_data["price £"].str.rsplit(' ', 1).str.get(0)

        by_data.dropna(axis='rows', inplace=True)
        return by_data

    def getAuction_df(self):
        return self.auction_df

    def getBuy_now_df(self):
        return self.buy_now_df

    def getSold_auction_df(self):
        return self.sold_auction_df

    def getSold_buy_now_df(self):
        return self.sold_buy_now_df
