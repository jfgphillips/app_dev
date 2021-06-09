from datetime import datetime
import os
import pandas as pd


class applicationIO:

    def __init__(self, search_term: str, parent_dir):
        self.search_term = search_term
        self.parent_dir = parent_dir

    def file_save(self, li_df, so_df):
        """
        :param li_df:
        :param so_df:
        :return: li_fp, so_fp
        """

        directory = "eBay " + self.search_term + " " + str(
            datetime.now().strftime('%d-%m-%y at %H.%M'))
        # Directory

        # Parent Directory path

        # Path
        path = os.path.join(self.parent_dir, directory)

        # Create the directory
        # search argument and a date in
        # '/Users/john/Documents/app development/parsed files'
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s" % path)

        list_fp = path + '/' + 'current private sellers of the ' + self.search_term + ".csv"
        sold_fp = path + '/' + 'sold private sellers of the ' + self.search_term + ".csv"
        li_df.to_csv(list_fp, index=False)
        so_df.to_csv(sold_fp, index=False)
        return list_fp, sold_fp

    def file_import(self, list_file_path, sold_file_path):
        """
        :param list_file_path:
        :param sold_file_path:
        :return:
        """

        listing_df = pd.read_csv(list_file_path)
        listing_df.drop_duplicates(inplace=True)
        historical_data = pd.read_csv(sold_file_path)
        historical_data.drop_duplicates(inplace=True)

        return listing_df, historical_data
